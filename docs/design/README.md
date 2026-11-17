# CaseLoop design pack

This pack is for both academic attachment review and operational stakeholders. It separates the **current local implementation** from **proposed work**; the mockups are concepts, not screenshots or claims that unfinished features are already live.

## Deliverables

- `CaseLoop_Stakeholder_Design_Brief.pptx` — editable stakeholder presentation.
- `mockups/` — SVG screen concepts that can be imported into Figma; open `mockups/preview.html` to review them in a browser.
- `architecture.mmd` and `workflow.mmd` — editable Mermaid diagrams.
- `checklist.md` — implementation and deployment readiness checklist.
- `documentation-plan.md` — recommended system analysis/design document set.
- `build_presentation.py` — standard-library generator for the PowerPoint.

## Visual and data conventions

- Red, slate, white, and teal are used as a neutral CaseLoop palette; no protected Red Cross emblem is reproduced.
- UI and report examples use synthetic data.
- Response publication is human-reviewed. The response register and audit timeline are not general-purpose delete/edit areas.
- WhatsApp Groups API, Oracle Cloud deployment, and the production React serving container are future work unless explicitly marked otherwise.

## Rebuild the deck

From the repository root:

```powershell
python docs/design/build_presentation.py
```

The script writes the `.pptx` beside itself and requires only Python's standard library.
