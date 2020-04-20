#bin/bash
python3 ex01.py --store store.jck --store-pass storepassword --key-id aesalias --key-pass keypassword --iv 1234567898765432 --mode oracle --enc-type cbc --inputs zeroes.txt
python3 xor.py --iv-previous 1234567898765432 --iv-new 1234567898765433 --output-path xor.txt
python3 ex01.py --store store.jck --store-pass storepassword --key-id aesalias --key-pass keypassword --iv 1234567898765433 --mode challenge --enc-type cbc --inputs xor.txt test.txt
cmp --silent "challenge_message.txt" "enc_zeroes.txt" && echo "xor.txt" || echo "test.txt"
