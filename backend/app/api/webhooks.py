import hashlib
import hmac
import json

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.models import IntakeSubmission

router = APIRouter(prefix="/api/webhooks", tags=["Provider webhooks"])
MAX_WEBHOOK_BYTES = 1_000_000
MAX_MESSAGE_CHARS = 10_000


@router.get("/whatsapp")
def verify_whatsapp_webhook(
    mode: str | None = Query(default=None, alias="hub.mode"),
    verify_token: str | None = Query(default=None, alias="hub.verify_token"),
    challenge: str | None = Query(default=None, alias="hub.challenge"),
):
    if not settings.WHATSAPP_VERIFY_TOKEN:
        raise HTTPException(
            status_code=503, detail="WhatsApp webhook verification is not configured."
        )
    if (
        mode != "subscribe"
        or not verify_token
        or not hmac.compare_digest(verify_token, settings.WHATSAPP_VERIFY_TOKEN)
        or not challenge
    ):
        raise HTTPException(status_code=403, detail="Webhook verification failed.")
    return Response(content=challenge, media_type="text/plain")


def _text_messages(payload: object) -> list[tuple[str, str]]:
    if not isinstance(payload, dict) or payload.get("object") != "whatsapp_business_account":
        return []
    messages: list[tuple[str, str]] = []
    entries = payload.get("entry", [])
    if not isinstance(entries, list):
        return messages
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        changes = entry.get("changes", [])
        if not isinstance(changes, list):
            continue
        for change in changes:
            if not isinstance(change, dict):
                continue
            value = change.get("value", {})
            if not isinstance(value, dict):
                continue
            inbound = value.get("messages", [])
            if not isinstance(inbound, list):
                continue
            for message in inbound:
                if not isinstance(message, dict) or message.get("type") != "text":
                    continue
                message_id = message.get("id")
                text = message.get("text", {})
                body = text.get("body") if isinstance(text, dict) else None
                if (
                    isinstance(message_id, str)
                    and message_id
                    and isinstance(body, str)
                    and body.strip()
                    and len(body) <= MAX_MESSAGE_CHARS
                ):
                    messages.append((message_id, body))
    return messages


@router.post("/whatsapp")
async def receive_whatsapp_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    if not settings.WHATSAPP_APP_SECRET:
        raise HTTPException(
            status_code=503, detail="WhatsApp webhook signing is not configured."
        )
    raw_body = await request.body()
    if len(raw_body) > MAX_WEBHOOK_BYTES:
        raise HTTPException(status_code=413, detail="Webhook payload is too large.")

    signature = request.headers.get("X-Hub-Signature-256", "")
    expected_signature = "sha256=" + hmac.new(
        settings.WHATSAPP_APP_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Webhook signature is invalid.")

    try:
        payload = json.loads(raw_body)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise HTTPException(status_code=400, detail="Webhook JSON is invalid.") from exc

    accepted = 0
    duplicates = 0
    for message_id, body in _text_messages(payload):
        if db.query(IntakeSubmission).filter(
            IntakeSubmission.source_message_id == message_id
        ).first():
            duplicates += 1
            continue
        db.add(
            IntakeSubmission(
                source_channel="whatsapp",
                source_message_id=message_id,
                source_text=body,
                status="pending",
            )
        )
        try:
            db.commit()
            accepted += 1
        except IntegrityError:
            db.rollback()
            duplicates += 1

    return {
        "status": "ok",
        "accepted": accepted,
        "duplicates": duplicates,
    }
