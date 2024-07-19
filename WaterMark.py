from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

import numpy as np
import time
import random
import Path

def createKey():
    # RSA 키 생성
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    path = Path.getKeyFolder()
    with open(path + 'private.pem', "wb") as f:
        f.write(private_key)

    with open(path + 'public.pem', "wb") as f:
        f.write(public_key)

def create():
    private_key_file = Path.getKeyFolder() + 'private.pem'
    # 타임스탬프 추가
    timestamp = int(time.time())
    watermark_data = f"{random.random()}|{timestamp}"

    # 해시 생성
    hash_obj = SHA256.new(watermark_data.encode('utf-8'))

     # RSA 서명
    with open(private_key_file, "rb") as f:
        private_key = RSA.import_key(f.read())
    signature = pkcs1_15.new(private_key).sign(hash_obj)

    # 해시 값을 사용하여 16비트로 줄이기
    short_watermark_bits = bin(int(signature.hex(), 16))[-16:]
    
    print(f"Watermark Bits: {short_watermark_bits}")

    return np.array(list(map(int, short_watermark_bits)))

def verify_watermark(watermark_data, signature, public_key_file):
    # 해시 생성
    hash_obj = SHA256.new(watermark_data.encode('utf-8'))

    # RSA 서명 검증
    with open(public_key_file, "rb") as f:
        public_key = RSA.import_key(f.read())

    try:
        pkcs1_15.new(public_key).verify(hash_obj, signature)
        print("The watermark is authentic.")
    except (ValueError, TypeError):
        print("The watermark is not authentic.")
