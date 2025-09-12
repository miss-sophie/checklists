## ForeFlight `.fmd` File Format Specification

### 1. Binary File Layout

An `.fmd` file is a binary blob composed of:

```
┌───────────────────┬───────────────────────────────┐
│ 16-byte IV (hex)  │ N-byte ciphertext (hex)       │
└───────────────────┴───────────────────────────────┘
```

1. **Initialization Vector (IV)**

   * Length: 16 bytes
   * Purpose: Random per-file seed for AES-CBC
   * Location: First 16 bytes of the file

2. **Ciphertext**

   * Length: `file_size − 16`
   * Contains AES-CBC encryption of a PKCS#7-padded JSON container (see below)

### 2. Encryption Parameters

* **Algorithm**: AES-128 in CBC mode
* **Key**: ASCII string `81e06e41a93f3848` (16 bytes, fixed)
* **Padding**: PKCS#7 to a multiple of 16 bytes
* **IV Generation**: `os.urandom(16)`

Encryption steps (export path):

1. Serialize JSON container → UTF-8 bytes
2. Apply PKCS#7 padding
3. Prepend 16-byte IV
4. Encrypt padded bytes with AES-CBC(key, iv) → ciphertext

Decryption (import path) is the reverse.

### 3. JSON Container (Pre-Encryption)

Before encryption, the file payload is a **compact JSON** object:

```jsonc
{
  "type": "checklist",
  "payload": { … }
}
```

* **type**: Always `"checklist"`
* **payload**: The actual checklist data model (see §4)
* **Serialization options**: `json.dumps(obj, separators=(",",":"))` (no extra whitespace)

### 4. Checklist Data Model (`payload`)

The `payload` object follows a 4-level hierarchical schema:

```jsonc
{
  "metadata": { … },
  "objectId": "<32-char hex UUID>",
  "schemaVersion": "1.0",
  "groups": [ … ]
}
```

#### 4.1. `metadata` (object)

| Field           | Type   | Description                         |
| --------------- | ------ | ----------------------------------- |
| `name`          | string | Checklist set title                 |
| `tailNumber`    | string | Aircraft tail number (registration) |
| `description`   | string | (Optional) free-text description    |
| `schemaVersion` | string | Must be `"1.0"`                     |

#### 4.2. `objectId` (string)

* A 32-character lowercase hex UUID (no dashes).
* Used internally for sync/tracking.

#### 4.3. `schemaVersion` (string)

* Mirrors `metadata.schemaVersion`, currently `"1.0"`
* May be used by ForeFlight to version checks.

#### 4.4. `groups` (array)

An array of **categories**. Each element:

```jsonc
{
  "groupType": "normal" | "abnormal" | "emergency",
  "objectId":  "<uuid>",
  "items":     [ … ]    // subgroups
}
```

* **groupType**: Lowercase category name
* **items**: Array of **subgroups** (see §4.5)

#### 4.5. Subgroup Entries (`groups[].items`)

Each subgroup represents a heading within a category:

```jsonc
{
  "title":    "<subgroup name>",
  "objectId": "<uuid>",
  "items":    [ … ]  // checklists under this subgroup
}
```

* **title**: The name displayed in ForeFlight (e.g. “Preflight”, “Cabin Check”)

#### 4.6. Checklist Entries (`subgroup.items`)

Each checklist is a named list of steps:

```jsonc
{
  "title":    "<checklist name>",
  "objectId": "<uuid>",
  "items":    [ … ]  // step entries
}
```

* **title**: The checklist’s name within its subgroup

#### 4.7. Step Entries (`checklist.items`)

Each step is a challenge-response or detail item:

```jsonc
{
  "title":  "<challenge text>",
  "detail": "<inline detail text>",    // optional, may be empty string
  "type":   "comment" | <absent>,      // `'comment'` for detail-only items
  "note":   "<hint or note text>"      // optional
}
```

* **title**: The main prompt or challenge
* **detail**: Supplemental inline info (often shown to the right of title)
* **type**:

  * If **absent** (or any value other than `"comment"`), treated as a **check** item
  * If `"comment"`, treated as an **info-only / detail** item (no checkbox)
* **note**: A longer hint or explanatory note, shown in ForeFlight’s UI as a popup

### 5. Summary of Hierarchy

```text
payload
├─ metadata
│   ├─ name
│   ├─ tailNumber
│   ├─ description
│   └─ schemaVersion
├─ objectId
├─ schemaVersion
└─ groups [    ← categories (Normal/Abnormal/Emergency)
    ├─ groupType
    ├─ objectId
    └─ items [ ← subgroups
        ├─ title
        ├─ objectId
        └─ items [ ← checklists
            ├─ title
            ├─ objectId
            └─ items [ ← steps
                ├─ title
                ├─ detail
                ├─ type
                └─ note
            ]
        ]
    ]
]
```

### 6. Example (Pre-Encryption)

```json

{"type":"checklist","payload":{
  "metadata":{"name":"TEST","tailNumber":"D-ERFH","description":"","schemaVersion":"1.0"},
  "objectId":"a1b2c3d4e5f60718293a4b5c6d7e8f90",
  "schemaVersion":"1.0",
  "groups":[
    {
      "groupType":"normal",
      "objectId":"11111111111111111111111111111111",
      "items":[
        {
          "title":"Preflight",
          "objectId":"22222222222222222222222222222222",
          "items":[
            {
              "title":"Fuel Quantity",
              "detail":"CHECK SUFFICIENT",
              "objectId":"33333333333333333333333333333333",
              "items":[
                {
                  "title":"Left Tank",
                  "detail":"",
                  "type":"comment",
                  "note":"Verify gauge reading matches logbook"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}}
```

Finally, that JSON is padded and encrypted as described in §1–§2 to produce the `.fmd` file that ForeFlight consumes.
