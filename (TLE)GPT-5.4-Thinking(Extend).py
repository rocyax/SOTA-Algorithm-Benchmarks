import sys
from bisect import bisect_left, bisect_right
from functools import lru_cache

MOD = 1_000_000_007
INV2 = (MOD + 1) // 2

def prepare(max_k: int):
    # Seed values:
    # x_k = a_{2k} - a_{2k-1}
    # b_k = a_{2k}
    b = [0, 2, 8, 21, 51, 112]
    x = [0, 1, 4, 5, 9, 10]

    def count_terms_leq(v: int) -> int:
        """Number of sequence terms a_i <= v, using current b[] only."""
        if v < 1:
            return 0

        # even terms: b_j <= v
        u = bisect_right(b, v) - 1

        # odd terms after a1: 2*b_j <= v
        lo, hi = 1, len(b) - 1
        w = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if 2 * b[mid] <= v:
                w = mid
                lo = mid + 1
            else:
                hi = mid - 1

        # a1 = 1, plus all b_j, plus all 2*b_j
        return 1 + u + w

    def count_omitted_upto(m: int) -> int:
        """
        Number of omitted integers y <= m, where omitted means:
        y never appears in x_1, x_2, ...
        This works as long as m < b[-1].
        """
        if m <= 0:
            return 0

        k = bisect_left(b, m)  # first block with b_k >= m
        if k == 1:
            return 1 if m >= 2 else 0

        # total omitted up to b_{k-1}
        total = 2 * (k - 1) * (k - 1) - 2 * (k - 1) + 1

        # block (b_{k-1}, b_k]:
        # {2*b_{k-1} - a_i | 1 <= i <= 2k-3}
        total += (2 * k - 3) - count_terms_leq(2 * b[k - 1] - m - 1)

        # {b_k - a_i | 1 <= i <= 2k-2}
        if m >= b[k] - b[k - 1]:
            total += (2 * k - 2) - count_terms_leq(b[k] - m - 1)

        # plus b_k itself
        if m >= b[k]:
            total += 1

        return total

    # Extend until b[-1] is definitely larger than every x_k we may query.
    while b[-1] <= max_k + (2 * (len(b) - 1) * (len(b) - 1) - 2 * (len(b) - 1) + 1) + 5:
        k = len(x)  # next x-index to compute

        lo = k
        hi = min(
            b[-1] - 1,
            k + (2 * (len(b) - 1) * (len(b) - 1) - 2 * (len(b) - 1) + 1) + 5,
        )

        while lo < hi:
            mid = (lo + hi) // 2
            if mid - count_omitted_upto(mid) >= k:
                hi = mid
            else:
                lo = mid + 1

        xk = lo
        x.append(xk)
        b.append(2 * b[-1] + xk)

    K = len(x) - 1

    # Build all sequence terms a_1..a_{2K}.
    a = [0] * (2 * K + 1)
    a[1] = 1
    for k in range(1, K + 1):
        a[2 * k] = b[k]
        if 2 * k + 1 <= 2 * K:
            a[2 * k + 1] = 2 * b[k]

    # Build all omitted numbers y <= b_K.
    Y = [2]
    for k in range(2, K + 1):
        for i in range(1, 2 * k - 2):   # 1 .. 2k-3
            Y.append(2 * b[k - 1] - a[i])
        for i in range(1, 2 * k - 1):   # 1 .. 2k-2
            Y.append(b[k] - a[i])
        Y.append(b[k])

    Y.sort()

    # prefix sums of omitted values, and of 2^{-r(y)} where r(y)=y-index+1
    preY = [0]
    preInv = [0]
    sy = 0
    si = 0
    for idx, y in enumerate(Y, 1):
        sy = (sy + y) % MOD
        rank = y - idx + 1
        si = (si + pow(INV2, rank, MOD)) % MOD
        preY.append(sy)
        preInv.append(si)

    return b, Y, preY, preInv

def solve_all(nums):
    max_k = max((n + 1) // 2 for n in nums)
    b, Y, preY, preInv = prepare(max_k)
    omitted_total = len(Y)

    @lru_cache(maxsize=None)
    def kth_non_omitted(k: int):
        """Return (x_k, cnt), where cnt = number of omitted y <= x_k."""
        if k <= 0:
            return 0, 0

        lo = k
        hi = k + omitted_total + 5  # x_k = k + O(log^2 k)

        while lo < hi:
            mid = (lo + hi) // 2
            cnt = bisect_right(Y, mid)
            if mid - cnt >= k:
                hi = mid
            else:
                lo = mid + 1

        cnt = bisect_right(Y, lo)
        return lo, cnt

    @lru_cache(maxsize=None)
    def XW(k: int):
        """
        Returns:
          x_k  : exact integer
          X_k  : sum_{i=1}^k x_i mod MOD
          W_k  : sum_{i=1}^k 2^{k-i} x_i mod MOD
        """
        if k <= 0:
            return 0, 0, 0

        xk, cnt = kth_non_omitted(k)
        xk_mod = xk % MOD

        # X_k = sum of non-omitted numbers <= x_k
        Xk = (xk_mod * ((xk + 1) % MOD) * INV2 - preY[cnt]) % MOD

        # W_k = sum 2^{k-i} * i + sum_{omitted y<=x_k}(2^{k-r(y)+1}-1)
        p2 = pow(2, k + 1, MOD)
        Wk = (p2 - (k % MOD) - 2 + p2 * preInv[cnt] - cnt) % MOD
        return xk, Xk, Wk

    @lru_cache(maxsize=None)
    def B(k: int) -> int:
        """b_k = a_{2k} mod MOD."""
        if k <= 0:
            return 0
        _, _, Wk = XW(k)
        return (pow(2, k - 1, MOD) + Wk) % MOD

    @lru_cache(maxsize=None)
    def P(k: int) -> int:
        """P_k = sum_{i=1}^{2k} a_i mod MOD."""
        if k <= 0:
            return 0
        _, Xk, _ = XW(k)
        _, Xkm1, Wkm1 = XW(k - 1)
        return (pow(2, k + 1, MOD) - 2 + 8 * Wkm1 - 4 * Xkm1 + Xk) % MOD

    out = []
    for n in nums:
        if n == 1:
            out.append("1")
        elif n & 1:
            m = n // 2
            out.append(str((P(m) + 2 * B(m)) % MOD))
        else:
            out.append(str(P(n // 2) % MOD))
    return out

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    nums = [int(x) for x in data[1:1 + t]]
    print("\n".join(solve_all(nums)))

if __name__ == "__main__":
    main()