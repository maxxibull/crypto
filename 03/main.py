from random import randint
from math import gcd
from sympy import mod_inverse

class Keys:
    def __init__(self, sequence_length, max_randint_sequence, max_randint_q):
        self.generate_keys(sequence_length, max_randint_sequence, max_randint_q)

    def generate_superincreasing_sequence(self, length, max_randint):
        sequence = []
        for _ in range(length):
            sequence.append(sum(sequence) + randint(1, max_randint))
        return sequence

    def get_greater_number(self, lower_bound, max_randint):
        return lower_bound + randint(1, max_randint)

    def get_coprime(self, upper_bound):
        rand = randint(1, upper_bound - 1)
        while gcd(rand, upper_bound) != 1:
            rand = randint(1, upper_bound - 1)
        return rand

    def generate_private_key(self, sequence_length, max_randint_sequence, max_randint_q):
        sequence = self.generate_superincreasing_sequence(sequence_length, max_randint_sequence)
        q = self.get_greater_number(sum(sequence), max_randint_q)
        r = self.get_coprime(q)
        self.private_key = (sequence, q, r)

    def generate_public_key(self, sequence, q, r):
        self.public_key = [(w * r) % q for w in sequence]

    def generate_keys(self, sequence_length, max_randint_sequence, max_randint_q):
        self.generate_private_key(sequence_length, max_randint_sequence, max_randint_q)
        self.generate_public_key(*self.private_key)

def encrypt(message, public_key):
    bin_message = "".join(format(ord(m), "b") for m in message)
    if len(bin_message) > len(public_key):
        print("Length of the public key is too short!")
        return
    result = 0
    for i in range(len(bin_message)):
        result += int(bin_message[i]) * public_key[i]
    return result

def decrypt(message, sequence, q, r):
    max_sequence_value = (message * mod_inverse(r, q)) % q
    indexes = []
    while max_sequence_value > 0:
        index = 0
        while sequence[index] <= max_sequence_value:
            index += 1
        indexes.append(index - 1)
        max_sequence_value -= sequence[index - 1]
    result = ""
    for i in range(indexes[0] + 1):
        if i in indexes:
            result += "1"
        else:
            result += "0"
    return "".join(chr(int("".join(r), 2)) for r in zip(*[iter(result)] * 7))

def gui():
    keys = Keys(50, 10, 1000)
    print("Options:")
    print("[0] Exit")
    print("[1] Generate keys")
    print("[2] Encrypt")
    print("[3] Decrypt")
    print("===")
    while(True):
        print()
        option = input("Enter option number: ")
        if option == "0":
            return
        elif option == "1":
            sequence_length = int(input("Enter sequence length: "))
            max_randint_sequence = int(input("Enter max randint for sequence: "))
            max_randint_q = int(input("Enter max randint for q: "))
            keys = Keys(sequence_length, max_randint_sequence, max_randint_q)
            print(f"Public key: {keys.public_key}")
        elif option == "2":
            message = input("Enter message: ")
            print(f"Encrypted message: {encrypt(message, keys.public_key)}")
        elif option == "3": 
            ciphertext = int(input("Enter ciphertext: "))
            print(f"Decrypted message: {decrypt(ciphertext, *keys.private_key)}")
        else:
            print("Wrong data!")

def main():
    gui()

if __name__ == "__main__":
    main()