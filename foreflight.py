#!/usr/bin/env python3
"""
Tool: to_foreflight.py
Purpose: Convert between ForeFlight encrypted .fmd checklist files and a human-editable YAML format.
Outputs:
  - Import: FMD → YAML
  - Export: YAML → FMD

Requirements:
  - Python 3.8+
  - pyyaml
  - pycryptodome
"""
import argparse
import json
import os
import uuid
from pathlib import Path

import yaml
from Crypto.Cipher import AES


# === Constants ===
AES_KEY = b'81e06e41a93f3848'        # 16-byte AES key (ASCII)
AES_BLOCK_SIZE = AES.block_size       # Block size (16 bytes)
FOREFLIGHT_CONTAINER_TYPE = 'checklist'
PAYLOAD_FIELD = 'payload'            # JSON field for payload inside container
DETAIL_ITEM_TYPE = 'comment'         # ForeFlight uses 'comment' for detail items
SCHEMA_VERSION_DEFAULT = '1.0'


# === PKCS7 Padding Functions ===
def pad_bytes(data: bytes) -> bytes:
    """
    Apply PKCS7 padding to align data length to AES_BLOCK_SIZE.
    """
    padding_length = AES_BLOCK_SIZE - (len(data) % AES_BLOCK_SIZE)
    return data + bytes([padding_length] * padding_length)


def unpad_bytes(padded_data: bytes) -> bytes:
    """
    Remove PKCS7 padding.
    """
    padding_length = padded_data[-1]
    return padded_data[:-padding_length]


# === YAML → ForeFlight JSON Payload ===
def convert_yaml_to_payload(source_yaml: dict) -> dict:
    """
    Translate the source YAML structure into the ForeFlight JSON payload.
    This payload will be encrypted and wrapped before writing .fmd.
    """
    # Build top-level metadata section
    payload = {
        'metadata': {
            'name':          source_yaml.get('checklist_name', ''),
            'tailNumber':    source_yaml.get('tailNumber', ''),
            'description':   source_yaml.get('description', ''),
            'schemaVersion': source_yaml.get('schemaVersion', SCHEMA_VERSION_DEFAULT)
        },
        'objectId':      uuid.uuid4().hex,
        'groups':        [],
        'schemaVersion': source_yaml.get('schemaVersion', SCHEMA_VERSION_DEFAULT)
    }

    # Iterate categories
    for category in source_yaml.get('categories', []):
        category_entry = {
            'groupType': category.get('name', '').lower(),
            'items':     [],
            'objectId':  uuid.uuid4().hex
        }

        # Iterate subgroups within category
        for subgroup in category.get('groups', []):
            subgroup_entry = {
                'title':    subgroup.get('name', ''),
                'items':    [],
                'objectId': uuid.uuid4().hex
            }

            # Iterate checklists within subgroup
            for checklist in subgroup.get('checklists', []):
                checklist_entry = {
                    'title':    checklist.get('name', ''),
                    'items':    [],
                    'objectId': uuid.uuid4().hex
                }

                # Iterate steps within checklist
                for step in checklist.get('items', []):
                    step_entry = {
                        'title':    step.get('text', ''),
                        'detail':   step.get('detail', ''),
                        'objectId': uuid.uuid4().hex
                    }
                    # Mark detail/check type
                    if step.get('type') == 'detail':
                        step_entry['type'] = DETAIL_ITEM_TYPE

                    # Optional note field
                    note_text = step.get('note')
                    if note_text:
                        step_entry['note'] = note_text

                    checklist_entry['items'].append(step_entry)

                subgroup_entry['items'].append(checklist_entry)

            category_entry['items'].append(subgroup_entry)

        payload['groups'].append(category_entry)

    return payload


# === ForeFlight JSON Payload → YAML ===
def convert_payload_to_yaml(payload_json: dict) -> dict:
    """
    Translate the decrypted ForeFlight JSON payload into the editable YAML structure.
    """
    output_yaml = {
        'checklist_name': payload_json.get('metadata', {}).get('name', ''),
        'tailNumber':     payload_json.get('metadata', {}).get('tailNumber', ''),
        'description':    payload_json.get('metadata', {}).get('detail', ''),
        'schemaVersion':  payload_json.get('schemaVersion', SCHEMA_VERSION_DEFAULT),
        'categories':     []
    }

    # Iterate categories
    for category_entry in payload_json.get('groups', []):
        category_yaml = {
            'name':   category_entry.get('groupType', '').capitalize(),
            'groups': []
        }

        # Iterate subgroups
        for subgroup_entry in category_entry.get('items', []):
            subgroup_yaml = {
                'name':       subgroup_entry.get('title', ''),
                'checklists': []
            }

            # Iterate checklists
            for checklist_entry in subgroup_entry.get('items', []):
                checklist_yaml = {
                    'name': checklist_entry.get('title', ''),
                    'items': []
                }

                # Iterate steps
                for step_entry in checklist_entry.get('items', []):
                    item_yaml = { 'text': step_entry.get('title', '') }

                    # Include detail if present
                    detail_text = step_entry.get('detail', '')
                    if detail_text:
                        item_yaml['detail'] = detail_text

                    # Determine item type
                    if step_entry.get('type') == DETAIL_ITEM_TYPE:
                        item_yaml['type'] = 'detail'
                    else:
                        item_yaml['type'] = 'check'

                    # Include note if present
                    if step_entry.get('note'):
                        item_yaml['note'] = step_entry.get('note')

                    checklist_yaml['items'].append(item_yaml)

                subgroup_yaml['checklists'].append(checklist_yaml)

            category_yaml['groups'].append(subgroup_yaml)

        output_yaml['categories'].append(category_yaml)

    return output_yaml


