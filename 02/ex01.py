import argparse
import os
import random
import jks
from Crypto.Cipher import AES

MODES = ("oracle", "challenge")
ENCRYPTIONS = {
    "ofb": AES.MODE_OFB,
    "ctr": AES.MODE_CTR,
    "cbc": AES.MODE_CBC,
}

def get_encryption_key(store_path, store_password, key_id, key_password):
    store = jks.KeyStore.load(store_path, store_password)
    return store.secret_keys[key_id]

def encrypt_file(input_path, output_path, cipher):
    with open(input_path, mode="rb") as input_file:
        text = input_file.read()
        cipher_text = cipher.encrypt(text)
    with open(output_path, mode="wb") as output_file:
        output_file.write(cipher_text)

def main(args):
    encryption_key = get_encryption_key(args.store, args.store_pass, args.key_id, args.key_pass)
    encryption_key.decrypt(args.key_pass)
    if args.mode == "oracle":
        for input_path in args.inputs:
            encrypt_file(
                input_path,
                f"enc_{input_path}",
                AES.new(
                    encryption_key._key,
                    ENCRYPTIONS[args.enc_type],
                    bytes(args.iv, encoding="utf-8"),
                ),
            )
    else:
        input_path = random.choice(args.inputs[:2])
        encrypt_file(
            input_path,
            f"challenge_message.txt",
            AES.new(
                encryption_key._key,
                ENCRYPTIONS[args.enc_type],
                bytes(args.iv, encoding="utf-8"),
            ),
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--store", required=True, help="Keystore")
    parser.add_argument("--store-pass", required=True, help="Password to keystore")
    parser.add_argument("--key-id", required=True, help="Key id")
    parser.add_argument("--key-pass", required=True, help="Password to key")
    parser.add_argument("--iv", required=True, help="IV")
    parser.add_argument("--mode", required=True, choices=MODES, help="Program mode")
    parser.add_argument("--enc-type",required=True, choices=ENCRYPTIONS.keys(), help="Ecnryption type",)
    parser.add_argument("--inputs", required=True, help="Input files", nargs="+")
    args = parser.parse_args()
    main(args)
