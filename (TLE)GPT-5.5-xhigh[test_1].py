import sys
from bisect import bisect_right


MOD = 1_000_000_007
INV2 = (MOD + 1) // 2
EXTRA = 1_000_000


def build_skips(max_k):
    """Return skip start positions t for all cross-pair differences needed.

    If c_j is the j-th cross-pair difference, then c_j is absent from the gap
    sequence and increases every d_i with i >= c_j - j + 1 by one.
    """
    if max_k <= 0:
        return [], [0], [0]

    limit = max_k + EXTRA

    a = [0, 1, 2]
    diffs = {1}
    mex = 2
    n = 2

    while not (n % 2 == 0 and a[-1] > limit):
        n += 1
        if n % 2:
            value = 2 * a[-1]
        else:
            value = a[-1] + mex

        for i in range(1, n):
            diffs.add(value - a[i])
        a.append(value)

        while mex in diffs:
            mex += 1

    cross = set()
    size = len(a)
    for j in range(1, size):
        aj = a[j]
        pj = (j + 1) // 2
        for i in range(j - 1, 0, -1):
            d = aj - a[i]
            if d > limit:
                break
            if (i + 1) // 2 != pj:
                cross.add(d)

    cross = sorted(cross)

    starts = []
    for idx, c in enumerate(cross, 1):
        t = c - idx + 1
        if t > max_k:
            break
        starts.append(t)

    pref_t = [0]
    pref_inv_pow = [0]
    for t in starts:
        pref_t.append((pref_t[-1] + (t % MOD)) % MOD)
        pref_inv_pow.append((pref_inv_pow[-1] + pow(INV2, t, MOD)) % MOD)

    return starts, pref_t, pref_inv_pow


def solve_case(n, starts, pref_t, pref_inv_pow):
    k = n // 2
    m = bisect_right(starts, k)

    k_mod = k % MOD
    pow2_k = pow(2, k, MOD)
    pow2_next = (2 * pow2_k) % MOD

    sum_d = (
        k_mod * ((k + 1) % MOD) * INV2
        + (m % MOD) * ((k_mod + 1) % MOD)
        - pref_t[m]
    ) % MOD

    weighted_d = (
        pow2_next
        - k_mod
        - 2
        + pow2_next * pref_inv_pow[m]
        - m
    ) % MOD

    sum_even_terms = (pow2_k - 1 + 2 * weighted_d - sum_d) % MOD

    if n % 2:
        return (1 + 3 * sum_even_terms) % MOD

    last_even = ((pow2_k * INV2) + weighted_d) % MOD
    return (1 + 3 * sum_even_terms - 2 * last_even) % MOD


def main():
    data = sys.stdin.buffer.read().lstrip(b"\xef\xbb\xbf").split()
    if not data:
        return

    t = int(data[0])
    nums = [int(x) for x in data[1 : 1 + t]]
    max_k = max((x // 2 for x in nums), default=0)

    starts, pref_t, pref_inv_pow = build_skips(max_k)
    out = [str(solve_case(x, starts, pref_t, pref_inv_pow)) for x in nums]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
