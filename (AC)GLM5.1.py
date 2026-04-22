import sys
from bisect import bisect_right

MOD = 10**9 + 7
inv2 = (MOD + 1) // 2

def solve():
    data = sys.stdin.read().split()
    T = int(data[0])
    ns = [data[i+1] for i in range(T)]
    
    max_n = 0
    for s in ns:
        v = int(s)
        if v > max_n:
            max_n = v
    
    K_max = max_n // 2 + 1
    
    if K_max < 100:
        N_max = 40
    elif K_max < 10**6:
        N_max = 100
    elif K_max < 10**9:
        N_max = 200
    elif K_max < 10**12:
        N_max = 400
    else:
        N_max = 700
    
    max_island_val = K_max + 500000
    
    a = [0] * (N_max + 1)
    a[1] = 1
    a[2] = 2
    
    track_limit = N_max + 2000
    small_diffs = set()
    small_diffs.add(1)
    
    for n in range(3, N_max + 1):
        r = 1
        while r in small_diffs:
            r += 1
        if n % 2 == 1:
            a[n] = 2 * a[n-1]
        else:
            a[n] = a[n-1] + r
        for i in range(1, n):
            d = a[n] - a[i]
            if d <= track_limit:
                small_diffs.add(d)
    
    even_consec = set()
    for k in range(1, N_max // 2 + 1):
        j = 2 * k
        if j <= N_max:
            even_consec.add(a[j] - a[j-1])
    
    island_set = set()
    for j in range(2, N_max + 1):
        for i in range(j-1, 0, -1):
            d = a[j] - a[i]
            if d > max_island_val:
                break
            if d not in even_consec:
                island_set.add(d)
    
    sorted_islands = sorted(island_set)
    
    prefix_sum = [0] * (N_max + 2)
    for i in range(1, N_max + 1):
        prefix_sum[i] = (prefix_sum[i-1] + a[i]) % MOD
    
    K_init = 3
    B_init = a[2 * K_init] % MOD
    S_init = prefix_sum[2 * K_init] % MOD
    
    all_d_init = set()
    for j in range(2, 2*K_init+1):
        for i in range(1, j):
            all_d_init.add(a[j] - a[i])
    mex_init = 1
    while mex_init in all_d_init:
        mex_init += 1
    
    # Precompute the full profile: at each event, store (k_after, B, S, mex)
    # An event = stretch + island encounter
    # After the event, k = ev_k + 1, B and S are updated, mex = ev_new_mex
    
    profile_k = [K_init]  # k values at each profile point
    profile_B = [B_init]
    profile_S = [S_init]
    profile_mex = [mex_init]
    
    k = K_init
    B = B_init
    S = S_init
    mex = mex_init
    
    while True:
        idx = bisect_right(sorted_islands, mex) - 1
        # Find next island > mex
        idx2 = idx + 1
        while idx2 < len(sorted_islands) and sorted_islands[idx2] <= mex:
            idx2 += 1
        
        if idx2 >= len(sorted_islands):
            break
        
        next_island = sorted_islands[idx2]
        steps = next_island - mex - 1
        
        if steps > 0:
            t = steps
            mm = mex % MOD
            alpha = (B + mm + 1) % MOD
            two_t = pow(2, t, MOD)
            B = (alpha * two_t - mm - t % MOD - 1) % MOD
            tm = t % MOD
            S = (S + 4 * alpha % MOD * (two_t - 1) % MOD
                 - 3 * tm * mm % MOD
                 - 2 * tm
                 - tm * ((3 * t + 1) % MOD) % MOD * inv2) % MOD
            mex = mex + t
            k = k + t
        
        old_mex = mex
        S = (S + 4 * B + old_mex % MOD) % MOD
        B = (2 * B + old_mex % MOD) % MOD
        
        mex = old_mex + 1
        while mex in island_set:
            mex += 1
        
        k += 1
        
        profile_k.append(k)
        profile_B.append(B)
        profile_S.append(S)
        profile_mex.append(mex)
        
        if k > K_max + 10:
            break
    
    # For each test case
    for n_str in ns:
        n = int(n_str)
        K = n // 2
        is_odd = n % 2 == 1
        
        if n <= N_max:
            print(prefix_sum[n] % MOD)
            continue
        
        # Binary search in profile to find the last entry with k <= K
        idx = bisect_right(profile_k, K) - 1
        
        B = profile_B[idx]
        S = profile_S[idx]
        mex = profile_mex[idx]
        k = profile_k[idx]
        
        # Fast-forward from k to K
        if k < K:
            t = K - k
            mm = mex % MOD
            alpha = (B + mm + 1) % MOD
            two_t = pow(2, t, MOD)
            B = (alpha * two_t - mm - t % MOD - 1) % MOD
            tm = t % MOD
            S = (S + 4 * alpha % MOD * (two_t - 1) % MOD
                 - 3 * tm * mm % MOD
                 - 2 * tm
                 - tm * ((3 * t + 1) % MOD) % MOD * inv2) % MOD
        
        if is_odd:
            ans = (S + 2 * B) % MOD
        else:
            ans = S % MOD
        
        print(ans % MOD)

solve()
