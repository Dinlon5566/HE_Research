# 本專案用來測試CKKS在浮點數上的精度

import tenseal as ts
import time
import numpy as np
# constant
times = 1000
a = 50.32
b = 6966.987
twosum=a+b
twominus=a-b
twomul=a*b

def createCKKSContext():
    CKKSContext = ts.context(ts.SCHEME_TYPE.CKKS,
                             poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
    CKKSContext.generate_galois_keys()
    CKKSContext.global_scale = 2**40
    return CKKSContext


def show_progress(iteration, total, length=50):
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = "█" * filled_length + '-' * (length - filled_length)
    print(f'\rProgress: |{bar}| {percent}%', end='\r')
    if iteration == total: 
        print()

def main():
    CKKScontext = createCKKSContext()

    ssum=0
    sminus=0
    smul=0

    for i in range(times):
        encrypt_a = ts.ckks_vector(CKKScontext, [a])
        encrypt_b = ts.ckks_vector(CKKScontext, [b])
        enTwosum = encrypt_a + encrypt_b
        enTwominus = encrypt_a - encrypt_b
        enTwomul = encrypt_a * encrypt_b
        deTwosum = enTwosum.decrypt()
        deTwominus = enTwominus.decrypt()
        deTwomul = enTwomul.decrypt()
        ssum += abs(deTwosum[0]-twosum)
        sminus+= abs(deTwominus[0]-twominus)
        smul+= abs(deTwomul[0]-twomul)   
        show_progress(i+1, times)     
        
    #輸出誤差
    print(f"計算 {times} 次加法誤差：{ssum} 平均誤差：{ssum/times}")
    print(f"計算 {times} 次減法誤差：{sminus} 平均誤差：{sminus/times}")
    print(f"計算 {times} 次乘法誤差：{smul} 平均誤差：{smul/times}")
    
    
if __name__ == "__main__":
    main()
