import sys

MOD = 10 ** 9 + 7
PHI = MOD - 1
INV2 = (MOD + 1) // 2


def precompute(max_k: int):
    B = max_k + 10 ** 7
    a = [0, 1, 2]
    diffs = {1}
    r = 2                     # smallest positive integer not yet in diffs
    n = 3
    while True:
        if n & 1:
            val = 2 * a[-1]
            a.append(val)
            # add small differences; break when they exceed B
            for i in range(n - 1, 0, -1):
                d = val - a[i]
                if d > B:
                    break
                if d not in diffs:
                    diffs.add(d)
                    if d == r:
                        r += 1
                        while r in diffs:
                            r += 1
        else:
            val = a[-1] + r
            a.append(val)
            for i in range(n - 1, 0, -1):
                d = val - a[i]
                if d > B:
                    break
                if d not in diffs:
                    diffs.add(d)
                    if d == r:
                        r += 1
                        while r in diffs:
                            r += 1
        if a[n - 1] > B:
            break
        n += 1

    # a few extra terms to be safe
    for _ in range(10):
        n += 1
        if n & 1:
            val = 2 * a[-1]
            a.append(val)
            for i in range(n - 1, 0, -1):
                d = val - a[i]
                if d > B:
                    break
                if d not in diffs:
                    diffs.add(d)
                    if d == r:
                        r += 1
                        while r in diffs:
                            r += 1
        else:
            val = a[-1] + r
            a.append(val)
            for i in range(n - 1, 0, -1):
                d = val - a[i]
                if d > B:
                    break
                if d not in diffs:
                    diffs.add(d)
                    if d == r:
                        r += 1
                        while r in diffs:
                            r += 1

    diag = set()
    for t in range(1, n // 2 + 1):
        diag.add(a[2 * t] - a[2 * t - 1])

    U = [x for x in diffs if x not in diag and x <= B]
    U.sort()
    m = len(U)

    prefU = [0] * (m + 1)
    P = [0] * (m + 1)
    sU = 0
    sP = 0
    base = INV2
    mod = MOD
    phi = PHI
    for j, u in enumerate(U):
        sU += u % mod
        if sU >= mod:
            sU -= mod
        prefU[j + 1] = sU
        e = (u % phi - j) % phi
        sP += pow(base, e, mod)
        if sP >= mod:
            sP -= mod
        P[j + 1] = sP

    return U, prefU, P


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    ns = [int(x) for x in data[1:]]

    max_k = max(n // 2 for n in ns)
    U, prefU, P = precompute(max_k)
    m = len(U)

    out = []
    for n in ns:
        k = n // 2
        # binary search for J = smallest j with U[j] - j - 1 >= k
        lo = 0
        hi = m
        while lo < hi:
            mid = (lo + hi) // 2
            if U[mid] - mid - 1 >= k:
                hi = mid
            else:
                lo = mid + 1
        J = lo

        d_k = k + J
        d_k_mod = (k % MOD + J) % MOD

        Dsum = d_k_mod * ((d_k_mod + 1) % MOD) % MOD * INV2 % MOD
        Dsum = (Dsum - prefU[J]) % MOD

        two_k1 = pow(2, (k + 1) % PHI, MOD)
        A = (two_k1 * ((1 + P[J]) % MOD) - (d_k_mod + 2)) % MOD

        if n & 1 == 0:          # n = 2k
            S = (two_k1 - 2 + 4 * A - 3 * Dsum) % MOD
        else:                    # n = 2k + 1
            two_k = pow(2, k % PHI, MOD)
            S = (3 * two_k - 2 + 6 * A - 3 * Dsum) % MOD

        out.append(str(S))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
