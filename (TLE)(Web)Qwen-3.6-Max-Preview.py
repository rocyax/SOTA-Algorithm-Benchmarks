import sys

# Set recursion limit just in case, though not used here
sys.setrecursionlimit(2000)

MOD = 10**9 + 7

def mat_mul(A, B):
    """Multiply two 4x4 matrices modulo MOD."""
    C = [[0]*4 for _ in range(4)]
    for i in range(4):
        Ai = A[i]
        Ci = C[i]
        for k in range(4):
            aik = Ai[k]
            if aik == 0:
                continue
            Bk = B[k]
            for j in range(4):
                Ci[j] = (Ci[j] + aik * Bk[j]) % MOD
    return C

def mat_pow(A, p):
    """Compute A^p modulo MOD using binary exponentiation."""
    res = [[0]*4 for _ in range(4)]
    for i in range(4):
        res[i][i] = 1
    base = A
    while p > 0:
        if p & 1:
            res = mat_mul(res, base)
        base = mat_mul(base, base)
        p >>= 1
    return res

def mat_vec_mul(M, V):
    """Multiply 4x4 matrix M by 4x1 vector V modulo MOD."""
    res = [0]*4
    for i in range(4):
        s = 0
        Mi = M[i]
        for j in range(4):
            s = (s + Mi[j] * V[j]) % MOD
        res[i] = s
    return res

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    try:
        T = int(next(it))
    except StopIteration:
        return

    # Precomputed answers for small n
    pre = {1: 1, 2: 3, 3: 7, 4: 15, 5: 31}
    out = []

    for _ in range(T):
        n_str = next(it)
        n = int(n_str)
        
        if n <= 5:
            out.append(str(pre[n]))
            continue

        K = n // 2
        
        # Base state at k=3: [a_6, k, 1, S_6]
        # a_6 = 21, S_6 = 52
        V = [21, 3, 1, 52]
        cur_k = 3
        
        m = 1
        # Process blocks until we reach the target pair index K
        while cur_k < K:
            if m == 1:
                start, length, C = 3, 1, 6
            elif m == 2:
                start, length, C = 4, 6, 6
            else:
                # For m >= 3, boundaries follow powers of 2
                start = (1 << (m + 1)) - 6
                length = (1 << (m + 1))
                C = m + 4
            
            end = start + length - 1
            
            # Determine overlap between current block and remaining steps [cur_k, K-1]
            low = max(cur_k, start)
            high = min(K - 1, end)
            
            if low <= high:
                steps = high - low + 1
                C_mod = C % MOD
                
                # Transition matrix for r_{2k} = k + C
                # [a_{2(k+1)}]   [2 1 C 0] [a_{2k}]
                # [k+1       ] = [0 1 1 0] [k    ]
                # [1         ]   [0 0 1 0] [1    ]
                # [S_{2(k+1)}]   [4 1 C 1] [S_{2k}]
                M = [
                    [2, 1, C_mod, 0],
                    [0, 1, 1, 0],
                    [0, 0, 1, 0],
                    [4, 1, C_mod, 1]
                ]
                
                Mp = mat_pow(M, steps)
                V = mat_vec_mul(Mp, V)
                cur_k = high + 1
            
            m += 1
            # Safety break if blocks overshoot (shouldn't happen with correct logic)
            if start > K and cur_k < K:
                break

        ans = V[3]  # S_{2K}
        if n % 2 == 1:
            # If n is odd, add a_n = a_{2K+1} = 2 * a_{2K}
            ans = (ans + 2 * V[0]) % MOD
            
        out.append(str(ans))
        
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()