import sys
from bisect import bisect_right

MOD = 10**9 + 7
PHI = MOD - 1
INV2 = (MOD + 1) // 2


def precompute_levels(max_level: int):
    """
    Directly precompute a small prefix of a_n, then extract:
      e[k] = a[2k]
      g[k] = a[2k] - a[2k-1]
      P[k] = sorted(e[k] - a[i] for i=1..2k)

    max_level is only about 350 for n < 10^100.
    """
    N = 2 * (max_level + 2)

    a = [0] * (N + 1)
    a[1], a[2] = 1, 2

    diffs = {1}
    mex = 2

    for n in range(3, N + 1):
        if n & 1:
            a[n] = 2 * a[n - 1]
        else:
            while mex in diffs:
                mex += 1
            a[n] = a[n - 1] + mex

        an = a[n]
        for i in range(1, n):
            diffs.add(an - a[i])

    e = [0] * (max_level + 3)
    g = [0] * (max_level + 3)
    P = [[] for _ in range(max_level + 3)]

    for k in range(1, max_level + 2):
        e[k] = a[2 * k]
        g[k] = a[2 * k] - a[2 * k - 1]
        P[k] = sorted(e[k] - a[i] for i in range(1, 2 * k + 1))

    return e, g, P


def build_R(limit: int, e, g, P, max_level: int):
    """
    Build sorted non-gap differences R <= limit.
    """
    vals = []

    for k in range(1, max_level + 1):
        if e[k] > limit:
            break

        shift1 = e[k]
        shift2 = e[k] + g[k + 1]

        for p in P[k]:
            x = shift1 + p
            if x > limit:
                break

            vals.append(x)

            y = shift2 + p
            if y <= limit:
                vals.append(y)

    return sorted(set(vals))


def prepare_global_R(maxK: int, e, g, P, max_level: int):
    """
    Need R up to g_K = K + count(R <= g_K).
    Fixed point iteration gives the needed global limit.
    """
    guess = maxK

    while True:
        R = build_R(guess, e, g, P, max_level)
        new_guess = maxK + len(R)
        if new_guess == guess:
            return R
        guess = new_guess


def prepare_prefixes(R):
    """
    For sorted R = [r_1, r_2, ...], precompute:
      A[c] = sum_{j=1..c} 2^(j-r_j)
      B[c] = sum_{j=1..c} r_j
    modulo MOD.
    """
    prefA = [0] * (len(R) + 1)
    prefB = [0] * (len(R) + 1)

    for j, r in enumerate(R, start=1):
        prefA[j] = (prefA[j - 1] + pow(2, (j - r) % PHI, MOD)) % MOD
        prefB[j] = (prefB[j - 1] + r) % MOD

    return prefA, prefB


def count_excluded_for_K(K: int, R):
    """
    Find c such that g_K = K + c and c = count(R <= g_K).
    """
    guess = K

    while True:
        c = bisect_right(R, guess)
        new_guess = K + c
        if new_guess == guess:
            return c
        guess = new_guess


def compute_e_and_sum_e(K: int, R, prefA, prefB):
    """
    Returns:
      e_K = a_{2K}
      E_sum = e_1 + e_2 + ... + e_K
    modulo MOD.
    """
    c = count_excluded_for_K(K, R)

    k_mod = K % MOD
    c_mod = c % MOD
    pow2K = pow(2, K, MOD)

    # Base case if g_i = i:
    # H = sum i * 2^(K-i) = 2^(K+1) - K - 2
    H0 = (2 * pow2K - k_mod - 2) % MOD

    # Each excluded r_j shifts gaps from index s_j = r_j - j + 1 upward by +1.
    # Weighted correction:
    # sum_j (2^(K-s_j+1)-1)
    # = 2^K * sum_j 2^(j-r_j) - c
    Hcorr = (pow2K * prefA[c] - c_mod) % MOD
    H = (H0 + Hcorr) % MOD

    # Sum of gaps.
    G0 = k_mod * ((K + 1) % MOD) % MOD * INV2 % MOD
    Gcorr = (
        c_mod * k_mod
        - prefB[c]
        + c_mod * ((c + 1) % MOD) % MOD * INV2
    ) % MOD
    Gsum = (G0 + Gcorr) % MOD

    # e_K = 2^(K-1) + H
    eK = (pow2K * INV2 + H) % MOD

    # sum e_i = 2^K - 1 + 2H - sum g_i
    sumE = (pow2K - 1 + 2 * H - Gsum) % MOD

    return eK, sumE


def answer(n: int, R, prefA, prefB):
    if n & 1:
        # n = 2K - 1
        K = (n + 1) // 2
        eK, sumE = compute_e_and_sum_e(K, R, prefA, prefB)
        return (3 * sumE - 3 * eK + 1) % MOD
    else:
        # n = 2K
        K = n // 2
        eK, sumE = compute_e_and_sum_e(K, R, prefA, prefB)
        return (3 * sumE - 2 * eK + 1) % MOD


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    t = int(data[0])
    ns = [int(x) for x in data[1:1 + t]]

    maxK = max((n + 1) // 2 for n in ns)

    # e_k roughly doubles, so bit_length + 10 is plenty.
    max_level = max(20, maxK.bit_length() + 10)

    e, g, P = precompute_levels(max_level)
    R = prepare_global_R(maxK, e, g, P, max_level)
    prefA, prefB = prepare_prefixes(R)

    out = [str(answer(n, R, prefA, prefB)) for n in ns]
    print("\n".join(out))


if __name__ == "__main__":
    main()