import sys

MOD = 10**9 + 7


def build_non_mex(max_bound):
    a = [None, 1, 2]
    S = {1}
    limit = 2 * max_bound + 10
    j = 2
    while a[-1] <= limit:
        j += 1
        if j % 2 == 1:
            an = 2 * a[-1]
        else:
            r = 1
            while r in S:
                r += 1
            an = a[-1] + r
        for i in range(1, j):
            d = an - a[i]
            if d <= limit:
                S.add(d)
        a.append(an)
    J = j

    non_mex = set()
    non_mex.add(1)
    for k in range(1, J // 2 + 1):
        if 2 * k + 1 <= J and a[2 * k] <= max_bound:
            non_mex.add(a[2 * k])
    for jj in range(3, J + 1):
        for ii in range(1, jj - 1):
            d = a[jj] - a[ii]
            if d <= max_bound:
                non_mex.add(d)
    return sorted(non_mex)


def compute_B(m, non_mex_sorted, inv2):
    if m <= 0:
        return 0
    len_nm = len(non_mex_sorted)
    F_val = 0
    SD_val = 0
    m_limit = m - 1
    for i in range(1, len_nm + 1):
        u_i = non_mex_sorted[i - 1]
        start = u_i - i + 1
        if i < len_nm:
            u_ip1 = non_mex_sorted[i]
            end = u_ip1 - i - 1
        else:
            end = m_limit
        if start > m_limit:
            break
        a_ = start if start >= 1 else 1
        b_ = end if end <= m_limit else m_limit
        if a_ > b_:
            continue
        length = b_ - a_ + 1
        SD_val = (SD_val + i * (length % MOD)) % MOD
        e1 = m - a_ + 1
        e2 = m - b_
        val = (pow(2, e1, MOD) - pow(2, e2, MOD)) % MOD
        F_val = (F_val + i * val) % MOD
    term1 = pow(2, m + 2, MOD)
    term2 = 4 % MOD
    mm = m % MOD
    mp3 = (m + 3) % MOD
    term3 = mm * mp3 % MOD * inv2 % MOD
    B = (term1 - term2 - term3 + F_val - SD_val) % MOD
    return B


def solve():
    data = sys.stdin.buffer.read().split()
    T = int(data[0])
    queries = [int(x) for x in data[1:T + 1]]
    max_n = max(queries)
    non_mex_sorted = build_non_mex(max_n)
    inv2 = pow(2, MOD - 2, MOD)
    out = []
    for n in queries:
        if n == 1:
            out.append('1')
            continue
        if n % 2 == 0:
            m = n // 2
            Bm_1 = compute_B(m - 1, non_mex_sorted, inv2)
            Bm = compute_B(m, non_mex_sorted, inv2)
            ans = (1 + 2 * Bm_1 + Bm) % MOD
        else:
            m = (n - 1) // 2
            Bm = compute_B(m, non_mex_sorted, inv2)
            ans = (1 + 3 * Bm) % MOD
        out.append(str(ans))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    solve()