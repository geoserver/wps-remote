from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import base64
import sys

def encrypt(message, externKey, passphrase):
    publickey = open(externKey, "r")
    rsa_key = RSA.importKey(publickey, passphrase=passphrase)
    # verifier = PKCS1_v1_5.new(rsa_key)
    # h = SHA.new(message)
    encriptedData = rsa_key.encrypt(message, 0)
    print(base64.b64encode(encriptedData[0]))

if __name__ == "__main__":
    if len(sys.argv) == 4:
        encrypt(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python encrypt.py password path/to/rsakey.pub passphrase")
