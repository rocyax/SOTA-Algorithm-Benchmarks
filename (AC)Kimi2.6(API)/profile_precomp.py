import sys, time

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
    diag = set()
    for t in range(1, n // 2 + 1):
        diag.add(a[2 * t] - a[2 * t - 1])
    t0 = time.time()
    U = [x for x in diffs if x not in diag and x <= B]
    U.sort()
    t1 = time.time()
    m = len(U)
    prefU = [0] * (m + 1)
    P = [0] * (m + 1)
    sU = 0
    sP = 0
    base = inv2
    mod = MOD
    for j, u in enumerate(U):
        sU += u % mod
        if sU >= mod:
            sU -= mod
        prefU[j+1] = sU
        # inline pow via built-in
        sP += pow(base, u - j, mod)
        if sP >= mod:
            sP -= mod
        P[j+1] = sP
    t2 = time.time()
    print('filter sort', t1-t0)
    print('prefix', t2-t1)
    print('len U', m)
    return U, prefU, P

# simulate with max_k ~ 1e100 / 2
max_k = 10**100 // 2
precompute(max_k)
