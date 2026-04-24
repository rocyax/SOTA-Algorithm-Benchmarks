# answer.py
import sys
from bisect import bisect_right

MOD = 10**9 + 7
INV2 = (MOD + 1) // 2


def prepare(max_rank):
    """
    We need all skipped numbers c whose effect-rank tau = c - (#previous skipped)
    is <= max_rank.

    Since n < 1e100, generating until the current even term exceeds
    max_rank + 1_000_000 is more than enough; the loop below also verifies
    this margin condition.
    """
    margin = 1_000_000

    while True:
        U = max_rank + margin

        # Generate initial A001856 terms until an even term is > U.
        a = [0, 1, 2]          # 1-indexed; a[0] unused
        diffs = {1}
        mex = 1

        while True:
            idx = len(a)       # next index

            if idx & 1:        # odd index
                x = 2 * a[-1]
            else:              # even index
                while mex in diffs:
                    mex += 1
                x = a[-1] + mex

            for i in range(1, idx):
                diffs.add(x - a[i])

            a.append(x)

            if idx % 2 == 0 and x > U:
                break

        # Skipped numbers: all differences <= U except the special adjacent
        # mex differences a[2k+2] - a[2k+1], k >= 1.
        skipped = set()
        n_terms = len(a) - 1

        for j in range(2, n_terms + 1):
            aj = a[j]
            for i in range(j - 1, 0, -1):
                d = aj - a[i]
                if d > U:
                    break

                is_special_mex_pair = (i >= 3 and (i & 1) and j == i + 1)
                if not is_special_mex_pair:
                    skipped.add(d)

        skipped = sorted(skipped)

        # If an unseen skipped number c > U had tau <= max_rank, then before it
        # there would already be more than `margin` skipped numbers <= U.
        if len(skipped) < margin:
            break

        margin *= 2

    taus = []
    pref_inv_pow2 = [0]
    pref_tau = [0]

    current_inv_pow = 1
    prev_tau = 0

    for idx, c in enumerate(skipped, start=1):
        tau = c - (idx - 1)
        taus.append(tau)

        delta = tau - prev_tau
        if delta == 1:
            current_inv_pow = current_inv_pow * INV2 % MOD
        elif delta:
            current_inv_pow = current_inv_pow * pow(INV2, delta, MOD) % MOD
        prev_tau = tau

        pref_inv_pow2.append((pref_inv_pow2[-1] + current_inv_pow) % MOD)
        pref_tau.append((pref_tau[-1] + tau) % MOD)

    return taus, pref_inv_pow2, pref_tau


def solve_case(n, taus, pref_inv_pow2, pref_tau):
    def b_mod(m):
        # b_m = a_{2m}
        if m <= 0:
            return 0

        cnt = bisect_right(taus, m - 1)
        pow2m = pow(2, m, MOD)

        # b_m = 2^(m+1) - m - 1 + sum_{tau<=m-1}(2^(m-tau)-1)
        return (
            2 * pow2m
            - (m % MOD)
            - 1
            + pow2m * pref_inv_pow2[cnt]
            - cnt
        ) % MOD

    def rho_prefix(k):
        # sum_{i=1}^k rho_i
        if k <= 0:
            return 0

        cnt = bisect_right(taus, k)

        base = (k % MOD) * ((k + 1) % MOD) % MOD * INV2 % MOD
        extra = (cnt % MOD) * ((k + 1) % MOD) % MOD
        extra = (extra - pref_tau[cnt]) % MOD

        return (base + extra) % MOD

    def B_mod(m):
        # B_m = sum_{i=1}^m b_i
        if m <= 0:
            return 0

        bm = b_mod(m)
        return (2 * bm - 2 - rho_prefix(m - 1)) % MOD

    m = n // 2

    # S_{2m} = 1 + 2 * B_{m-1} + B_m
    ans = (1 + 2 * B_mod(m - 1) + B_mod(m)) % MOD

    # S_{2m+1} = S_{2m} + a_{2m+1} = S_{2m} + 2*b_m
    if n & 1:
        ans = (ans + 2 * b_mod(m)) % MOD

    return ans


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    t = int(data[0])
    nums = [int(x) for x in data[1:1 + t]]

    max_m = max(n // 2 for n in nums)
    max_rank = max(0, max_m - 1)

    taus, pref_inv_pow2, pref_tau = prepare(max_rank)

    out = []
    for n in nums:
        out.append(str(solve_case(n, taus, pref_inv_pow2, pref_tau)))

    print("\n".join(out))


if __name__ == "__main__":
    main()