from bisect import bisect_right
import sys

MOD = 10**9 + 7
INV2 = (MOD + 1) // 2


def advance_block(x_prev, x_sum_prev, m, offset, steps):
    if steps <= 0:
        return x_prev, x_sum_prev

    pow2 = pow(2, steps, MOD)
    steps_mod = steps % MOD
    mc = (m + offset) % MOD

    x_now = (
        pow2 * x_prev
        + mc * (pow2 - 1)
        + (2 * pow2 - steps_mod - 2)
    ) % MOD

    block_sum = ((x_prev + mc + 2) % MOD) * ((2 * pow2 - 2) % MOD)
    block_sum -= steps_mod * ((mc + 2) % MOD)
    block_sum -= steps_mod * ((steps_mod + 1) % MOD) * INV2
    x_sum_now = (x_sum_prev + block_sum) % MOD

    return x_now, x_sum_now


def build_bad_and_states(limit_k):
    if limit_k <= 1:
        return [], [], [], []

    extra = 2 * (limit_k.bit_length() + 5) ** 2 + 20
    bound = limit_k + extra

    while True:
        terms = [1, 2]
        bad_set = set()
        bad_vals = []

        candidate = 2
        x_prev = 2

        while x_prev <= bound:
            odd_term = x_prev * 2

            for v in terms:
                bad = odd_term - v
                if bad not in bad_set:
                    bad_set.add(bad)
                    bad_vals.append(bad)

            while candidate in bad_set:
                candidate += 1
            gap = candidate
            candidate += 1

            even_term = odd_term + gap
            for v in terms:
                bad = even_term - v
                if bad not in bad_set:
                    bad_set.add(bad)
                    bad_vals.append(bad)

            terms.append(odd_term)
            terms.append(even_term)
            x_prev = even_term

        bad_vals.sort()
        chosen_upto_bound = bound - bisect_right(bad_vals, bound)
        if chosen_upto_bound >= limit_k:
            break
        bound *= 2

    shifted = [q - i - 1 for i, q in enumerate(bad_vals)]

    states = []
    if bad_vals:
        states = [(2, 2)] * len(bad_vals)
        x_cur, x_sum_cur = 2, 2
        for j in range(1, len(bad_vals)):
            steps = bad_vals[j] - bad_vals[j - 1] - 1
            m = bad_vals[j - 1] - j
            x_cur, x_sum_cur = advance_block(x_cur, x_sum_cur, m, j, steps)
            states[j] = (x_cur, x_sum_cur)

    return bad_vals, shifted, states


def get_even_term_and_prefix_sum(k, bad_vals, shifted, states):
    if k == 1:
        return 2, 2

    skipped = bisect_right(shifted, k)
    x_prev, x_sum_prev = states[skipped - 1]
    m = bad_vals[skipped - 1] - skipped
    steps = k - m
    return advance_block(x_prev, x_sum_prev, m, skipped, steps)


def solve_one(n, bad_vals, shifted, states):
    if n == 1:
        return 1

    k = n // 2
    even_term, even_prefix_sum = get_even_term_and_prefix_sum(k, bad_vals, shifted, states)

    if n & 1:
        return (1 + 3 * even_prefix_sum) % MOD

    if k == 1:
        prev_prefix_sum = 0
    else:
        prev_prefix_sum = get_even_term_and_prefix_sum(k - 1, bad_vals, shifted, states)[1]
    return (1 + 3 * prev_prefix_sum + even_term) % MOD


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    nums = [int(x) for x in data[1:1 + t]]

    max_k = 1
    for n in nums:
        if n > 1:
            max_k = max(max_k, n // 2)

    bad_vals, shifted, states = build_bad_and_states(max_k)

    out = [str(solve_one(n, bad_vals, shifted, states)) for n in nums]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()