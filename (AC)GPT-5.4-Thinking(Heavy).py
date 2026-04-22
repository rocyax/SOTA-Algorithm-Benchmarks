import sys
from bisect import bisect_right

MOD = 10**9 + 7
INV2 = (MOD + 1) // 2


def count_t(i: int, limit: int, d: list[int], c: list[int]) -> int:
    """
    Count elements <= limit in T_i.

    T_1 = {0, 1}
    T_i = {0, d_i} U (c_i + T_{i-1})   for i >= 2
    """
    cnt = 0
    while True:
        if limit < 0:
            return cnt
        cnt += 1                    # 0
        if limit >= d[i]:
            cnt += 1                # d_i
        if i == 1:
            return cnt
        limit -= c[i]
        i -= 1


def precompute(max_m: int):
    """
    Precompute all exceptional numbers up to a safe limit.

    For x <= 10^100, the number of exceptional values <= x is only O((log x)^2),
    so this precompute is tiny in practice.
    """
    if max_m == 0:
        return [], [0], [0], [1, 2]

    bits = max_m.bit_length()
    margin = 2 * (bits + 5) * (bits + 5) + 10
    limit = max_m + margin

    # 1-indexed
    d = [0, 1]      # d_k = a_{2k} - a_{2k-1}
    b = [0, 2]      # b_k = a_{2k}
    c = [0, 0]      # c_k = b_k - b_{k-1}, k >= 2
    T = [None, [0, 1]]

    k = 1
    while True:
        k += 1

        def count_exc(x: int) -> int:
            ans = 0
            for i in range(1, len(b)):
                if b[i] > x:
                    break
                ans += count_t(i, x - b[i], d, c)
            for i in range(2, len(c)):
                if c[i] > x:
                    break
                ans += count_t(i - 1, x - c[i], d, c)
            return ans

        # d_k is the k-th positive integer outside the exceptional set
        x = k
        while True:
            nx = k + count_exc(x)
            if nx == x:
                dk = x
                break
            x = nx

        d.append(dk)
        bk = 2 * b[k - 1] + dk
        ck = bk - b[k - 1]
        b.append(bk)
        c.append(ck)

        # T_k is sorted because ck > dk and T_{k-1} is sorted
        T.append([0, dk] + [ck + x for x in T[k - 1]])

        if b[k] > limit and c[k] > limit:
            break

    # Enumerate all exceptional numbers <= limit
    exc = []
    for i in range(1, len(b)):
        bi = b[i]
        if bi <= limit:
            rem = limit - bi
            for x in T[i]:
                if x > rem:
                    break
                exc.append(bi + x)

        if i >= 2:
            ci = c[i]
            if ci <= limit:
                rem = limit - ci
                for x in T[i - 1]:
                    if x > rem:
                        break
                    exc.append(ci + x)

    exc.sort()

    # remove duplicates, just in case
    uniq = []
    last = None
    for x in exc:
        if x != last:
            uniq.append(x)
            last = x
    exc = uniq

    m = len(exc)

    pref_sum = [0] * (m + 1)       # prefix sum of exceptional numbers
    pref_weight = [0] * (m + 1)    # prefix sum of 2^(j - e_j)
    pow2_small = [1] * (m + 2)     # 2^i mod MOD for small i

    for i in range(1, m + 2):
        pow2_small[i] = (pow2_small[i - 1] * 2) % MOD

    if m:
        # w_j = 2^(j - e_j)
        w = pow(INV2, exc[0] - 1, MOD)   # j = 1
        pref_sum[1] = exc[0] % MOD
        pref_weight[1] = w

        gap_cache = {}
        prev = exc[0]

        for j in range(2, m + 1):
            cur = exc[j - 1]
            gap = cur - prev

            mul = gap_cache.get(gap)
            if mul is None:
                mul = (2 * pow(INV2, gap, MOD)) % MOD   # 2^(1-gap)
                gap_cache[gap] = mul

            w = (w * mul) % MOD
            prev = cur

            pref_sum[j] = (pref_sum[j - 1] + cur) % MOD
            pref_weight[j] = (pref_weight[j - 1] + w) % MOD

    return exc, pref_sum, pref_weight, pow2_small


def prefix_x_over_2x(n: int) -> int:
    """sum_{x=1}^n x / 2^x mod MOD"""
    if n <= 0:
        return 0
    return (2 - ((n + 2) % MOD) * pow(INV2, n, MOD)) % MOD


def pair_prefix_data(m: int, exc, pref_sum, pref_weight, pow2_small):
    """
    Return:
        b_m = a_{2m} mod MOD
        B_m = sum_{i=1}^m b_i mod MOD
    """
    if m == 0:
        return 0, 0

    # d_m satisfies: d_m = m + (# exceptional numbers <= d_m)
    x = m
    while True:
        nx = m + bisect_right(exc, x)
        if nx == x:
            d_m = x
            break
        x = nx

    cnt = bisect_right(exc, d_m)
    sum_exc = pref_sum[cnt]
    sum_2j_minus_ej = pref_weight[cnt]

    # G(d) = sum_{x non-exceptional, 2<=x<=d} x * 2^(exc_before(x) - x)
    G = (
        pow2_small[cnt] * prefix_x_over_2x(d_m)
        - pow2_small[cnt + 1]
        + 3 * INV2
        + sum_2j_minus_ej
    ) % MOD

    pow2m = pow(2, m, MOD)
    W = pow2m * G % MOD                    # W = sum_{i=2}^m 2^(m-i) d_i
    b_m = (pow2m + W) % MOD

    # D_m = sum_{i=1}^m d_i
    D_m = ((d_m % MOD) * ((d_m + 1) % MOD) * INV2 - sum_exc) % MOD

    # B_m = sum_{i=1}^m b_i
    B_m = (pow2m * 2 - 1 + 2 * W - D_m) % MOD

    return b_m, B_m


def solve(nums: list[int]) -> list[int]:
    max_m = max(n // 2 for n in nums)
    exc, pref_sum, pref_weight, pow2_small = precompute(max_m)

    ans = []
    for n in nums:
        m = n // 2
        b_m, B_m = pair_prefix_data(m, exc, pref_sum, pref_weight, pow2_small)

        if n & 1:
            # 1 + (b_1+2b_1) + ... + (b_m+2b_m)
            ans.append((1 + 3 * B_m) % MOD)
        else:
            # 1 + (b_1+2b_1) + ... + (b_{m-1}+2b_{m-1}) + b_m
            ans.append((1 + 3 * B_m - 2 * b_m) % MOD)

    return ans


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    nums = [int(x) for x in data[1:1 + t]]

    out = solve(nums)
    sys.stdout.write("\n".join(map(str, out)))


if __name__ == "__main__":
    main()