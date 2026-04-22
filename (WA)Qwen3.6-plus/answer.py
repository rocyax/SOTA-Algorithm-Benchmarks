import sys

def solve():
    MOD = 10**9 + 7
    raw = sys.stdin.buffer.read()
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    data = raw.split()
    if not data:
        return
    T = int(data[0])

    N = 2000
    a = [0] * N
    a[0] = 1
    if N > 1:
        a[1] = 2

    MAX_DIFF = 500000
    is_diff = bytearray(MAX_DIFF + 2)
    is_diff[1] = 1
    mex = 1

    for i in range(2, N):
        if (i + 1) & 1:
            ai = a[i - 1] * 2
            for j in range(i):
                d = ai - a[j]
                if d <= MAX_DIFF:
                    is_diff[d] = 1
                    if d == mex:
                        while is_diff[mex]:
                            mex += 1
            a[i] = ai
        else:
            while mex <= MAX_DIFF and is_diff[mex]:
                mex += 1
            r = mex
            ai = a[i - 1] + r
            for j in range(i):
                d = ai - a[j]
                if d <= MAX_DIFF:
                    is_diff[d] = 1
            a[i] = ai

    S_mod = [0] * N
    S_mod[0] = 1
    for i in range(1, N):
        S_mod[i] = (S_mod[i - 1] + a[i] % MOD) % MOD

    inv2 = pow(2, MOD - 2, MOD)

    d_vals = []
    max_k = (N - 1) // 2 - 1
    for k in range(1, max_k + 1):
        dk = a[2 * k + 1] - 2 * a[2 * k - 1]
        d_vals.append(dk)

    C_mod = 0
    inv2_k = inv2
    for dk in d_vals:
        C_mod = (C_mod + dk * inv2_k) % MOD
        inv2_k = inv2_k * inv2 % MOD

    L_mod = (4 + 2 * C_mod) % MOD
    half = inv2
    TWO_PHI = 2 * (MOD - 1)

    results = []
    for i in range(T):
        ns = data[i + 1]
        if isinstance(ns, bytes):
            ns = ns.decode()

        ns_len = len(ns)
        if ns_len <= 3:
            n = int(ns)
            results.append(str(S_mod[n - 1] if n < N else str(S_mod[N - 1])))
            continue
        elif ns_len == 4:
            n = int(ns)
            if n < N:
                results.append(str(S_mod[n - 1]))
                continue

        n_is_odd = int(ns[-1]) % 2

        n_mod = 0
        n_mod_2phi = 0
        for ch in ns:
            d = ord(ch) - 48
            n_mod = (n_mod * 10 + d) % MOD
            n_mod_2phi = (n_mod_2phi * 10 + d) % TWO_PHI

        m_mod = ((n_mod - (1 if n_is_odd else 0) + MOD) % MOD) * half % MOD
        m_mod_2phi = (n_mod_2phi - (1 if n_is_odd else 0)) // 2

        two_m = pow(2, m_mod_2phi, MOD)
        m_sq = m_mod * m_mod % MOD
        correction = 3 * m_sq % MOD * half % MOD

        if not n_is_odd:
            result = (L_mod * two_m % MOD - correction - 5) % MOD
        else:
            A_m = (two_m + two_m * half % MOD * C_mod % MOD) % MOD
            S_2m = (L_mod * two_m % MOD - correction - 5) % MOD
            result = (S_2m + 2 * A_m % MOD) % MOD

        results.append(str(result))

    sys.stdout.write('\n'.join(results) + '\n')

solve()
