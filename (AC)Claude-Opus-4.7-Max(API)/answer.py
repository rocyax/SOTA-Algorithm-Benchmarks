import sys
from bisect import bisect_right


def solve():
    MOD = 10**9 + 7
    MOD_M1 = MOD - 1
    inv2 = (MOD + 1) // 2

    data = sys.stdin.buffer.read().split()
    if not data:
        return
    T = int(data[0])
    queries = [int(x) for x in data[1:T + 1]]
    if not queries:
        return

    max_n = max(queries)

    a_seq = [None, 1, 2]
    S = {1}
    max_bound = max_n
    LIMIT_S = 1 << 25

    N_CAP = 800
    j = 2
    while j < N_CAP:
        j += 1
        if j % 2 == 1:
            an = 2 * a_seq[j - 1]
        else:
            r = 1
            while r in S:
                r += 1
            an = a_seq[j - 1] + r
        a_seq.append(an)
        for i in range(1, j):
            d = an - a_seq[i]
            if d <= LIMIT_S:
                S.add(d)
        if a_seq[j - 1] > 2 * max_bound and a_seq[j] > 2 * max_bound:
            break

    N = len(a_seq) - 1

    mex_pairs = set()
    for k in range(1, (N - 1) // 2 + 1):
        if 2 * k + 2 <= N:
            mex_pairs.add((2 * k + 1, 2 * k + 2))

    non_mex = set()
    for j2 in range(2, N + 1):
        aj = a_seq[j2]
        for i in range(1, j2):
            if (i, j2) in mex_pairs:
                continue
            d = aj - a_seq[i]
            if d <= max_bound:
                non_mex.add(d)

    U = sorted(non_mex)
    len_U = len(U)

    a_arr = [0] * (len_U + 2)
    W = [0] * (len_U + 2)
    for i in range(1, len_U + 1):
        u = U[i - 1]
        a_arr[i] = u - i + 1
        exp = (i - u) % MOD_M1
        W[i] = pow(2, exp, MOD)

    S_W = [0] * (len_U + 2)
    for i in range(1, len_U + 1):
        S_W[i] = (S_W[i - 1] + W[i]) % MOD

    P_2 = [0] * (len_U + 2)
    for k in range(1, len_U):
        P_2[k] = (P_2[k - 1] + k * (U[k] - U[k - 1] - 1)) % MOD

    def compute_B(m):
        if m <= 0:
            return 0
        M = m - 1
        pow_m = pow(2, m % MOD_M1, MOD)
        if M <= 0:
            D1 = 0
            D2 = 0
        else:
            I = bisect_right(a_arr, M, 1, len_U + 1) - 1
            if I < 1:
                D1 = 0
                D2 = 0
            else:
                if I < len_U and a_arr[I + 1] == M + 1:
                    diff_w = (S_W[I] - I * W[I + 1]) % MOD
                    D1 = pow_m * diff_w % MOD
                    u_I = U[I - 1]
                    u_I1 = U[I]
                    D2 = (P_2[I - 1] + I * (u_I1 - u_I - 1)) % MOD
                else:
                    D1 = (pow_m * S_W[I] - 2 * I) % MOD
                    u_I = U[I - 1]
                    D2 = (P_2[I - 1] + I * ((m - u_I + I - 1) % MOD)) % MOD

        term1 = pow(2, (m + 2) % MOD_M1, MOD)
        mm = m % MOD
        mp3 = (m + 3) % MOD
        term3 = mm * mp3 % MOD * inv2 % MOD
        B = (term1 - 4 - term3 + D1 - D2) % MOD
        return B

    out = []
    for n in queries:
        if n == 1:
            out.append('1')
            continue
        if n % 2 == 0:
            m = n // 2
            ans = (1 + 2 * compute_B(m - 1) + compute_B(m)) % MOD
        else:
            m = (n - 1) // 2
            ans = (1 + 3 * compute_B(m)) % MOD
        out.append(str(ans))

    sys.stdout.write('\n'.join(out) + '\n')


solve()
