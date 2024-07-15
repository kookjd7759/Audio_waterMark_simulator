from Crypto.PublicKey import RSA

# 키 생성
key = RSA.generate(2048)

# 공개키와 개인키 추출
public_key = key.publickey().export_key()
private_key = key.export_key()

# 키 출력
print("공개키:", public_key.decode())
print("개인키:", private_key.decode())