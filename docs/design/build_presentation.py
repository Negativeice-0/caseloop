#!/usr/bin/env python3
"""Build the editable CaseLoop stakeholder deck using Python's standard library."""

from __future__ import annotations

from html import escape
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


OUT = Path(__file__).with_name("CaseLoop_Stakeholder_Design_Brief.pptx")
SLIDE_W = 12_192_000
SLIDE_H = 6_858_000
SCALE_X = SLIDE_W / 1000
SCALE_Y = SLIDE_H / 562.5

NAVY = "0F172A"
RED = "C62828"
TEAL = "0F766E"
BLUE = "2563EB"
AMBER = "B45309"
WHITE = "FFFFFF"
BG = "F8FAFC"
PALE = "F1F5F9"
MID = "475569"
MUTED = "64748B"
LINE = "CBD5E1"
GREEN = "15803D"


def emu(value: float, scale: float) -> int:
    return round(value * scale)


def esc(value: str) -> str:
    return escape(value, quote=True)


class Slide:
    def __init__(self) -> None:
        self.shapes: list[str] = []
        self.next_id = 2

    def add(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        fill: str | None = None,
        stroke: str | None = None,
        geometry: str = "rect",
        text: str | None = None,
        size: int = 16,
        color: str = NAVY,
        bold: bool = False,
        align: str = "l",
        valign: str = "ctr",
        inset: float = 10,
    ) -> None:
        shape_id = self.next_id
        self.next_id += 1
        name = f"Shape {shape_id}"
        fill_xml = (
            f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>'
            if fill
            else "<a:noFill/>"
        )
        line_xml = (
            f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{stroke}"/></a:solidFill></a:ln>'
            if stroke
            else "<a:ln><a:noFill/></a:ln>"
        )
        tx_body = ""
        if text is not None:
            paragraphs = []
            for line in text.split("\n"):
                paragraphs.append(
                    "<a:p>"
                    f'<a:pPr algn="{align}"><a:buNone/></a:pPr>'
                    "<a:r>"
                    f'<a:rPr lang="en-US" sz="{size * 100}" b="{1 if bold else 0}">'
                    f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
                    '<a:latin typeface="Aptos"/>'
                    "</a:rPr>"
                    f"<a:t>{esc(line)}</a:t>"
                    "</a:r>"
                    f'<a:endParaRPr lang="en-US" sz="{size * 100}"/>'
                    "</a:p>"
                )
            tx_body = (
                f'<p:txBody><a:bodyPr wrap="square" anchor="{valign}" '
                f'lIns="{emu(inset, SCALE_X)}" rIns="{emu(inset, SCALE_X)}" '
                f'tIns="{emu(inset, SCALE_Y)}" bIns="{emu(inset, SCALE_Y)}">'
                "</a:bodyPr><a:lstStyle/>"
                + "".join(paragraphs)
                + "</p:txBody>"
            )
        self.shapes.append(
            "<p:sp>"
            f'<p:nvSpPr><p:cNvPr id="{shape_id}" name="{name}"/>'
            "<p:cNvSpPr/><p:nvPr/></p:nvSpPr>"
            "<p:spPr>"
            f'<a:xfrm><a:off x="{emu(x, SCALE_X)}" y="{emu(y, SCALE_Y)}"/>'
            f'<a:ext cx="{emu(w, SCALE_X)}" cy="{emu(h, SCALE_Y)}"/></a:xfrm>'
            f'<a:prstGeom prst="{geometry}"><a:avLst/></a:prstGeom>'
            f"{fill_xml}{line_xml}</p:spPr>{tx_body}</p:sp>"
        )

    def rect(self, x: float, y: float, w: float, h: float, fill: str, **kwargs: object) -> None:
        self.add(x, y, w, h, fill=fill, **kwargs)

    def text(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        value: str,
        size: int = 16,
        color: str = NAVY,
        bold: bool = False,
        align: str = "l",
        valign: str = "ctr",
    ) -> None:
        self.add(x, y, w, h, text=value, size=size, color=color, bold=bold, align=align, valign=valign)

    def xml(self) -> str:
        group = (
            '<p:nvGrpSpPr><p:cNvPr id="1" name=""/>'
            "<p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>"
            "<p:grpSpPr><a:xfrm><a:off x=\"0\" y=\"0\"/>"
            "<a:ext cx=\"0\" cy=\"0\"/><a:chOff x=\"0\" y=\"0\"/>"
            "<a:chExt cx=\"0\" cy=\"0\"/></a:xfrm></p:grpSpPr>"
        )
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            "<p:cSld><p:spTree>"
            + group
            + "".join(self.shapes)
            + "</p:spTree></p:cSld>"
            "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>"
        )


