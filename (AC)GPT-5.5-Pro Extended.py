import sys
from bisect import bisect_left

MOD = 1_000_000_007
INV2 = (MOD + 1) // 2


def generate_terms(cnt: int):
    """Generate the first cnt terms exactly. cnt is only O(log max_n)."""
    a = [1]
    diffs = set()
    mex = 1

    for n in range(2, cnt + 1):
        if n == 2:
            x = 2
        elif n & 1:
            x = 2 * a[-1]
        else:
            x = a[-1] + mex

        for y in a:
            diffs.add(x - y)
        a.append(x)

        while mex in diffs:
            mex += 1

    return a


def build_forbidden(a, upper: int):
    """
    Differences <= upper that are not adjacent pair gaps a[2k]-a[2k-1].
    i, j below are 1-based indices.
    """
    forbidden = []

    for j in range(1, len(a) + 1):
        aj = a[j - 1]

        # Going backwards: differences increase as i decreases, so we can stop.
        for i in range(j - 1, 0, -1):
            d = aj - a[i - 1]
            if d > upper:
                break

            # This one is a gap g_k, not a forbidden value.
            if not (j % 2 == 0 and i == j - 1):
                forbidden.append(d)

    return sorted(set(forbidden))


def advance(E: int, S: int, v: int, L: int):
    """
    Apply L consecutive gaps v, v+1, ..., v+L-1 to:
      E = a[2k] mod MOD
      S = sum_{i=1}^{2k} a[i] mod MOD
    """
    if L <= 0:
        return E, S

    p = pow(2, L, MOD)
    lm = L % MOD
    vm = v % MOD

    # A = sum_{t=0}^{L-1} 2^(L-1-t) * (v+t)
    A = (vm * (p - 1) + (p - lm - 1)) % MOD

    # B = sum_{t=0}^{L-1} (v+t)
    B = (lm * vm + lm * ((L - 1) % MOD) * INV2) % MOD

    oldE = E
    E = (p * oldE + A) % MOD
    S = (S + 4 * ((p - 1) % MOD) * oldE + 4 * A - 3 * B) % MOD
    return E, S


def build_checkpoints(forbidden):
    """
    Checkpoint c means: after skipping the first c forbidden values and after
    processing all allowed gap values before them.
    """
    Kdone = 0
    next_value = 1

    # Modular trick: with g_1=1, e_1=2*e_0+1 and P_1=P_0+4*e_0+1,
    # so e_0=1/2 gives e_1=2, P_1=3.
    E = INV2
    S = 0

    cpK = [0]
    cpNext = [1]
    cpE = [E]
    cpS = [S]

    for x in forbidden:
        L = x - next_value
        if L:
            E, S = advance(E, S, next_value, L)
            Kdone += L

        # x is not used as an adjacent gap.
        next_value = x + 1

        cpK.append(Kdone)
        cpNext.append(next_value)
        cpE.append(E)
        cpS.append(S)

    return cpK, cpNext, cpE, cpS


def prepare(maxK: int):
    """
    Precompute all non-adjacent differences needed for every K <= maxK.
    """
    b = max(1, maxK.bit_length())
    upper = max(1, maxK + (2 * (b + 10)) ** 2)

    while True:
        cnt = max(20, 2 * (upper.bit_length() + 10))

        while True:
            a = generate_terms(cnt)
            # Then no later term can create a non-adjacent difference <= upper.
            if a[-2] > upper:
                break
            cnt *= 2

        forbidden = build_forbidden(a, upper)
        cpK, cpNext, cpE, cpS = build_checkpoints(forbidden)

        # For the j-th forbidden value f_j, cpK[j] = f_j - j:
        # number of allowed gap values before f_j. It is nondecreasing.
        H = cpK[1:]

        c = bisect_left(H, maxK)  # forbidden values strictly before g_maxK
        needed = maxK + c         # value of g_maxK

        if needed <= upper:
            return H, cpK, cpNext, cpE, cpS

        b = max(1, needed.bit_length())
        upper = needed + (2 * (b + 10)) ** 2


def solve_one(N: int, data):
    H, cpK, cpNext, cpE, cpS = data

    if N == 1:
        return 1

    K = N // 2

    # Number of forbidden values before the K-th allowed gap.
    c = bisect_left(H, K)

    E = cpE[c]
    S = cpS[c]
    L = K - cpK[c]

    E, S = advance(E, S, cpNext[c], L)

    if N & 1:
        return (S + 2 * E) % MOD
    return S % MOD


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return

    T = int(tokens[0])
    ns = [int(x) for x in tokens[1:1 + T]]

    data = prepare(max(n // 2 for n in ns))
    print("\n".join(str(solve_one(n, data)) for n in ns))


if __name__ == "__main__":
    main()