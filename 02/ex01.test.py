import unittest
from ex01 import get_encryption_key, encrypt_file
from Crypto.Cipher import AES
import filecmp
import os

def decrypt_file(input_path, output_path, cipher):
    with open(input_path, mode="rb") as input_file:
        cipher_text = input_file.read()
        text = cipher.decrypt(cipher_text)
    with open(output_path, mode="w") as output_file:
        output_file.write(str(text, encoding="utf-8"))

class EncryptionsTestCase(unittest.TestCase): 
    def setUp(self):
        self.input_path = "zeroes.txt"
        self.encryption_key = get_encryption_key("store.jck", "storepassword", "aesalias", "keypassword")
        self.encryption_key.decrypt("keypassword")

    def test_ofb(self):
        temp_file = "ofb.txt"
        ouput_file = "ofb_dec.txt"
        encrypt_file(self.input_path, temp_file, AES.new(self.encryption_key._key, AES.MODE_OFB, "0000000000000000"))
        decrypt_file(temp_file, ouput_file, AES.new(self.encryption_key._key, AES.MODE_OFB, "0000000000000000"))
        self.assertTrue(filecmp.cmp(self.input_path, ouput_file))

    def test_ctr(self):
        temp_file = "ctr.txt"
        ouput_file = "ctr_dec.txt"
        counter = os.urandom(16)
        encrypt_file(self.input_path, temp_file, AES.new(self.encryption_key._key, AES.MODE_CTR, "0000000000000000", counter=lambda: counter))
        decrypt_file(temp_file, ouput_file, AES.new(self.encryption_key._key, AES.MODE_CTR, "0000000000000000", counter=lambda: counter))
        self.assertTrue(filecmp.cmp(self.input_path, ouput_file))

    def test_cbc(self):
        temp_file = "cbc.txt"
        ouput_file = "cbc_dec.txt"
        encrypt_file(self.input_path, temp_file, AES.new(self.encryption_key._key, AES.MODE_CBC, "0000000000000000"))
        decrypt_file(temp_file, ouput_file, AES.new(self.encryption_key._key, AES.MODE_CBC, "0000000000000000"))
        self.assertTrue(filecmp.cmp(self.input_path, ouput_file))

if __name__ == '__main__':
    unittest.main()
