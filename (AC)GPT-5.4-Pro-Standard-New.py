import sys, os
from bisect import bisect_right

MOD = 1_000_000_007
PHI = MOD - 1
INV2 = (MOD + 1) // 2
SAFE = 1_000_000
SMALL_POW_LIMIT = 10000


def build_terms_until(limit: int):
    """Generate a[1..n] until n is even and a[n] > limit.

    This also gives the preceding odd gap after the last even gap <= limit,
    which is needed when enumerating interval sums.
    """
    a = [0, 1, 2]  # 1-indexed
    diffs = {1}
    mex = 2
    n = 2

    while not (n % 2 == 0 and a[-1] > limit and n > 2):
        n += 1
        if n & 1:
            x = a[-1] * 2
        else:
            x = a[-1] + mex

        # Add all new differences x - a[i].
        for y in a[1:]:
            diffs.add(x - y)
        a.append(x)

        while mex in diffs:
            mex += 1

    return a


def build_for_limit(limit: int):
    """Build sorted P and prefix data.

    P is the set of all interval sums of the gap sequence that contain at
    least one even-positioned gap. The odd-positioned single gaps are exactly
    the q_i values, so q_i are the positive integers not in P.
    """
    a = build_terms_until(limit)
    # gaps[i] = a[i+1] - a[i], 1-indexed; the last generated term is the
    # first even term > limit, so all necessary gaps are present.
    gaps = [0]
    gaps_extend = gaps.append
    for i in range(1, len(a) - 1):
        gaps_extend(a[i + 1] - a[i])

    r = len(gaps) - 1
    P = []
    append_p = P.append
    for left in range(1, r + 1):
        s = 0
        has_even_gap = False
        for right in range(left, r + 1):
            s += gaps[right]
            if (right & 1) == 0:
                has_even_gap = True
            if s > limit:
                break
            if has_even_gap:
                append_p(s)

    P.sort()
    del gaps, a

    # Prefixes over P. For P[j-1] with 1-based rank j, its threshold is
    # t = P[j-1] - j: it contributes +1 to every q_i with i >= t.
    n = len(P)
    pref_t = [0] * (n + 1)       # sum of thresholds modulo MOD
    pref_inv2_t = [0] * (n + 1)  # sum of INV2^threshold modulo MOD

    small_pow = [1] * SMALL_POW_LIMIT
    for i in range(1, SMALL_POW_LIMIT):
        small_pow[i] = (small_pow[i - 1] * INV2) % MOD

    cur = 1  # INV2^0
    prev_t = 0
    for rank, p in enumerate(P, 1):
        t = p - rank
        delta = (t - prev_t) % PHI
        if delta:
            if delta < SMALL_POW_LIMIT:
                cur = (cur * small_pow[delta]) % MOD
            else:
                cur = (cur * pow(INV2, delta, MOD)) % MOD
        pref_inv2_t[rank] = (pref_inv2_t[rank - 1] + cur) % MOD
        pref_t[rank] = (pref_t[rank - 1] + (t % MOD)) % MOD
        prev_t = t

    return P, pref_t, pref_inv2_t


def count_p_before_q(P, c: int) -> int:
    """For the c-th positive integer not in P, return #P not exceeding it."""
    x = c
    while True:
        cnt = bisect_right(P, x)
        nx = c + cnt
        if nx == x:
            return cnt
        x = nx


def calc_b_and_B(m: int, P, pref_t, pref_inv2_t):
    """Return (b_m, B_m) modulo MOD, where b_m=a[2m] and B_m=sum b_i."""
    if m <= 0:
        return 0, 0

    pow2m = pow(2, m, MOD)
    pow2m1 = pow(2, m - 1, MOD)
    mm = m % MOD

    # Base case q_i = i + 1, i=1..m-1.
    W = (3 * pow2m1 - mm - 2) % MOD
    U = ((m - 1) % MOD) * ((m + 2) % MOD) % MOD * INV2 % MOD

    # Add one step function for every P element <= q_{m-1}.
    c = count_p_before_q(P, m)
    W = (W + pow2m * pref_inv2_t[c] - c) % MOD
    U = (U + (c % MOD) * mm - pref_t[c]) % MOD

    b = (pow2m + W) % MOD
    B = (2 * (pow2m - 1) + 2 * W - U) % MOD
    return b, B


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    ns = [int(x) for x in data[1:1 + t]]
    max_m = max((n // 2 for n in ns), default=0)

    # The number of excluded values P below any q_i is O(log^2 i).  For the
    # official bound n < 10^100 this margin is far larger than necessary.
    limit = max_m + SAFE
    P, pref_t, pref_inv2_t = build_for_limit(limit)

    out = []
    for n in ns:
        m = n // 2
        b, B = calc_b_and_B(m, P, pref_t, pref_inv2_t)
        if n & 1:
            ans = (1 + 3 * B) % MOD
        else:
            ans = (1 + 3 * B - 2 * b) % MOD
        out.append(str(ans))

    sys.stdout.write("\n".join(out))
    sys.stdout.flush()
    os._exit(0)


if __name__ == "__main__":
    main()
