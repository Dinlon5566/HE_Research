import time
import tenseal as ts
import matplotlib.pyplot as plt
import numpy as np

# initialize BFV context
BFVContext = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=4096, plain_modulus=1032193)
BFVContext.generate_galois_keys()
BFVContext.global_scale = 2**40

# create encrypted vector
a = [3165461]   # initial plaintext data
Ta_encrypted = ts.bfv_vector(BFVContext, a)

times_list = []
elapsed_times = []
average_times = []

# 1 times to 2^n times
for exponent in range(14):
    print(f"times: {2 ** exponent}")
    
    times = 2 ** exponent
    times_list.append(times)

    
    start_time_bfv = time.time()
    for i in range(times):
        a_encrypted = ts.bfv_vector(BFVContext, a)
        a_encrypted = Ta_encrypted
        a_encrypted = a_encrypted * a_encrypted
        a_decrypted = a_encrypted.decrypt()
    end_time_bfv = time.time()

    elapsed_time = end_time_bfv - start_time_bfv
    elapsed_times.append(elapsed_time)
    average_times.append(elapsed_time / times)

for i, txt in enumerate(elapsed_times):
    print(f"{times_list[i]} times: {txt:.6f} seconds")
    plt.annotate(f'{txt:.2f}', (times_list[i], elapsed_times[i]))

# Draw table of total time and average time
plt.plot(times_list, elapsed_times, marker='o', label='Total Time')
plt.plot(times_list, average_times, marker='x', linestyle='--', color='r', label='Average Time')
plt.xlabel('Number of Encryptions/Decryptions')
plt.ylabel('Time (seconds)')
plt.title('BFV Encryptions/Decryptions operations Time')
plt.xscale('log') 
plt.yscale('log')
plt.grid(True)
plt.legend()
plt.show()
