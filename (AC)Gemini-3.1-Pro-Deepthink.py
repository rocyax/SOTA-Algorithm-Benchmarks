import sys

def solve():
    # Defend against Integer string conversion length limits on modern Python 3 updates
    try:
        sys.set_int_max_str_digits(200000)
    except AttributeError:
        pass

    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    T = int(input_data[0])
    queries = input_data[1:T+1]
    
    MOD = 10**9 + 7
    MOD_MINUS_1 = MOD - 1
    inv2 = (MOD + 1) // 2
    
    # 1. Precomputations Phase (Calculated once in ~0.05s)
    a = [0, 1, 2]
    S = {1}
    r = 1
    S_add = S.add
    
    for i in range(3, 681):
        if i % 2 == 1:
            nxt = 2 * a[-1]
        else:
            while r in S:
                r += 1
            nxt = a[-1] + r
            r += 1 
            
        for j in range(1, i):
            S_add(nxt - a[j])
        a.append(nxt)
        
    M_set = S.copy()
    # Exclude elements structurally of the step form a[2k] - a[2k-1] 
    for k in range(1, 341):
        M_set.discard(a[2*k] - a[2*k-1])
        
    MAX_VAL = 10**100
    M_full = sorted([x for x in M_set if x <= MAX_VAL])
    
    L = len(M_full)
    pref_M = [0] * (L + 1)
    pref_pow = [0] * (L + 1)
    
    # Form layout prefix boundaries limits
    for i in range(L):
        pref_M[i+1] = (pref_M[i] + M_full[i]) % MOD
        exp = (M_full[i] - i - 1) % MOD_MINUS_1
        pref_pow[i+1] = (pref_pow[i] + pow(inv2, exp, MOD)) % MOD
        
    def V(x):
        return ((x + 2) % MOD) * pow(inv2, x % MOD_MINUS_1, MOD) % MOD

    out = []
    
    # 2. Query Sum Math Evaluations O(log |M|)
    for q_str in queries:
        N = int(q_str)
        if N == 1:
            out.append("1")
            continue
        if N == 2:
            out.append("3")
            continue
            
        K = N // 2
        
        # O(log |M|) bounds narrowing determining exact skip intervals
        low = 0
        high = L
        while low < high:
            mid = (low + high + 1) // 2
            if M_full[mid - 1] - mid <= K:
                low = mid
            else:
                high = mid - 1
                
        E = low
        X_K = K + E
        
        # S2 = Mathematical aggregation of R_i bounds up to limits
        S2 = (X_K % MOD) * ((X_K + 1) % MOD) % MOD * inv2 % MOD
        S2 = (S2 - pref_M[E]) % MOD
        
        # ans_S1 represents the telescoping summation (R_i * 2^{K-i}) evaluated precisely 
        simp = (2 + pref_pow[E]) % MOD
        simp = (simp - pow(2, E % MOD_MINUS_1, MOD) * V(X_K)) % MOD
        
        exp2_K_minus_1 = pow(2, (K - 1) % MOD_MINUS_1, MOD)
        exp2_K = (exp2_K_minus_1 * 2) % MOD
        
        ans_S1 = simp * exp2_K % MOD
        
        # Target representation equivalents resolved relative to parity 
        b_K = (exp2_K_minus_1 + ans_S1) % MOD
        sum_b = (2 * b_K - 1 - S2) % MOD
        
        if N % 2 == 0:
            sum_b_prev = (sum_b - b_K) % MOD
            ans = (1 + 3 * sum_b_prev + b_K) % MOD
        else:
            ans = (1 + 3 * sum_b) % MOD
            
        out.append(str((ans % MOD + MOD) % MOD))
        
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()