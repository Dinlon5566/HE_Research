import time
import tenseal as ts
import matplotlib.pyplot as plt
import numpy as np

# 初始化CKKS上下文
CKKSContext = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
CKKSContext.generate_galois_keys()
CKKSContext.global_scale = 2**40

# 創建加密向量
b = [0.123]  # 初始明文數據，CKKS支持浮點數
Ta_encrypted = ts.ckks_vector(CKKSContext, b)

times_list = []
elapsed_times = []
average_times = []

# 從1次到2^n次
for exponent in range(14):
    print(f"times: {2 ** exponent}")
    
    times = 2 ** exponent
    times_list.append(times)

    start_time_ckks = time.time()
    for i in range(times):
        a_encrypted = Ta_encrypted
        a_encrypted = a_encrypted * a_encrypted
    end_time_ckks = time.time()

    elapsed_time = end_time_ckks - start_time_ckks
    elapsed_times.append(elapsed_time)
    average_times.append(elapsed_time / times)

# 打印和繪製結果
for i, txt in enumerate(elapsed_times):
    print(f"{times_list[i]} times: {txt:.6f} seconds")
    plt.annotate(f'{txt:.2f}', (times_list[i], elapsed_times[i]))

plt.plot(times_list, elapsed_times, marker='o', label='Total Time')
plt.plot(times_list, average_times, marker='x', linestyle='--', color='r', label='Average Time')
plt.xlabel('Number of Computational operations')
plt.ylabel('Time (seconds)')
plt.title('CKKS Computational operations Time')
plt.xscale('log') 
plt.yscale('log')
plt.grid(True)
plt.legend()
plt.show()