# === Encryption / Decryption of .fmd Container ===
def encrypt_fmd_container(payload_json: dict) -> bytes:
    """
    Wrap the JSON payload in a container and encrypt to produce a .fmd blob.
    """
    container_dict = {
        'type':       FOREFLIGHT_CONTAINER_TYPE,
        PAYLOAD_FIELD: payload_json
    }
    raw_json = json.dumps(container_dict, separators=(',',':')).encode('utf-8')
    padded  = pad_bytes(raw_json)
    iv      = os.urandom(AES_BLOCK_SIZE)
    cipher  = AES.new(AES_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded)
    return iv + ciphertext


def decrypt_fmd_container(fmd_blob: bytes) -> dict:
    """
    Decrypt a .fmd blob and return the inner JSON payload.
    """
    iv         = fmd_blob[:AES_BLOCK_SIZE]
    ciphertext = fmd_blob[AES_BLOCK_SIZE:]
    cipher     = AES.new(AES_KEY, AES.MODE_CBC, iv)
    padded     = cipher.decrypt(ciphertext)
    raw_json   = unpad_bytes(padded)
    container = json.loads(raw_json.decode('utf-8'))
    return container.get(PAYLOAD_FIELD, {})


# === File I/O Utilities ===
def load_yaml_file(path: Path) -> dict:
    """
    Read YAML from file and parse into dictionary.
    """
    content = path.read_text(encoding='utf-8')
    return yaml.safe_load(content)


def save_yaml_file(data: dict, path: Path) -> None:
    """
    Dump dictionary to YAML file with UTF-8 encoding and unicode support.
    """
    yaml_str = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    path.write_text(yaml_str, encoding='utf-8')


def load_fmd_file(path: Path) -> dict:
    """
    Load and decrypt a .fmd file, returning the checklist JSON payload.
    """
    blob = path.read_bytes()
    return decrypt_fmd_container(blob)


def save_fmd_file(payload_json: dict, path: Path) -> None:
    """
    Encrypt and write payload JSON as a .fmd file.
    """
    blob = encrypt_fmd_container(payload_json)
    path.write_bytes(blob)


# === Conversion Wrappers ===
def export_yaml_to_fmd(yaml_path: Path, fmd_path: Path) -> None:
    """
    Read YAML, convert to payload JSON, then save as .fmd.
    """
    source_yaml = load_yaml_file(yaml_path)
    payload_json = convert_yaml_to_payload(source_yaml)
    save_fmd_file(payload_json, fmd_path)


def import_fmd_to_yaml(fmd_path: Path, yaml_path: Path) -> None:
    """
    Read .fmd, decrypt payload JSON, then save as YAML.
    """
    payload_json = load_fmd_file(fmd_path)
    output_yaml = convert_payload_to_yaml(payload_json)
    save_yaml_file(output_yaml, yaml_path)


# === Command-Line Interface ===
def main():
    parser = argparse.ArgumentParser(
        description='Convert between ForeFlight .fmd and YAML checklist formats.'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Import subcommand: FMD -> YAML
    import_parser = subparsers.add_parser('import', help='Import .fmd to YAML')
    import_parser.add_argument('fmd',  type=Path, help='Input .fmd file path')
    import_parser.add_argument('yaml', type=Path, help='Output YAML file path')

    # Export subcommand: YAML -> FMD
    export_parser = subparsers.add_parser('export', help='Export YAML to .fmd')
    export_parser.add_argument('yaml', type=Path, help='Input YAML file path')
    export_parser.add_argument('fmd',  type=Path, help='Output .fmd file path')

    args = parser.parse_args()
    if args.command == 'import':
        import_fmd_to_yaml(args.fmd, args.yaml)
    else:
        export_yaml_to_fmd(args.yaml, args.fmd)


if __name__ == '__main__':
    main()
