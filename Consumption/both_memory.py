import time
import psutil
import os
import tenseal as ts
import random

# 請在 linux下執行

def measure_memory_usage(func, *args, **kwargs):
    process = psutil.Process(os.getpid())
    start_memory_use = process.memory_info().rss
    result = func(*args, **kwargs)
    end_memory_use = process.memory_info().rss
    memory_use = end_memory_use - start_memory_use
    return memory_use, result


def bfv_algorithm():
    BFVContext = ts.context(
        ts.SCHEME_TYPE.BFV, poly_modulus_degree=4096, plain_modulus=1032193)
    BFVContext.generate_galois_keys()
    BFVContext.global_scale = 2**40

    Ta_encrypted = ts.bfv_vector(BFVContext, [random.randint(0, 100)])
    Ta_encrypted = Ta_encrypted * Ta_encrypted
    Ta_decrypted = Ta_encrypted.decrypt()
    return Ta_decrypted


def ckks_algorithm():
    CKKSContext = ts.context(
        ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
    CKKSContext.generate_galois_keys()
    CKKSContext.global_scale = 2**40

    Ta_encrypted = ts.ckks_vector(CKKSContext, [random.uniform(0, 100)])
    a_encrypted = Ta_encrypted * Ta_encrypted
    a_decrypted = a_encrypted.decrypt()
    return a_decrypted


def main():
    # 測量 BFV 算法的執行時間和記憶體使用
    start_time = time.time()
    memory_use_bfv, _ = measure_memory_usage(bfv_algorithm)
    end_time = time.time()
    execution_time_bfv = end_time - start_time

    print(f"BFV 執行時間: {execution_time_bfv} 秒")
    print(f"BFV 峰值記憶體使用: {memory_use_bfv / (1024**2)} MiB")

    # 測量 CKKS 算法的執行時間和記憶體使用
    start_time = time.time()
    memory_use_ckks, _ = measure_memory_usage(ckks_algorithm)
    end_time = time.time()
    execution_time_ckks = end_time - start_time

    print(f"CKKS 執行時間: {execution_time_ckks} 秒")
    print(f"CKKS 峰值記憶體使用: {memory_use_ckks / (1024**2)} MiB")


if __name__ == '__main__':
    main()
