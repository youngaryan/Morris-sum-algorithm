import random
import matplotlib.pyplot as plt
import numpy as np

def morris(stream):
    approx_count = 0
    exact_count = 0
    for _ in stream:
        exact_count+=1
        if random.random() < 1 / ((base ** approx_count)):
            approx_count += 1
        
    return 2**approx_count , exact_count

def plot_relative_errors(errors, title = "Morris"):
    errors = np.array(errors)
    average_error = np.mean(errors)
    std_deviation = np.std(errors)
    fig, ax = plt.subplots()
    ax.plot(errors, marker='o', linestyle='-', color='b', label='Relative Errors')
    ax.axhline(y=average_error, color='r', linestyle='--', label=f'Average Error: {average_error:.4f}')
    ax.axhline(y=average_error + std_deviation, color='g', linestyle='-.', label=f'Standard Deviation: {std_deviation:.4f}') 
    ax.axhline(y=average_error - std_deviation, color='g', linestyle='-.') 
    ax.set_xlabel('Iteration') 
    ax.set_ylabel('Relative Error') 
    ax.set_title(f'Relative Errors with Average and Standard Deviation {title}') 
    ax.legend()
    plt.show()
    
def sum_morris(stream, max_val=100):
    """
    Updates counters based on the probability rule and calculates the estimated sum.

    Args:
    stream (list): List of integers a_i representing incoming elements.

    Returns:
    int: The estimated sum, exact sum.
    """
    counters = [0] * (max_val + 1)  # Initialize n counters (indexed from 1 to n)
    exact_sum = 0
    # Update counters based on the given probability rule
    for elem in stream:
        exact_sum+=elem
        prob = 2 ** (-counters[elem])  # Probability 2^(-X_i)
        if random.random() < prob:  # Increment with the specified probability
            counters[elem] += 1

    # Calculate the estimated sum
    estimated_sum = 0
    for i in range(1, max_val + 1):  # Loop through counters (1-indexed)
        if counters[i] != 0:
            estimated_sum += (2 ** counters[i]) * i

    return estimated_sum, exact_sum

if __name__ == "__main__":

    base = 2
    
    approx_results = []
    exact_results = []
    errors = []
    relative_errors = []
    for i in range(100000):
        stream = [random.randint(1, 100) for _ in range(1_000)]
        approx, exact = morris(stream)
        # approx, exact = sum_morris(stream)
        approx_results.append(approx)
        exact_results.append(exact)
        errors.append(abs(approx - exact))
        relative_errors.append(abs(approx - exact) / exact if exact != 0 else 0)
        print(f"Approximate Sum: {approx:.2f}")
        print(f"Exact Sum: {exact}")
        print(f"Error: {abs(approx - exact):.2f}")
        print(f"Relative Error: {relative_errors[i]:.4f}")
    
        print("-" * 40)
    
    print(f"Average Error: {sum(errors) / len(errors):.2f}")
    print(f"Average Relative Error: {sum(relative_errors) / len(relative_errors):.4f}")
    
    plot_relative_errors(relative_errors)