import sys, time, random

MOD = 10**9 + 7
inv2 = (MOD + 1) // 2

def precompute(max_k):
    B = max_k + 10**7
    a = [0, 1, 2]
    diffs = {1}
    n = 3
    while True:
        if n & 1:
            a.append(2 * a[-1])
        else:
            r = 1
            while r in diffs:
                r += 1
            a.append(a[-1] + r)
        for i in range(1, n):
            diffs.add(a[n] - a[i])
        if a[n - 1] > B:
            break
        n += 1
    for _ in range(10):
        n += 1
        if n & 1:
            a.append(2 * a[-1])
        else:
            r = 1
            while r in diffs:
                r += 1
            a.append(a[-1] + r)
        for i in range(1, n):
            diffs.add(a[n] - a[i])
    N = n
    diag = set()
    for t in range(1, N // 2 + 1):
        diag.add(a[2 * t] - a[2 * t - 1])
    U = [x for x in diffs if x not in diag and x <= B]
    U.sort()
    prefU = [0]
    P = [0]
    for j, u in enumerate(U):
        prefU.append((prefU[-1] + (u % MOD)) % MOD)
        P.append((P[-1] + pow(inv2, u - j, MOD)) % MOD)
    return U, prefU, P

def solve_one(n, U, prefU, P):
    k = n // 2
    m = len(U)
    lo = 0
    hi = m
    while lo < hi:
        mid = (lo + hi) // 2
        d_candidate = k + mid
        ok_left = (mid == 0) or (U[mid - 1] < d_candidate)
        ok_right = (mid == m) or (U[mid] > d_candidate)
        if ok_left and ok_right:
            lo = mid
            break
        if not ok_left:
            hi = mid
        else:
            lo = mid + 1
    m_prime = lo
    d_k = k + m_prime
    d_k_mod = (k % MOD + m_prime) % MOD
    Dsum = d_k_mod * ((d_k_mod + 1) % MOD) % MOD * inv2 % MOD
    Dsum = (Dsum - prefU[m_prime]) % MOD
    A = (pow(2, k + 1, MOD) * ((1 + P[m_prime]) % MOD) - (d_k_mod + 2)) % MOD
    if n & 1 == 0:
        S = (pow(2, k + 1, MOD) - 2 + 4 * A - 3 * Dsum) % MOD
    else:
        S = (3 * pow(2, k, MOD) - 2 + 6 * A - 3 * Dsum) % MOD
    return S

# generate 1000 test cases around 10^100
T = 1000
ns = [random.randint(10**99, 10**100 - 1) for _ in range(T)]
max_k = max(n // 2 for n in ns)

t0 = time.time()
U, prefU, P = precompute(max_k)
t1 = time.time()

out = []
for n in ns:
    out.append(str(solve_one(n, U, prefU, P)))
t2 = time.time()

print('precompute', t1 - t0)
print('solve', t2 - t1)
print('total', t2 - t0)
