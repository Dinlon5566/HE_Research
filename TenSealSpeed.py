import tenseal as ts
import time
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import numpy as np

# 初始化參數
times = 1000
a = 5465623
b = 5.5

# 1. BFV
BFVContext = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=4096, plain_modulus=1032193)
BFVContext.generate_galois_keys()
BFVContext.global_scale = 2**40

# 測量BFV加解密時間
start_time_bfv = time.time()
for i in range(times):
    a_encrypted = ts.bfv_vector(BFVContext, [a])
    a_decrypted = a_encrypted.decrypt()
end_time_bfv = time.time()

print(f"BFV 加解密 {times} 次所需時間：{(end_time_bfv - start_time_bfv):.6f} 秒")
print(f"平均每次加解密時間：{(end_time_bfv - start_time_bfv)/times:.6f} 秒")

# 2.CKKS

CKKSContext = ts.context(ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
CKKSContext.generate_galois_keys()
CKKSContext.global_scale = 2**40

start_time_ckks = time.time()
for i in range(times):
    a_encrypted = ts.ckks_vector(CKKSContext, [a])
    a_decrypted = a_encrypted.decrypt()
end_time_ckks = time.time()
    
print(f"CKKS 加解密 {times} 次所需時間：{(end_time_ckks - start_time_ckks):.6f} 秒")
print(f"平均每次加解密時間：{(end_time_ckks - start_time_ckks)/times:.6f} 秒")

# 3. AES256
data = str(a).encode('utf-8')

# 測量AES加解密時間
start_time_aes = time.time()
for i in range(times):
    key = get_random_bytes(32)  # 256bit key
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    cipher_dec = AES.new(key, AES.MODE_EAX,nonce=cipher.nonce)
    decrypted_data = cipher_dec.decrypt(ciphertext)
end_time_aes = time.time()

print(f"AES256 加解密 {times} 次所需時間：{(end_time_aes - start_time_aes):.6f} 秒")
print(f"平均每次加解密時間：{(end_time_aes - start_time_aes)/times:.6f} 秒")

