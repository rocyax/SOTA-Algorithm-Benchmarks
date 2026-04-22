import sys
import math

MOD = 10**9 + 7

# Global cache for the telescoping sum to ensure batch queries run near O(1)
# prefix_T_sum[M] = sum_{m=1}^{M} (m+1) * 2^{-T_m} % MOD
prefix_T_sum = [0]
current_max_M = 0

def get_S(N):
    global current_max_M, prefix_T_sum
    
    if N == 1:
        return 1
    if N == 2:
        return 3
        
    k = N // 2
    
    # 1. Find block M: M is the integer where T_{M-1} < k <= T_M
    # T_M = M(M+1)/2
    M = (math.isqrt(8 * k + 1) - 1) // 2
    if M * (M + 1) // 2 < k:
        M += 1
        
    M_minus_1 = M - 1
    
    # 2. Compute sum_{i=1}^k R_i
    # Sum over full blocks 1 to M-1
    sum_m3 = pow(M_minus_1 * M // 2, 2, MOD)
    sum_m2 = M_minus_1 * M * (2 * M - 1) // 6 % MOD
    sum_m = M_minus_1 * M // 2 % MOD
    
    full_blocks_sum = (sum_m3 + (sum_m2 - sum_m) * pow(2, MOD - 2, MOD)) % MOD
    
    # Sum over the partial M-th block
    rem = k - (M_minus_1 * M // 2)
    partial_sum = (rem * pow(M, 2, MOD) + rem * (rem - 1) // 2) % MOD
    
    total_R_sum = (full_blocks_sum + partial_sum) % MOD
    
    # 3. Compute the dynamically cached telescoping sum for a_{2k}
    while current_max_M < M - 1:
        current_max_M += 1
        m = current_max_M
        T_m = m * (m + 1) // 2
        
        # term = (m + 1) * 2^{-T_m}
        inv_2_Tm = pow(2, MOD - 1 - (T_m % (MOD - 1)), MOD)
        term = ((m + 1) * inv_2_Tm) % MOD
        
        prefix_T_sum.append((prefix_T_sum[-1] + term) % MOD)
        
    telescoping_sum = prefix_T_sum[M - 1]
    
    # 4. Compute a_{2k}
    pow_2_k = pow(2, k, MOD)
    pow_2_k_minus_1 = pow(2, k - 1, MOD)
    
    a_2k = (5 * pow_2_k_minus_1 - pow(M, 2, MOD) - rem - 1 + pow_2_k * telescoping_sum) % MOD
    a_2k = (a_2k + MOD) % MOD
    
    # 5. Finalize S(N) mapping parity equations
    if N % 2 == 0:
        ans = (4 * a_2k - 3 * total_R_sum - 2) % MOD
    else:
        ans = (6 * a_2k - 3 * total_R_sum - 2) % MOD
        
    return (ans + MOD) % MOD

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    T = int(input_data[0])
    queries = [int(x) for x in input_data[1:T+1]]
    
    out = []
    for n in queries:
        out.append(str(get_S(n)))
        
    print('\n'.join(out))

if __name__ == '__main__':
    solve()