def base_slide(title: str, kicker: str, page: int) -> Slide:
    s = Slide()
    s.rect(0, 0, 1000, 562.5, BG)
    s.rect(0, 0, 1000, 7, RED)
    s.text(42, 24, 800, 22, kicker.upper(), 10, RED, True)
    s.text(42, 48, 900, 42, title, 26, NAVY, True)
    s.rect(42, 98, 916, 1.5, LINE)
    s.text(42, 532, 760, 18, "CASELOOP  |  DESIGN CONCEPT  |  SYNTHETIC DATA", 8, MUTED, True)
    s.text(920, 529, 38, 22, f"{page:02d}", 10, RED, True, "r")
    return s


def card(s: Slide, x: float, y: float, w: float, h: float, title: str, body: str, accent: str = RED) -> None:
    s.add(x, y, w, h, fill=WHITE, stroke="E2E8F0", geometry="roundRect")
    s.rect(x, y, 5, h, accent)
    s.text(x + 16, y + 12, w - 30, 25, title, 15, NAVY, True)
    s.text(x + 16, y + 42, w - 30, h - 52, body, 11, MID, False, valign="t")


def make_deck() -> list[Slide]:
    slides: list[Slide] = []

    # 1. Cover
    s = Slide()
    s.rect(0, 0, 1000, 562.5, NAVY)
    s.rect(0, 0, 12, 562.5, RED)
    s.rect(54, 42, 46, 46, RED, geometry="roundRect")
    s.text(54, 44, 46, 42, "CL", 17, WHITE, True, "ctr")
    s.text(116, 46, 420, 34, "CaseLoop", 24, WHITE, True)
    s.text(116, 75, 420, 20, "FIELD INFORMATION  /  CLEAR ASSIGNMENTS", 9, "CBD5E1", True)
    s.text(54, 176, 550, 108, "From field updates\nto accountable action", 36, WHITE, True, valign="t")
    s.text(56, 302, 470, 66, "A human-reviewed coordination workspace for response records, team assignments, timelines, and operational reports.", 15, "CBD5E1", False, valign="t")
    s.rect(56, 405, 210, 42, RED, geometry="roundRect")
    s.text(56, 406, 210, 40, "STAKEHOLDER DESIGN BRIEF", 10, WHITE, True, "ctr")
    s.text(56, 493, 520, 20, "Concept and current local implementation  |  13 November 2026", 9, "94A3B8")
    s.add(650, 102, 280, 280, fill="1E293B", stroke="334155", geometry="roundRect")
    s.text(680, 126, 220, 32, "One reviewed picture", 18, WHITE, True)
    for i, (label, col) in enumerate(
        [("INCOMING REPORT", "FEE2E2"), ("REVIEWED RESPONSE", "DBEAFE"), ("TEAM ASSIGNMENT", "CCFBF1")]
    ):
        yy = 183 + i * 57
        s.rect(680, yy, 220, 42, col, geometry="roundRect")
        s.text(696, yy + 2, 190, 38, label, 10, NAVY, True)
        if i < 2:
            s.text(774, yy + 38, 32, 20, "↓", 15, WHITE, True, "ctr")
    s.text(680, 373, 220, 32, "Human approval stays in the loop.", 10, "CBD5E1", False, "ctr")
    slides.append(s)

    # 2. Need and outcome
    s = base_slide("Why CaseLoop?", "The operational need", 2)
    s.text(44, 120, 420, 28, "TODAY'S FRICTION", 10, MUTED, True)
    s.text(537, 120, 420, 28, "INTENDED OUTCOME", 10, MUTED, True)
    card(s, 44, 150, 265, 105, "Scattered updates", "Reports arrive in chats, calls, and notes with different levels of detail.", RED)
    card(s, 44, 270, 265, 105, "Unclear ownership", "It can be hard to see who accepted a task and when it changed.", AMBER)
    card(s, 44, 390, 265, 105, "Manual reporting", "Coordinators repeat data entry when preparing summaries.", BLUE)
    s.rect(347, 287, 146, 92, "FEE2E2", geometry="roundRect")
    s.text(357, 291, 126, 82, "REVIEW\nSTRUCTURE\nTRACE", 13, RED, True, "ctr")
    card(s, 537, 150, 420, 160, "A shared response register", "Approved field information is visible in one place. Responders can view, not delete or rewrite, published records.", TEAL)
    card(s, 537, 330, 420, 165, "A traceable coordination chain", "Assignments, status changes, actor, and event time feed the timeline and filtered report preview.", RED)
    slides.append(s)

    # 3. People and permissions
    s = base_slide("Design around roles and responsibility", "Users and access", 3)
    card(s, 44, 142, 288, 304, "Responder", "CAN\n- View approved response records\n- See team assignments\n- Update authorized assigned work\n\nCANNOT\n- Administer accounts or teams\n- Delete published responses", BLUE)
    card(s, 356, 142, 288, 304, "Coordinator", "CAN\n- Review and correct intake drafts\n- Approve and publish responses\n- Create linked team assignments\n- Preview and export reports\n\nAUDIT\n- Actions are attributed in timeline", TEAL)
    card(s, 668, 142, 288, 304, "Administrator", "CAN\n- Manage accounts and teams\n- Maintain response and assignment data\n- Review intake and timeline\n- Access reports and analysis\n\nGUARDRAIL\n- Public signup never grants admin", RED)
    s.rect(44, 466, 912, 42, "E2E8F0", geometry="roundRect")
    s.text(60, 469, 880, 36, "Principle: authority follows the task; the audit timeline records changes rather than acting as an editable workspace.", 12, NAVY, True, "ctr")
    slides.append(s)

    # 4. Workflow
    s = base_slide("One source-to-report workflow", "Service workflow", 4)
    steps = [
        ("01", "CAPTURE", "Manual or approved\nchannel report", RED),
        ("02", "REVIEW", "Keep source; correct\nand validate", AMBER),
        ("03", "PUBLISH", "Coordinator approves\nresponse record", TEAL),
        ("04", "ASSIGN", "Optionally link team,\nowner, and due date", BLUE),
        ("05", "AUDIT", "Append actor and\nevent time", NAVY),
        ("06", "REPORT", "Filter, preview,\nexport Word", "7C3AED"),
    ]
    x0 = 38
    gap = 14
    w = 145
    for i, (num, label, body, col) in enumerate(steps):
        x = x0 + i * (w + gap)
        s.add(x, 176, w, 185, fill=WHITE, stroke="E2E8F0", geometry="roundRect")
        s.add(x + 14, 192, 34, 34, fill=col, geometry="ellipse", text=num, size=10, color=WHITE, bold=True, align="ctr")
        s.text(x + 12, 240, w - 24, 25, label, 12, col, True)
        s.text(x + 12, 272, w - 24, 62, body, 10, MID, False, valign="t")
        if i < len(steps) - 1:
            s.text(x + w - 3, 244, gap + 10, 28, ">", 15, MUTED, True, "ctr")
    s.rect(82, 402, 836, 68, "FEF3C7", geometry="roundRect")
    s.text(104, 407, 792, 58, "Human review is the publication gate. Incoming WhatsApp content becomes a draft; it does not silently become an approved response or assignment.", 13, "78350F", True, "ctr")
    s.text(82, 483, 836, 28, "Branch labels such as KLB are explicit metadata for filters and reporting, not guesses from ambiguous text.", 10, MUTED, False, "ctr")
    slides.append(s)

    # 5. UI concepts
    s = base_slide("The interface: clear for each role", "UI design", 5)
    card(s, 44, 132, 285, 340, "01  Auth landing", "One clear dispatch action.\n\nSign in sits at the far right.\n\nAdministrator access remains available without competing with the main action.\n\nResponsive spacing is checked at desktop and phone widths.", RED)
    card(s, 357, 132, 285, 340, "02  Response register", "Published records are visibly read-only.\n\nBranch, team, and date filters aid retrieval.\n\nSource and approval context remain visible.\n\nNo destructive controls are shown to responders.", TEAL)
    card(s, 670, 132, 285, 340, "03  Admin cockpit", "Queues and assignments are actionable.\n\nPeople and team controls are role-gated.\n\nTimeline remains audit history.\n\nReport preview and export use the same filters.", BLUE)
    s.text(44, 490, 912, 24, "Editable SVG mockups are included beside this deck and can be imported into Figma.", 11, MUTED, True)
    slides.append(s)

    # 6. Architecture
    s = base_slide("Keep the stack; make deployment explicit", "Technical architecture", 6)
    card(s, 44, 136, 279, 268, "CURRENT LOCAL BASELINE", "React 18 + TypeScript\nVite frontend (separate dev server)\n\nFastAPI / Python 3.11\nDocker Compose API container\n\nPostgreSQL 16\nDocker container + named volume", BLUE)
    card(s, 361, 136, 279, 268, "TARGET OCI DEMO", "One Always Free eligible VM\nDocker Engine / Compose\n\nPython API + Docker Postgres\nReact production static service\nHTTPS reverse proxy\n\nSynthetic data only", TEAL)
    card(s, 678, 136, 279, 268, "REQUIRED BEFORE LIVE", "Validate ARM64 images/deps\nRestrict SSH and web ingress\nKeep port 5432 private\nStore secrets outside Git\nBack up and test restore\nMonitor free-tier use", RED)
    s.rect(44, 426, 913, 62, "E2E8F0", geometry="roundRect")
    s.text(60, 430, 880, 53, "Important: the existing Compose file has API and database services; React currently runs separately. Add a production frontend service or serve static assets through a controlled web server.", 11, NAVY, True, "ctr")
    slides.append(s)

    # 7. WhatsApp
    s = base_slide("WhatsApp intake: official, consent-based, reviewable", "Integration concept", 7)
    card(s, 44, 136, 204, 237, "MESSAGE", "A participant sends a text to the official business number or an eligible API-created group.", RED)
    card(s, 267, 136, 204, 237, "WEBHOOK", "Verify signature; deduplicate message ID; keep provider timestamp, source, and sender ID.", BLUE)
    card(s, 490, 136, 204, 237, "DRAFT", "Extract text and explicit branch tag such as KLB. Map sender identity to an authorized person.", AMBER)
    card(s, 713, 136, 244, 237, "COORDINATOR", "Correct and approve. Publish to register, optionally create assignment, and append audit event.", TEAL)
    s.rect(44, 401, 913, 90, "FEE2E2", geometry="roundRect")
    s.text(63, 408, 875, 72, "Groups API boundary: Official Business Account eligibility; invite-only API-created groups; maximum 8 participants. This is not a way to scrape arbitrary existing group history. CaseLoop group payload support is future work.", 12, "7F1D1D", True, "ctr")
    slides.append(s)

    # 8. Hosting and cost control
    s = base_slide("Oracle OCI: closest fit for a Compose-based free demo", "Hosting decision", 8)
    card(s, 44, 136, 430, 311, "WHAT FITS", "Always Free A1 currently lists 2 OCPU and 12 GB RAM, plus 200 GB of Always Free block storage in the home region.\n\nOne ARM64 VM can host Docker Compose for the API, PostgreSQL, and a production frontend/reverse proxy.\n\nCapacity is not guaranteed; validate ARM64 compatibility first.", TEAL)
    card(s, 495, 136, 462, 311, "BILLING GUARDRAILS", "Stay on Free Tier; use only resources labelled Always Free; do not upgrade for this demo.\n\nSet quotas and budget alerts, but remember budgets are soft alerts, not hard billing caps.\n\nIdle free compute may be reclaimed. Keep off-VM backups and treat the demo as disposable.", RED)
    s.text(48, 472, 900, 32, "No provider setting is a guaranteed zero-spend lock after enabling billable resources.", 12, NAVY, True, "ctr")
    s.text(48, 503, 900, 20, "Official limits can change; check the OCI Free Tier and budget documentation before provisioning.", 9, MUTED, False, "ctr")
    slides.append(s)

    # 9. Document plan
    s = base_slide("Design documents make the goal reviewable", "System analysis and design", 9)
    docs = [
        ("BRIEF", "Problem, scope,\nusers, outcomes"),
        ("REQUIREMENTS", "Use cases and\nacceptance tests"),
        ("DIAGRAMS", "Workflow, context,\nERD, sequence"),
        ("SAFEGUARDS", "Roles, privacy,\nretention, risks"),
        ("RUNBOOK", "OCI steps, backup,\nrestore, rollback"),
        ("USER GUIDE", "Coordinator and\nresponder tasks"),
    ]
    for i, (label, desc) in enumerate(docs):
        x = 43 + i * 153
        s.add(x, 170, 140, 122, fill=WHITE, stroke="E2E8F0", geometry="roundRect")
        s.text(x + 8, 185, 124, 26, label, 10, RED if i % 2 == 0 else TEAL, True, "ctr")
        s.text(x + 12, 220, 116, 55, desc, 10, MID, False, "ctr")
    s.rect(43, 329, 872, 96, "E0F2FE", geometry="roundRect")
    s.text(64, 337, 830, 80, "Recommended order: validate the workflow and permissions first; confirm the data model and privacy rules; document the deployment; then test a synthetic end-to-end scenario before enabling any external integration.", 13, "0C4A6E", True, "ctr")
    s.text(44, 455, 910, 42, "The design pack includes an item checklist, documentation plan, architecture diagram, workflow diagram, and editable screen mockups.", 11, MUTED, True, "ctr")
    slides.append(s)

    # 10. Learning roadmap and close
    s = base_slide("Build confidence by owning one small change at a time", "Learning and next steps", 10)
    card(s, 44, 136, 286, 286, "WEEK 1  |  GIT + UI", "Read the diff and status.\nTrace one React form.\nMake one safe visual change.\nCheck desktop and mobile.", RED)
    card(s, 357, 136, 286, 286, "WEEK 2  |  API + DATA", "Trace UI -> API -> model -> database.\nRead one endpoint and its test.\nUse synthetic rows.\nWrite one focused test.", BLUE)
    card(s, 670, 136, 286, 286, "WEEK 3  |  OPERATE", "Read Compose logs and health.\nPractice backup and restore.\nReview OCI free-only controls.\nDeploy only after checklist.", TEAL)
    s.rect(44, 447, 913, 52, NAVY, geometry="roundRect")
    s.text(60, 450, 880, 46, "Next decision: approve the diagrams and scope, then build the OCI synthetic demo before starting WhatsApp integration.", 12, WHITE, True, "ctr")
    slides.append(s)

    return slides


