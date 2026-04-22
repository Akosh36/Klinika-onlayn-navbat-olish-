#!/usr/bin/env python
"""
Simple translation compiler that creates valid .mo files from .po files
"""

import os
import struct

def parse_po_file(po_content):
    """Parse a .po file and extract msgid/msgstr pairs"""
    messages = {}
    lines = po_content.strip().split('\n')
    
    current_msgid = None
    current_msgstr = None
    in_msgid = False
    in_msgstr = False
    
    for line in lines:
        line = line.rstrip()
        
        if line.startswith('#'):
            continue
        elif line.startswith('msgid'):
            in_msgid = True
            in_msgstr = False
            # Extract the string value
            match = line[6:].strip()
            if match.startswith('"') and match.endswith('"'):
                current_msgid = match[1:-1]
            else:
                current_msgid = ""
        elif line.startswith('msgstr'):
            in_msgstr = True
            in_msgid = False
            # Extract the string value
            match = line[7:].strip()
            if match.startswith('"') and match.endswith('"'):
                current_msgstr = match[1:-1]
            else:
                current_msgstr = ""
        elif in_msgid and line.startswith('"'):
            # Continuation of msgid
            if line.endswith('"'):
                current_msgid += line[1:-1]
            else:
                current_msgid += line[1:]
        elif in_msgstr and line.startswith('"'):
            # Continuation of msgstr
            if line.endswith('"'):
                current_msgstr += line[1:-1]
            else:
                current_msgstr += line[1:]
        elif line == "" and current_msgid is not None and current_msgstr is not None:
            # End of entry
            if current_msgid:  # Skip empty msgid (header)
                messages[current_msgid] = current_msgstr
            current_msgid = None
            current_msgstr = None
    
    # Handle last entry
    if current_msgid is not None and current_msgstr is not None and current_msgid:
        messages[current_msgid] = current_msgstr
    
    return messages

def generate_mo_data(messages):
    """Generate binary .mo file data from messages dict"""
    # Sort messages by msgid
    items = sorted(messages.items())
    
    # Build the file
    data = b''
    
    # Calculate offsets
    entries = []
    ids = b''
    strs = b''
    
    for msgid, msgstr in items:
        msgid_bytes = msgid.encode('utf-8')
        msgstr_bytes = msgstr.encode('utf-8')
        
        entries.append((
            len(ids),
            len(msgid_bytes),
            len(strs),
            len(msgstr_bytes)
        ))
        ids += msgid_bytes + b'\x00'
        strs += msgstr_bytes + b'\x00'
    
    # Header values
    keyoffset = 7 * 4 + 16 * len(entries)
    valueoffset = keyoffset + len(ids)
    
    # Magic number (0xde120495 for little endian)
    data += struct.pack('<I', 0xde120495)
    # Version
    data += struct.pack('<I', 0)
    # Number of entries
    data += struct.pack('<I', len(entries))
    # Offset of table with original strings
    data += struct.pack('<I', 28)
    # Offset of table with translated strings
    data += struct.pack('<I', 28 + len(entries) * 8)
    # Size of hashing table
    data += struct.pack('<I', 0)
    # Offset of hashing table
    data += struct.pack('<I', 0)
    
    # Original string table
    for offset, length, _, _ in entries:
        data += struct.pack('<I', length)
        data += struct.pack('<I', keyoffset + offset)
    
    # Translated string table
    for _, _, offset, length in entries:
        data += struct.pack('<I', length)
        data += struct.pack('<I', valueoffset + offset)
    
    # Original strings
    data += ids
    # Translated strings
    data += strs
    
    return data

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    locale_dir = os.path.join(base_dir, 'locale')
    
    # Compile .po files to .mo files
    for lang in ['uz', 'ru']:
        po_file = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.po')
        mo_file = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.mo')
        
        if os.path.exists(po_file):
            try:
                with open(po_file, 'r', encoding='utf-8') as f:
                    po_content = f.read()
                
                messages = parse_po_file(po_content)
                mo_data = generate_mo_data(messages)
                
                with open(mo_file, 'wb') as f:
                    f.write(mo_data)
                
                print(f"✓ Created: {mo_file}")
            except Exception as e:
                print(f"✗ Error: {e}")
        else:
            print(f"✗ Not found: {po_file}")
    
    print("\n✓ Translation compilation complete!")

