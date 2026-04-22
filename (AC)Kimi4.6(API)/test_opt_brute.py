import random, sys
from answer import precompute, MOD, PHI, INV2

def brute(n):
    a = [0, 1, 2]
    diffs = {1}
    for idx in range(3, n + 1):
        if idx & 1:
            a.append(2 * a[-1])
        else:
            r = 1
            while r in diffs:
                r += 1
            a.append(a[-1] + r)
        for i in range(1, idx):
            diffs.add(a[idx] - a[i])
    return sum(a[1:n+1]) % MOD

max_n = 500
max_k = max_n // 2
U, prefU, P = precompute(max_k)

for n in range(1, max_n + 1):
    k = n // 2
    lo = 0
    hi = len(U)
    while lo < hi:
        mid = (lo + hi) // 2
        if U[mid] - mid - 1 >= k:
            hi = mid
        else:
            lo = mid + 1
    J = lo
    d_k_mod = (k % MOD + J) % MOD
    Dsum = d_k_mod * ((d_k_mod + 1) % MOD) % MOD * INV2 % MOD
    Dsum = (Dsum - prefU[J]) % MOD
    two_k1 = pow(2, (k + 1) % PHI, MOD)
    A = (two_k1 * ((1 + P[J]) % MOD) - (d_k_mod + 2)) % MOD
    if n & 1 == 0:
        S = (two_k1 - 2 + 4 * A - 3 * Dsum) % MOD
    else:
        two_k = pow(2, k % PHI, MOD)
        S = (3 * two_k - 2 + 6 * A - 3 * Dsum) % MOD
    expected = brute(n)
    if S != expected:
        print('Mismatch at', n, S, expected)
        sys.exit(1)

print('All ok up to', max_n)

# random tests up to 1000
for _ in range(100):
    n = random.randint(1, 1000)
    k = n // 2
    lo = 0
    hi = len(U)
    while lo < hi:
        mid = (lo + hi) // 2
        if U[mid] - mid - 1 >= k:
            hi = mid
        else:
            lo = mid + 1
    J = lo
    d_k_mod = (k % MOD + J) % MOD
    Dsum = d_k_mod * ((d_k_mod + 1) % MOD) % MOD * INV2 % MOD
    Dsum = (Dsum - prefU[J]) % MOD
    two_k1 = pow(2, (k + 1) % PHI, MOD)
    A = (two_k1 * ((1 + P[J]) % MOD) - (d_k_mod + 2)) % MOD
    if n & 1 == 0:
        S = (two_k1 - 2 + 4 * A - 3 * Dsum) % MOD
    else:
        two_k = pow(2, k % PHI, MOD)
        S = (3 * two_k - 2 + 6 * A - 3 * Dsum) % MOD
    expected = brute(n)
    if S != expected:
        print('Mismatch at random', n, S, expected)
        sys.exit(1)
print('All random ok up to 1000')
