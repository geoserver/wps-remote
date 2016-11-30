from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import base64
import sys

def decrypt(message, externKey, passphrase):
    privatekey = open(externKey, "r")
    rsa_key = RSA.importKey(privatekey, passphrase=passphrase)
    # verifier = PKCS1_v1_5.new(rsa_key)
    # h = SHA.new(message)
    decriptedData = rsa_key.decrypt(base64.b64decode(message))
    print(decriptedData)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        decrypt(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python decrypt.py password path/to/rsakey.pem passphrase")
