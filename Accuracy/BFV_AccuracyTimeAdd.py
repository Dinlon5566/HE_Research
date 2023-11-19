import tenseal as ts
import numpy as np
import matplotlib.pyplot as plt
import random


def createBFVContext():
    BFVContext = ts.context(
        ts.SCHEME_TYPE.BFV, poly_modulus_degree=4096, plain_modulus=1032193)
    BFVContext.generate_galois_keys()
    return BFVContext

def show_progress(run, total_runs, length=50):
    percent = "{0:.1f}".format(100 * (run / float(total_runs)))
    filled_length = int(length * run // total_runs)
    bar = "█" * filled_length + '-' * (length - filled_length)
    print(f'\rProgress: |{bar}| {percent}% Run {run}/{total_runs}', end='\r')
    if run == total_runs: 
        print()


def calculate_accuracy(BFVcontext, a, times):
    heSum = ts.bfv_vector(BFVcontext, [0])
    total = 0
    encrypt_a = ts.bfv_vector(BFVcontext, [a])
    for i in range(times):
        heSum += encrypt_a
        total += a
    deHeSum = heSum.decrypt()
    return abs(deHeSum[0] - total)


def main():
    BFVcontext = createBFVContext()

    timeExp = 13
    total_runs = 100
    results = np.zeros((total_runs, timeExp))

    for run in range(total_runs):
        for exponent in range(timeExp):
            times = 2 ** exponent
            a = random.randint(-2**8, 2**8)  
  
            accuracy = calculate_accuracy(BFVcontext, a, times)
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
    plt.title('BFV Additive Operations Error Analysis over 100 Runs')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.legend()
    plt.show()

# 呼叫 main 函數
main()
