import sys

MOD = 1_000_000_007
INV2 = (MOD + 1) // 2


def advance(even_value, even_sum, odd_sum, pos, end, skipped):
    length = end - pos
    if length <= 0:
        return even_value, even_sum, odd_sum

    length_mod = length % MOD
    scale = pow(2, length, MOD)
    tail = (((end + skipped) % MOD) * (scale - 1) - ((length_mod - 2) * scale + 2)) % MOD
    end_even = (scale * even_value + tail) % MOD

    even_tail = (
        even_value * (2 * (scale - 1) % MOD)
        + 2 * tail
        - length_mod * ((pos + skipped) % MOD)
        - length_mod * ((length + 1) % MOD) * INV2
    ) % MOD
    even_sum = (even_sum + even_tail) % MOD
    odd_sum = (odd_sum + 2 * (even_tail - end_even + even_value)) % MOD
    return end_even, even_sum, odd_sum


def precompute(limit, max_need):
    a = [0, 1, 2]
    diffs = {1}
    d = [0, 1]
    pref = [0, 1, 3]

    for n in range(3, 2 * limit + 1):
        if n & 1:
            value = 2 * a[-1]
        else:
            mex = d[-1]
            while mex in diffs:
                mex += 1
            value = a[-1] + mex
            d.append(mex)
        for old in a[1:]:
            diffs.add(value - old)
        a.append(value)
        pref.append((pref[-1] + value) % MOD)

    used = set(d[1:])
    skipped_values = sorted(x for x in diffs if x not in used and x <= max_need + len(diffs) + 10)
    thresholds = []
    for idx, value in enumerate(skipped_values, 1):
        threshold = value - idx + 1
        if threshold > 1:
            thresholds.append(threshold)

    even_sum = sum(a[2 * i] for i in range(1, len(d))) % MOD
    odd_sum = sum(a[2 * i - 1] for i in range(1, len(d))) % MOD
    return a, d, pref, thresholds, even_sum, odd_sum


def solve(n, a, d, pref, thresholds, base_even_sum, base_odd_sum):
    if n < len(pref):
        return pref[n]

    pair_count = n // 2
    extra_odd = n & 1
    base = len(d) - 1
    if pair_count <= base:
        ans = pref[2 * pair_count]
        if extra_odd:
            ans = (ans + 2 * a[2 * pair_count]) % MOD
        return ans

    even_value = a[2 * base] % MOD
    even_sum = base_even_sum
    odd_sum = base_odd_sum
    pos = base
    skipped = d[base] - base

    idx = 0
    while idx < len(thresholds) and thresholds[idx] <= base:
        idx += 1

    while idx < len(thresholds) and thresholds[idx] <= pair_count:
        threshold = thresholds[idx]
        even_value, even_sum, odd_sum = advance(even_value, even_sum, odd_sum, pos, threshold - 1, skipped)
        pos = threshold - 1
        while idx < len(thresholds) and thresholds[idx] == threshold:
            skipped += 1
            idx += 1

    even_value, even_sum, odd_sum = advance(even_value, even_sum, odd_sum, pos, pair_count, skipped)
    ans = (even_sum + odd_sum) % MOD
    if extra_odd:
        ans = (ans + 2 * even_value) % MOD
    return ans


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    nums = [int(x) for x in data[1:]]
    max_pair = max(nums) // 2
    limit = max(420, len(str(max(nums))) * 5)
    a, d, pref, thresholds, even_sum, odd_sum = precompute(limit, max_pair)
    out = [str(solve(n, a, d, pref, thresholds, even_sum, odd_sum)) for n in nums]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
