MOD = 10**9 + 7

memo = {}

def compute(n):
    if n in memo:
        return memo[n]
    if n == 0:
        return (0, 0)
    if n == 1:
        return (1, 1)
    if n % 2 == 1:
        k = (n - 1) // 2
        s_2k, a_2k = compute(2 * k)
        s_n = (s_2k + 2 * a_2k) % MOD
        a_n = (2 * a_2k) % MOD
        memo[n] = (s_n, a_n)
        return (s_n, a_n)
    else:
        k = n // 2
        s_k, a_k = compute(k)
        if k == 1:
            s_2k = 3
            a_2k = 2
        elif k == 2:
            s_2k = 15
            a_2k = 8
        elif k == 3:
            s_2k = 52
            a_2k = 21
        else:
            s_2k_prev, a_2k_prev = compute(2 * (k - 1))
            s_k_prev, a_k_prev = compute(k - 1)
            a_2k = (2 * a_2k_prev + (a_k - a_k_prev)) % MOD
            s_2k = (s_2k_prev + 4 * a_2k_prev + (a_k - a_k_prev)) % MOD
        memo[n] = (s_2k, a_2k)
        return (s_2k, a_2k)

def main():
    import sys
    input = sys.stdin.read().split()
    T = int(input[0])
    for i in range(1, T + 1):
        n_str = input[i]
        n = int(n_str)
        s, _ = compute(n)
        print(s % MOD)

if __name__ == "__main__":
    main()