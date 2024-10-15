#!/usr/bin/env python

from Crypto.Cipher import AES
import hashlib
import os
import sys
import re
import json

directory = sys.argv[1] if len(sys.argv) > 1 else "."
key = "HiReg-5D765B15-8F5B-46DC-9B7C-80322B8F74E4"

def decrypt(content, key):
    try:
        aes_key = hashlib.md5(key.encode()).digest()
        cipher = AES.new(aes_key, AES.MODE_ECB)
        return cipher.decrypt(content).decode()
    except ValueError as e:
        print(f"Invalid key: {str(e)}")
        return None

def getjsonprofile(filename, content):
    var = {}
    variable_pattern = re.compile(r'(\w+)=(.+)')

    for match in variable_pattern.finditer(content):
        name = match.group(1)
        value = match.group(2)
        var[name] = value

    json_data = {
        "name": filename,
        "DDRSTEP0": [int(x, 16) for x in var['DDRSTEP0'].split(',')],
        "ADDRESS": [
            var['ADDRESS0'],
            var['ADDRESS1'],
            var['ADDRESS2']
        ],
        "FILELEN": [
            var['FILELEN0'],
            var['FILELEN1']
        ],
        "STEPLEN": [
            var['STEPLEN0'],
            var['STEPLEN1']
        ]
    }

    return json_data

def main():
    for filename in os.listdir(directory):
        if filename.endswith(".chip"):
            name, _ = os.path.splitext(filename)
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'rb') as file:
                    content = file.read()

                print(f"Decoding {filename}")
                decrypted_content = decrypt(content, key).replace('\r','')
                jsonprofile = getjsonprofile(name.lower(), decrypted_content)

                if jsonprofile:
                    with open(directory + '/' + name.lower() + '.json', 'w') as f:
                        json.dump(jsonprofile, f)

            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main()
