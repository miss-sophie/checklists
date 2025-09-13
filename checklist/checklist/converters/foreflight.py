"""
ForeFlight .fmd import/export utilities
"""
import json
import os
import uuid
from pathlib import Path
import yaml
from Crypto.Cipher import AES

AES_KEY = b'81e06e41a93f3848'
AES_BLOCK_SIZE = AES.block_size
FOREFLIGHT_CONTAINER_TYPE = 'checklist'
PAYLOAD_FIELD = 'payload'
DETAIL_ITEM_TYPE = 'comment'
SCHEMA_VERSION_DEFAULT = '1.0'

def pad_bytes(data: bytes) -> bytes:
    padding_length = AES_BLOCK_SIZE - (len(data) % AES_BLOCK_SIZE)
    return data + bytes([padding_length] * padding_length)

def unpad_bytes(padded_data: bytes) -> bytes:
    padding_length = padded_data[-1]
    return padded_data[:-padding_length]

def convert_yaml_to_payload(source_yaml: dict) -> dict:
    payload = {
        'metadata': {
            'name':          source_yaml.get('checklist_name', ''),
            'tailNumber':    source_yaml.get('tailNumber', ''),
            'detail':   source_yaml.get('detail', ''),
            'schemaVersion': source_yaml.get('schemaVersion', SCHEMA_VERSION_DEFAULT)
        },
        'objectId':      uuid.uuid4().hex,
        'groups':        [],
        'schemaVersion': source_yaml.get('schemaVersion', SCHEMA_VERSION_DEFAULT)
    }
    for category in source_yaml.get('categories', []):
        category_entry = {
            'groupType': category.get('name', '').lower(),
            'items':     [],
            'objectId':  uuid.uuid4().hex
        }
        for subgroup in category.get('groups', []):
            subgroup_entry = {
                'title':    subgroup.get('name', ''),
                'items':    [],
                'objectId': uuid.uuid4().hex
            }
            for checklist in subgroup.get('checklists', []):
                checklist_entry = {
                    'title':    checklist.get('name', ''),
                    'items':    [],
                    'objectId': uuid.uuid4().hex
                }
                for step in checklist.get('items', []):
                    step_entry = {
                        'title':    step.get('text', ''),
                        'detail':   step.get('detail', ''),
                        'objectId': uuid.uuid4().hex
                    }
                    if step.get('type') == 'detail':
                        step_entry['type'] = DETAIL_ITEM_TYPE
                    note_text = step.get('note')
                    if note_text:
                        step_entry['note'] = note_text
                    checklist_entry['items'].append(step_entry)
                subgroup_entry['items'].append(checklist_entry)
            category_entry['items'].append(subgroup_entry)
        payload['groups'].append(category_entry)
    return payload

def convert_payload_to_yaml(payload_json: dict) -> dict:
    output_yaml = {
        'checklist_name': payload_json.get('metadata', {}).get('name', ''),
        'tailNumber':     payload_json.get('metadata', {}).get('tailNumber', ''),
        'detail':    payload_json.get('metadata', {}).get('detail', ''),
        'schemaVersion':  payload_json.get('schemaVersion', SCHEMA_VERSION_DEFAULT),
        'categories':     []
    }
    for category_entry in payload_json.get('groups', []):
        category_yaml = {
            'name':   category_entry.get('groupType', '').capitalize(),
            'groups': []
        }
        for subgroup_entry in category_entry.get('items', []):
            subgroup_yaml = {
                'name':       subgroup_entry.get('title', ''),
                'checklists': []
            }
            for checklist_entry in subgroup_entry.get('items', []):
                checklist_yaml = {
                    'name': checklist_entry.get('title', ''),
                    'items': []
                }
                for step_entry in checklist_entry.get('items', []):
                    item_yaml = { 'text': step_entry.get('title', '') }
                    detail_text = step_entry.get('detail', '')
                    if detail_text:
                        item_yaml['detail'] = detail_text
                    if step_entry.get('type') == DETAIL_ITEM_TYPE:
                        item_yaml['type'] = 'detail'
                    else:
                        item_yaml['type'] = 'check'
                    if step_entry.get('note'):
                        item_yaml['note'] = step_entry.get('note')
                    checklist_yaml['items'].append(item_yaml)
                subgroup_yaml['checklists'].append(checklist_yaml)
            category_yaml['groups'].append(subgroup_yaml)
        output_yaml['categories'].append(category_yaml)
    return output_yaml

def encrypt_fmd_container(payload_json: dict) -> bytes:
    container_dict = {
        'type': FOREFLIGHT_CONTAINER_TYPE,
        PAYLOAD_FIELD: payload_json
    }
    raw_json = json.dumps(container_dict, separators=(',',':')).encode('utf-8')
    padded  = pad_bytes(raw_json)
    iv      = os.urandom(AES_BLOCK_SIZE)
    cipher  = AES.new(AES_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded)
    return iv + ciphertext

def decrypt_fmd_container(fmd_blob: bytes) -> dict:
    iv         = fmd_blob[:AES_BLOCK_SIZE]
    ciphertext = fmd_blob[AES_BLOCK_SIZE:]
    cipher     = AES.new(AES_KEY, AES.MODE_CBC, iv)
    padded     = cipher.decrypt(ciphertext)
    raw_json   = unpad_bytes(padded)
    container = json.loads(raw_json.decode('utf-8'))
    return container.get(PAYLOAD_FIELD, {})

def load_yaml_file(path: Path) -> dict:
    content = path.read_text(encoding='utf-8')
    return yaml.safe_load(content)

def save_yaml_file(data: dict, path: Path) -> None:
    yaml_str = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    path.write_text(yaml_str, encoding='utf-8')

def load_fmd_file(path: Path) -> dict:
    blob = path.read_bytes()
    return decrypt_fmd_container(blob)

def save_fmd_file(payload_json: dict, path: Path) -> None:
    blob = encrypt_fmd_container(payload_json)
    path.write_bytes(blob)

def export_yaml_to_fmd(yaml_path: Path, fmd_path: Path) -> None:
    source_yaml = load_yaml_file(yaml_path)
    payload_json = convert_yaml_to_payload(source_yaml)
    save_fmd_file(payload_json, fmd_path)

def import_fmd_to_yaml(fmd_path: Path, yaml_path: Path) -> None:
    payload_json = load_fmd_file(fmd_path)
    output_yaml = convert_payload_to_yaml(payload_json)
    save_yaml_file(output_yaml, yaml_path)