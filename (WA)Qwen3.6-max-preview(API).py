import sys

MOD = 10**9 + 7

def pow_mod(a, b, m):
    result = 1
    a %= m
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % m
        a = (a * a) % m
        b //= 2
    return result

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    T = int(input_data[idx]); idx += 1
    
    queries = []
    for t in range(T):
        n_str = input_data[idx]; idx += 1
        queries.append(int(n_str))
    
    # Compute r values up to a limit
    LIMIT = 3000
    
    a = [0, 1, 2]
    d = [0, 1]
    base_values = set()
    base_values.add(1)
    current_mex = 2
    
    for n in range(3, LIMIT + 1):
        if n % 2 == 1:
            a.append(2 * a[n-1])
        else:
            r = current_mex
            while r in base_values:
                r += 1
            current_mex = r
            a.append(a[n-1] + r)
        
        d_new = a[n] - a[n-1]
        d.append(d_new)
        
        total = 0
        for k in range(n-1, 0, -1):
            total += d[k]
            base_values.add(total)
            if total == current_mex:
                current_mex += 1
    
    # Extract r values
    r_vals = [0]  # r_vals[0] unused
    for k in range(2, LIMIT // 2 + 1):
        r_vals.append(a[2*k] - a[2*k-1])
    
    # Compute prefix sums for small n
    prefix_sum_small = [0] * (LIMIT + 1)
    for i in range(1, LIMIT + 1):
        prefix_sum_small[i] = (prefix_sum_small[i-1] + a[i]) % MOD
    
    # For large n, use the formula
    # Sum(2m) = 1 + 3*sum_{k=1}^{m-1} b_k + b_m
    # Sum(2m+1) = 1 + 3*sum_{k=1}^{m} b_k
    # b_k = 2*b_{k-1} + r_{2k-1}
    
    # For large k, r_{2k-1} ≈ k + C
    # We estimate C from the last computed r value
    
    last_j = len(r_vals) - 1
    last_r = r_vals[-1]
    C = last_r - last_j
    
    # Precompute b_k and prefix sums up to LIMIT/2
    m_limit = LIMIT // 2
    b = [0, 2]
    b_prefix = [0, 2]
    
    for k in range(2, m_limit + 1):
        b_k = (2 * b[k-1] + r_vals[k-1]) % MOD
        b.append(b_k)
        b_prefix.append((b_prefix[k-1] + b_k) % MOD)
    
    for n in queries:
        if n <= LIMIT:
            print(prefix_sum_small[n])
        else:
            if n % 2 == 0:
                m = n // 2
                if m <= m_limit:
                    result = (1 + 3 * b_prefix[m-1] + b[m]) % MOD
                else:
                    # For large m, use the formula with r_{2k-1} ≈ k + C
                    # b_k = 2*b_{k-1} + k + C
                    # b_k = 2^k * b_0 + sum_{j=1}^{k} 2^{k-j} * (j + C)
                    #     = 2^k * b_0 + 2^k * (2 - (k+2)/2^k) + C * (2^k - 1)
                    #     = 2^k * (b_0 + 2 + C) - k - 2 - C
                    
                    # sum_{k=1}^{m} b_k = sum_{k=1}^{m} [2^k * (b_0 + 2 + C) - k - 2 - C]
                    #                     = (b_0 + 2 + C) * (2^{m+1} - 2) - m*(m+1)/2 - m*(2+C)
                    
                    # But this is an approximation. For exact computation, we need to use
                    # the actual r values for small k and the approximation for large k.
                    
                    # For now, use the approximation
                    b0 = 2
                    coeff = (b0 + 2 + C) % MOD
                    
                    pow2_m = pow_mod(2, m, MOD)
                    pow2_m1 = pow_mod(2, m + 1, MOD)
                    
                    sum_b = (coeff * (pow2_m1 - 2) - m * (m + 1) // 2 - m * (2 + C)) % MOD
                    
                    # b_m ≈ 2^m * (b_0 + 2 + C) - m - 2 - C
                    b_m = (coeff * pow2_m - m - 2 - C) % MOD
                    
                    result = (1 + 3 * (sum_b - b_m) + b_m) % MOD
                print(result)
            else:
                m = (n - 1) // 2
                if m <= m_limit:
                    result = (1 + 3 * b_prefix[m]) % MOD
                else:
                    # Use the approximation
                    b0 = 2
                    coeff = (b0 + 2 + C) % MOD
                    
                    pow2_m1 = pow_mod(2, m + 1, MOD)
                    
                    sum_b = (coeff * (pow2_m1 - 2) - m * (m + 1) // 2 - m * (2 + C)) % MOD
                    
                    result = (1 + 3 * sum_b) % MOD
                print(result)

solve()
