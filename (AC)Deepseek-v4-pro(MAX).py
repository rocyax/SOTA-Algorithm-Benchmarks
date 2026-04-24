import sys

MOD = 1_000_000_007
INV2 = (MOD + 1) // 2  # modular inverse of 2


def build_fail(limit):
    """Build the fail set for values up to `limit`.

    Returns a sorted list of fail values (differences that are NOT special/b-values).
    The list starts with 0 and ends with limit+1 as sentinels.
    """
    a = [1, 2]           # sequence terms
    diffs = {0, 1}        # all differences seen so far
    special = {1}         # b_k = a_{2k} - a_{2k-1}
    mex = 0               # current mex (monotonic)

    # Build terms until we have an even-length sequence exceeding limit
    while len(a) % 2 == 1 or a[-1] <= limit:
        n = len(a) + 1
        if n & 1:  # odd index
            new_val = a[-1] * 2
        else:      # even index
            while mex in diffs:
                mex += 1
            new_val = a[-1] + mex
            special.add(mex)

        for old in a:
            diffs.add(new_val - old)
        a.append(new_val)

    # Collect fail values: differences <= limit that are NOT special (b-values)
    fail = [x for x in diffs if 0 < x <= limit and x not in special]
    fail.sort()
    fail.insert(0, 0)          # sentinel start
    fail.append(limit + 1)     # sentinel end
    return fail


def advance(cur_mod, start_mod, k):
    """Advance through k complete pairs within a block.

    Args:
        cur_mod: current odd-indexed value (x_0) modulo MOD
        start_mod: first b-value (s) in this block modulo MOD
        k: number of complete pairs to process

    Returns (new_cur_mod, added_mod):
        new_cur_mod: the odd-indexed value after k pairs, modulo MOD
        added_mod: sum of the 2k terms added, modulo MOD
    """
    km = k % MOD
    p2 = pow(2, k, MOD)
    base = (cur_mod + 2 * start_mod + 2) % MOD

    # x_k = 2^k * (x_0 + 2s + 2) - 2k - 2s - 2  (mod MOD)
    new_cur = (p2 * base - 2 * km - 2 * start_mod - 2) % MOD

    # sum = 3*(x_0+2s+2)*(2^k-1) - 3*k*(k+2s+3)/2  (mod MOD)
    term1 = 3 * base * (p2 - 1) % MOD
    term2 = 3 * km * ((km + 2 * start_mod + 3) % MOD) % MOD * INV2 % MOD
    added = (term1 - term2) % MOD

    return new_cur, added


def solve(queries):
    max_n = max(queries)
    limit = max_n

    # Grow limit until we have enough b-values to cover all queries
    while True:
        fail = build_fail(limit)
        good_count = limit - (len(fail) - 2)  # values <= limit that are NOT fail
        if 1 + 2 * good_count >= max_n:
            break
        limit *= 2

    # Sort queries by index to process in order
    order = sorted(range(len(queries)), key=queries.__getitem__)
    ans = [0] * len(queries)

    pos = 1       # number of terms processed so far (a_1 is done)
    cur = 1       # a_1 mod MOD (current odd-indexed value)
    pref = 1      # sum a_1 mod MOD
    qi = 0        # pointer into sorted queries

    # Process blocks of consecutive b-values between fail values
    for i in range(1, len(fail)):
        block_len = fail[i] - fail[i - 1] - 1
        if block_len <= 0:
            continue

        start = fail[i - 1] + 1          # first b-value in this block
        start_mod = start % MOD
        block_end_pos = pos + 2 * block_len  # position after processing all pairs

        # Handle queries that fall within this block
        while qi < len(order) and queries[order[qi]] <= block_end_pos:
            n = queries[order[qi]]
            delta = n - pos          # how many more terms needed
            k = delta // 2           # complete pairs

            cur_k, add_k = advance(cur, start_mod, k)
            res = (pref + add_k) % MOD

            if delta & 1:  # one extra term (even-indexed)
                extra = (cur_k + start_mod + (k % MOD)) % MOD
                res = (res + extra) % MOD

            ans[order[qi]] = res
            qi += 1

        if qi == len(order):
            break

        # Advance to the end of the block
        cur, add_full = advance(cur, start_mod, block_len)
        pref = (pref + add_full) % MOD
        pos = block_end_pos

    return ans


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    queries = [int(x) for x in data[1:1 + t]]
    out = solve(queries)
    sys.stdout.write('\n'.join(map(str, out)))


if __name__ == '__main__':
    main()
