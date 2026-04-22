import sys

MOD = 10**9 + 7
INV2 = (MOD + 1) // 2


def arith_sum(first: int, length: int) -> int:
    # first + (first+1) + ... + (first+length-1)
    return (length % MOD) * ((2 * (first % MOD) + (length - 1) % MOD) % MOD) % MOD * INV2 % MOD


def append_part(W: int, D: int, need: int, base: int, segments) -> tuple[int, int]:
    """
    Append the first 'need' values of one stage to:
      D = sum d_i
      W = sum 2^(k-i) * d_i
    The stage values are base + offset, with offset taken from the allowed segments.
    """
    for l, r in segments:
        if need == 0:
            break
        take = r - l + 1
        if take > need:
            take = need
        first = base + l

        D = (D + arith_sum(first, take)) % MOD

        # Append a block: x, x+1, ..., x+take-1
        # NewW = 2^take * W + sum_{j=0}^{take-1} 2^(take-1-j) * (x+j)
        #      = 2^take * W + x * (2^take - 1) + (2^take - take - 1)
        p2 = pow(2, take, MOD)
        W = (p2 * W + (first % MOD) * ((p2 - 1) % MOD) + p2 - take - 1) % MOD

        need -= take
    return W % MOD, D % MOD


def precompute(max_k: int):
    # Generate only the first O(log max_k) pairs directly from the definition.
    a = [0, 1, 2]
    diffs = {1}
    miss = 2

    d = [None, 1]       # d_k = a_{2k} - a_{2k-1}
    e = [None, 2]       # e_k = a_{2k}
    E = [None, [1]]     # E_k = sorted {e_k - a_i | 1 <= i < 2k}
    M = [None, 1]       # M_k = #{i | d_i < e_k}

    while M[-1] < max_k:
        # odd term: a_{2m+1} = 2 * a_{2m}
        x = 2 * a[-1]
        for i in range(1, len(a)):
            diffs.add(x - a[i])
        a.append(x)

        # even term: smallest missing positive difference
        while miss in diffs:
            miss += 1
        x = a[-1] + miss
        for i in range(1, len(a)):
            diffs.add(x - a[i])
        a.append(x)

        m = (len(a) - 1) // 2
        ek = a[2 * m]
        dk = ek - a[2 * m - 1]

        d.append(dk)
        e.append(ek)
        # ek - a_i is increasing when i goes from 2m-1 down to 1
        E.append([ek - a[i] for i in range(2 * m - 1, 0, -1)])
        M.append(ek - 1 - 2 * m * (m - 1))

    # Stage m means the interval [e_m, e_{m+1}).
    # Inside this interval, the d-values are exactly:
    #   e_m + t,  1 <= t < e_m + d_{m+1},
    # except forbidden offsets:
    #   E_m, d_{m+1}, d_{m+1} + E_m.
    n = len(d) - 1
    stages = [None]
    for m in range(1, n):
        base = e[m]
        shift = d[m + 1]

        forb = sorted(set(E[m] + [shift] + [shift + x for x in E[m]]))

        segments = []
        cur = 1
        last = base + shift - 1
        for x in forb:
            if cur <= x - 1:
                segments.append((cur, x - 1))
            cur = x + 1
        if cur <= last:
            segments.append((cur, last))

        stages.append((base, segments))

    # Boundary prefix sums at k = M[m]
    Wb = [0] * (n + 1)
    Db = [0] * (n + 1)
    Wb[1] = 1
    Db[1] = 1

    for m in range(1, n):
        need = M[m + 1] - M[m]
        base, segments = stages[m]
        Wb[m + 1], Db[m + 1] = append_part(Wb[m], Db[m], need, base, segments)

    return M, stages, Wb, Db


def get_WD(k: int, M, stages, Wb, Db) -> tuple[int, int]:
    if k <= 0:
        return 0, 0

    # largest m with M[m] <= k
    lo, hi = 1, len(M) - 1
    while lo < hi:
        mid = (lo + hi + 1) >> 1
        if M[mid] <= k:
            lo = mid
        else:
            hi = mid - 1
    m = lo

    W = Wb[m]
    D = Db[m]
    rem = k - M[m]
    if rem:
        base, segments = stages[m]
        W, D = append_part(W, D, rem, base, segments)
    return W, D


def e_value(k: int, M, stages, Wb, Db) -> int:
    W, _ = get_WD(k, M, stages, Wb, Db)
    return (W + pow(2, k - 1, MOD)) % MOD


def e_prefix_sum(k: int, M, stages, Wb, Db) -> int:
    if k <= 0:
        return 0
    W, D = get_WD(k, M, stages, Wb, Db)
    ek = (W + pow(2, k - 1, MOD)) % MOD
    # sum_{i=1}^k e_i = 2 * e_k - sum_{i=1}^k d_i - 1
    return (2 * ek - D - 1) % MOD


def answer(n: int, M, stages, Wb, Db) -> int:
    if n == 1:
        return 1

    if n & 1:
        # n = 2k - 1
        k = (n + 1) // 2
        return (1 + 3 * e_prefix_sum(k - 1, M, stages, Wb, Db)) % MOD
    else:
        # n = 2k
        k = n // 2
        return (1 + 3 * e_prefix_sum(k - 1, M, stages, Wb, Db) + e_value(k, M, stages, Wb, Db)) % MOD


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    ns = [int(x) for x in data[1:1 + t]]

    max_k = max((n + 1) // 2 for n in ns)
    M, stages, Wb, Db = precompute(max_k)

    out = [str(answer(n, M, stages, Wb, Db)) for n in ns]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()