def slide_xml(slide: Slide) -> str:
    return slide.xml()


def content_types(slide_count: int) -> str:
    overrides = [
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    overrides.extend(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, slide_count + 1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        + "".join(overrides)
        + "</Types>"
    )


def relationships(items: list[tuple[str, str, str]]) -> str:
    rels = "".join(
        f'<Relationship Id="{rid}" Type="{kind}" Target="{target}"/>'
        for rid, kind, target in items
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + rels
        + "</Relationships>"
    )


def presentation_xml(slide_count: int) -> str:
    ids = "".join(
        f'<p:sldId id="{255 + i}" r:id="rId{i + 1}"/>'
        for i in range(1, slide_count + 1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        f"<p:sldIdLst>{ids}</p:sldIdLst>"
        f'<p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="wide"/>'
        '<p:notesSz cx="6858000" cy="9144000"/>'
        "<p:defaultTextStyle><a:defPPr><a:defRPr lang=\"en-US\"/></a:defPPr></p:defaultTextStyle>"
        "</p:presentation>"
    )


def theme_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="CaseLoop">'
        "<a:themeElements>"
        '<a:clrScheme name="CaseLoop">'
        '<a:dk1><a:srgbClr val="0F172A"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>'
        '<a:dk2><a:srgbClr val="334155"/></a:dk2><a:lt2><a:srgbClr val="F8FAFC"/></a:lt2>'
        '<a:accent1><a:srgbClr val="C62828"/></a:accent1><a:accent2><a:srgbClr val="0F766E"/></a:accent2>'
        '<a:accent3><a:srgbClr val="2563EB"/></a:accent3><a:accent4><a:srgbClr val="B45309"/></a:accent4>'
        '<a:accent5><a:srgbClr val="7C3AED"/></a:accent5><a:accent6><a:srgbClr val="64748B"/></a:accent6>'
        '<a:hlink><a:srgbClr val="2563EB"/></a:hlink><a:folHlink><a:srgbClr val="7C3AED"/></a:folHlink>'
        "</a:clrScheme>"
        '<a:fontScheme name="CaseLoop"><a:majorFont><a:latin typeface="Aptos Display"/></a:majorFont>'
        '<a:minorFont><a:latin typeface="Aptos"/></a:minorFont></a:fontScheme>'
        '<a:fmtScheme name="CaseLoop">'
        '<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:gradFill rotWithShape="1"><a:gsLst><a:gs pos="0"><a:schemeClr val="phClr"/></a:gs><a:gs pos="100000"><a:schemeClr val="phClr"/></a:gs></a:gsLst><a:lin ang="0" scaled="1"/></a:gradFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
        '<a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
        '<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>'
        '<a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
        '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
        '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="lt1"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="lt2"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>'
        "</a:fmtScheme></a:themeElements></a:theme>"
    )


def master_xml() -> str:
    tree = (
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/>'
        "<p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>"
        "<p:grpSpPr><a:xfrm><a:off x=\"0\" y=\"0\"/><a:ext cx=\"0\" cy=\"0\"/>"
        "<a:chOff x=\"0\" y=\"0\"/><a:chExt cx=\"0\" cy=\"0\"/></a:xfrm></p:grpSpPr>"
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        f"<p:cSld><p:spTree>{tree}</p:spTree></p:cSld>"
        '<p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/>'
        '<p:sldLayoutIdLst><p:sldLayoutId id="1" r:id="rId1"/></p:sldLayoutIdLst>'
        "<p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>"
        "</p:sldMaster>"
    )


def layout_xml() -> str:
    tree = (
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/>'
        "<p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>"
        "<p:grpSpPr><a:xfrm><a:off x=\"0\" y=\"0\"/><a:ext cx=\"0\" cy=\"0\"/>"
        "<a:chOff x=\"0\" y=\"0\"/><a:chExt cx=\"0\" cy=\"0\"/></a:xfrm></p:grpSpPr>"
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">'
        f'<p:cSld name="Blank"><p:spTree>{tree}</p:spTree></p:cSld>'
        "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>"
    )


def create_package(slides: list[Slide]) -> None:
    root_rels = relationships(
        [
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument", "ppt/presentation.xml"),
            ("rId2", "http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties", "docProps/core.xml"),
            ("rId3", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties", "docProps/app.xml"),
        ]
    )
    presentation_rels = [("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "slideMasters/slideMaster1.xml")]
    presentation_rels.extend(
        (f"rId{i + 1}", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide", f"slides/slide{i}.xml")
        for i in range(1, len(slides) + 1)
    )
    presentation_rels_xml = relationships(presentation_rels)
    layout_rels_xml = relationships(
        [("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "../slideMasters/slideMaster1.xml")]
    )
    master_rels_xml = relationships(
        [
            ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
            ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme", "../theme/theme1.xml"),
        ]
    )
    slide_rels_xml = relationships(
        [("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml")]
    )
    core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        "<dc:title>CaseLoop Stakeholder Design Brief</dc:title>"
        "<dc:subject>Human-reviewed operations coordination concept</dc:subject>"
        "<dc:creator>CaseLoop Project</dc:creator>"
        "</cp:coreProperties>"
    )
    app = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Application>CaseLoop design pack</Application>"
        f"<Slides>{len(slides)}</Slides><Company>CaseLoop Project</Company>"
        "</Properties>"
    )
    with ZipFile(OUT, "w", ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", content_types(len(slides)))
        package.writestr("_rels/.rels", root_rels)
        package.writestr("docProps/core.xml", core)
        package.writestr("docProps/app.xml", app)
        package.writestr("ppt/presentation.xml", presentation_xml(len(slides)))
        package.writestr("ppt/_rels/presentation.xml.rels", presentation_rels_xml)
        package.writestr("ppt/slideMasters/slideMaster1.xml", master_xml())
        package.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", master_rels_xml)
        package.writestr("ppt/slideLayouts/slideLayout1.xml", layout_xml())
        package.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", layout_rels_xml)
        package.writestr("ppt/theme/theme1.xml", theme_xml())
        for i, slide in enumerate(slides, start=1):
            package.writestr(f"ppt/slides/slide{i}.xml", slide_xml(slide))
            package.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels_xml)


if __name__ == "__main__":
    deck = make_deck()
    create_package(deck)
    print(f"Created {OUT} with {len(deck)} editable slides.")
