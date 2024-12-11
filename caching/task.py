import math
import time

def __is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def heavy_task_prime(time_delay):
    # primes = []
    # for num in range(10**6, 10**6 + 50000):  # Checking 50,000 numbers
    #     if __is_prime(num):
    #         primes.append(num)
    time.sleep(time_delay)
    # print(f"Found {len(primes)} primes.")

if __name__ == "__main__":
    start = time.time()
    heavy_task_prime()
    print("Time execution: {}".format(time.time() - start))