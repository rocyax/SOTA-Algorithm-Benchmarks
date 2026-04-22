import sys

MOD = 1_000_000_007
INV2 = (MOD + 1) // 2


def build_fail(limit: int):
    """
    Build all 'fail' values in [1, limit].

    fail = all realized differences except the special adjacent ones
           a_{2k} - a_{2k-1}.

    We stop when the last built term is even-indexed and > limit.
    Then no future fail value <= limit can appear.
    """
    a = [1, 2]
    diffs = {0, 1}      # all differences already present in the built prefix
    special = {1}       # used values b_k = a_{2k} - a_{2k-1}
    mex = 0

    while len(a) % 2 == 1 or a[-1] <= limit:
        n = len(a) + 1

        if n & 1:  # odd index
            new = a[-1] * 2
        else:      # even index
            while mex in diffs:
                mex += 1
            new = a[-1] + mex
            special.add(mex)

        for old in a:
            diffs.add(new - old)
        a.append(new)

    fail = [x for x in diffs if 0 < x <= limit and x not in special]
    fail.sort()

    # Sentinel 0 on the left, limit+1 on the right.
    # The last sentinel is enough because we only need good numbers <= limit.
    fail.insert(0, 0)
    fail.append(limit + 1)
    return fail


def advance(cur_mod: int, start_mod: int, k: int):
    """
    A block starts with consecutive increments:
        start, start+1, ..., start+k-1

    cur_mod: current odd-indexed term before this block, modulo MOD.

    Returns:
        new_cur_mod: odd-indexed term after k full pairs
        added_sum_mod: sum contributed by those 2*k terms
    """
    km = k % MOD
    p2 = pow(2, k, MOD)

    base = (cur_mod + 2 * start_mod + 2) % MOD

    # x_k = 2^k * (x_0 + 2s + 2) - 2k - 2s - 2
    new_cur = (p2 * base - 2 * km - 2 * start_mod - 2) % MOD

    # sum of k full pairs:
    # 3 * (x_0 + 2s + 2) * (2^k - 1) - 3 * k * (k + 2s + 3) / 2
    added = (
        3 * base * (p2 - 1)
        - 3 * km * ((km + 2 * start_mod + 3) % MOD) * INV2
    ) % MOD

    return new_cur, added


def solve(queries):
    max_n = max(queries)

    # Usually one round is enough, but make it robust.
    limit = max_n
    while True:
        fail = build_fail(limit)

        fail_count = len(fail) - 2          # exclude 0 and sentinel
        good_count = limit - fail_count     # good numbers in [1, limit]
        covered_terms = 1 + 2 * good_count  # a1 + two terms per good number

        if covered_terms >= max_n:
            break
        limit *= 2

    order = sorted(range(len(queries)), key=queries.__getitem__)
    ans = [0] * len(queries)

    pos = 1       # first 'pos' terms are already accounted for
    cur = 1       # a_pos, and pos is always odd here
    pref = 1      # sum of first pos terms modulo MOD
    qi = 0

    for i in range(1, len(fail)):
        block_len = fail[i] - fail[i - 1] - 1
        if block_len <= 0:
            continue

        start = fail[i - 1] + 1
        block_end_pos = pos + 2 * block_len
        start_mod = start % MOD

        # Answer queries lying inside this block.
        while qi < len(order) and queries[order[qi]] <= block_end_pos:
            n = queries[order[qi]]
            delta = n - pos
            k = delta // 2

            cur_k, add_k = advance(cur, start_mod, k)
            res = (pref + add_k) % MOD

            if delta & 1:
                # One extra even-indexed term:
                # x_k + (start + k)
                extra = (cur_k + start_mod + (k % MOD)) % MOD
                res = (res + extra) % MOD

            ans[order[qi]] = res
            qi += 1

        if qi == len(order):
            break

        # Consume the whole block.
        cur, add_full = advance(cur, start_mod, block_len)
        pref = (pref + add_full) % MOD
        pos = block_end_pos

    return ans


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    queries = [int(x) for x in data[1:1 + t]]
    out = solve(queries)
    sys.stdout.write("\n".join(map(str, out)))


if __name__ == "__main__":
    main()