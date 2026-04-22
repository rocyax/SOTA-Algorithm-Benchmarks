import time, sys
from answer import precompute, MOD, PHI, INV2
import random

T = 1000
ns = [random.randint(10**99, 10**100 - 1) for _ in range(T)]
max_k = max(n // 2 for n in ns)

t0 = time.time()
U, prefU, P = precompute(max_k)
t1 = time.time()

out = []
for n in ns:
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
    out.append(str(S))
t2 = time.time()
print('precompute', t1 - t0)
print('solve', t2 - t1)
print('total', t2 - t0)
