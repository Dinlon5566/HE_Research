import tenseal as ts
import numpy as np
import matplotlib.pyplot as plt
import random

def createCKKSContext():
    CKKSContext = ts.context(ts.SCHEME_TYPE.CKKS,
                             poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
    CKKSContext.generate_galois_keys()
    CKKSContext.global_scale = 2**40
    return CKKSContext

def show_progress(run, total_runs, length=50):
    percent = "{0:.1f}".format(100 * (run / float(total_runs)))
    filled_length = int(length * run // total_runs)
    bar = "█" * filled_length + '-' * (length - filled_length)
    print(f'\rProgress: |{bar}| {percent}% Run {run}/{total_runs}', end='\r')
    if run == total_runs: 
        print()

def calculate_accuracy(CKKScontext, a, times):
    heSum = ts.ckks_vector(CKKScontext, [0])
    total = 0
    encrypt_a = ts.ckks_vector(CKKScontext, [a])
    for i in range(times):
        heSum += encrypt_a
        total += a
    deHeSum = heSum.decrypt()
    return abs(deHeSum[0] - total)

def main():
    CKKScontext = createCKKSContext()
    
    timeExp = 13
    
    total_runs = 100
    results = np.zeros((total_runs, timeExp))
    
    for run in range(total_runs):
        for exponent in range(timeExp):
            times = 2 ** exponent
            a = random.uniform(-2**16, 2**16)
            accuracy = calculate_accuracy(CKKScontext, a, times)
            results[run, exponent] = accuracy
        show_progress(run + 1, total_runs)

    min_errors = results.min(axis=0)
    mean_errors = results.mean(axis=0)
    median_errors = np.median(results, axis=0)
    max_errors = results.max(axis=0)
    
    x = [2 ** exp for exp in range(timeExp)]
    
    for i, txt in enumerate(min_errors):
        print(f"{x[i]} Error amount: {txt:.10f}")
        plt.annotate(f'{txt:.2E}', (x[i], min_errors[i]))

    plt.plot(x, min_errors, marker='o', label='Minimum Error')
    plt.plot(x, mean_errors, marker='x', label='Average Error')
    plt.plot(x, median_errors, marker='^', label='Median Error')
    plt.plot(x, max_errors, marker='s', label='Maximum Error')
    plt.xlabel('Number of Computational Operations')
    plt.ylabel('Error | Abs {Dec[Enc(a)+Enc(b)]-(a+b)}')
    plt.title('CKKS Additive Operations Error Analysis over 100 Runs')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.legend()
    plt.show()

# 呼叫 main 函數
main()
