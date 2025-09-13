# YAML Checklist Structure Specification

This document defines the structure of the YAML file format used as the single source of truth for aircraft checklists. The YAML file is designed to be:

- **Human-editable**: Suitable for authors, maintainers, and reviewers.
- **Machine-readable**: Parsed by the `to_foreflight.py` script to generate ForeFlight-compatible `.fmd` files.
- **Printable**: Serves as the input for LaTeX rendering to produce PDF versions for cockpit or training use.

The checklist YAML schema reflects the operational structure found in professional aviation checklists and supports both normal and non-normal procedures.

Each YAML file contains a complete hierarchy of:

1. Aircraft metadata (title, tail number, version)
2. Operational categories (Normal, Abnormal, Emergency)
3. Subgroups (e.g. Preflight, In Flight)
4. Checklists (named sequences of items)
5. Individual checklist items (challenge-response steps or informational notes)

This format ensures synchronization across digital and printed checklists and supports structured extensions for training and operational auditing.

All fields and nesting levels are described in detail below.


```yaml
# ──────────────────────────────────────────────────────────────────────────────
# Top-level (required)
# ──────────────────────────────────────────────────────────────────────────────
checklist_name:  string       # Title of the checklist set
tailNumber:      string       # Aircraft registration (e.g. D-ERFH)
detail:     string       # Free-text description (can be empty)
schemaVersion:   "1.0"        # Must be "1.0"
categories:      [ … ]        # List of category objects
# ──────────────────────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────────────────────
# categories (array of objects)
# ──────────────────────────────────────────────────────────────────────────────
categories:
  - name:     string         # "Normal", "Abnormal" or "Emergency"
    groups:   [ … ]          # List of sub-group objects
# ──────────────────────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────────────────────
# groups (within each category)
# ──────────────────────────────────────────────────────────────────────────────
groups:
  - name:       string       # Subgroup heading, e.g. "Preflight", "Before Start"
    checklists: [ … ]        # List of checklist objects
# ──────────────────────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────────────────────
# checklists (within each subgroup)
# ──────────────────────────────────────────────────────────────────────────────
checklists:
  - name:  string            # Checklist title, e.g. "Exterior", "Engine Start"
    items: [ … ]             # List of step/item objects
# ──────────────────────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────────────────────
# items (within each checklist)
# ──────────────────────────────────────────────────────────────────────────────
items:
  - text:   string           # Challenge prompt (required)
    detail: string           # Inline detail/setting (optional; omit or "" if none)
    type:   "check"|"detail" # "check" for checkbox; "detail" for info-only
    note:   string           # Longer hint or popup note (optional)
# ──────────────────────────────────────────────────────────────────────────────
```

### Minimal example

```yaml
checklist_name: "Cessna 172S Procedures"
tailNumber:     "D-MEOW"
description:    "Normal & Emergency"
schemaVersion:  "1.0"
categories:
  - name: "Normal"
    groups:
      - name: "Preflight"
        checklists:
          - name: "Exterior"
            items:
              - text:   "Fuel Quantity"
                detail: "Sufficient — Right Tank"
                type:   "check"
                note:   "Verify against logbook"
              - text:   "Oil Quantity"
                detail: "1–2 qt"
                type:   "check"
              - text:   "Propeller"
                type:   "detail"
      - name: "Before Start"
        checklists:
          - name: "Cabin Check"
            items:
              - text:   "Seats & Belts"
                detail: "Locked"
                type:   "check"
              - text:   "Avionics Master"
                detail: "Off"
                type:   "check"

  - name: "Emergency"
    groups:
      - name: "Engine Failure"
        checklists:
          - name: "In Flight"
            items:
              - text: "Fuel Selector"
                detail: "Off"
                type: "check"
              - text: "Mixture"
                detail: "Cut Off"
                type: "check"
```

> **Note:**
>
> * **Order matters**: fields must appear exactly as above.
> * **Omit** optional keys (`detail`, `note`) if unused.
> * **`type`** must be either `"check"` or `"detail"`.
> * **`schemaVersion`** must read `"1.0"` for compatibility.
