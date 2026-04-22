import sys

# Increase recursion depth just in case
sys.setrecursionlimit(2000)

MOD = 10**9 + 7

def mat_mul(A, B):
    C = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            s = 0
            for k in range(4):
                s += A[i][k] * B[k][j]
            C[i][j] = s % MOD
    return C

def solve():
    input_data = sys.stdin.read().split()
    if not input_
        return
    
    iterator = iter(input_data)
    try:
        T_str = next(iterator)
        T = int(T_str)
    except StopIteration:
        return

    # Transition matrices derived for Chiaki Sequence sum
    # State vector V_k = [a_k, a_{k+1}, S_k, S_{k+1}]^T
    # For bit 0: transition k -> 2k
    M0 = [
        [2, 0, 0, 0],
        [0, 4, 0, 0],
        [1, 0, 2, 0],
        [0, 1, 0, 2]
    ]
    
    # For bit 1: transition k -> 2k+1
    M1 = [
        [0, 2, 0, 0],
        [0, 4, 0, 0],
        [0, 1, 2, 1],
        [0, 2, 0, 2]
    ]

    out = []
    for _ in range(T):
        n_str = next(iterator)
        n = int(n_str)
        if n == 0:
            out.append("0")
            continue
        if n == 1:
            out.append("1")
            continue
            
        # Binary representation of n
        b_str = bin(n)[2:]
        
        # Initial state for k=1: [a_1, a_2, S_1, S_2] = [1, 2, 1, 3]
        # We represent it as a column vector [1, 2, 1, 3]
        # We will apply matrices for each bit after the leading 1
        current = [1, 2, 1, 3]
        
        for bit in b_str[1:]:
            # Multiply current state by matrix
            M = M0 if bit == '0' else M1
            
            new_current = [0]*4
            for i in range(4):
                s = 0
                for j in range(4):
                    s += M[i][j] * current[j]
                new_current[i] = s % MOD
            current = new_current
            
        # The answer is S_n, which is the 3rd element (index 2) of the state vector
        out.append(str(current[2]))
        
    print("\n".join(out))

if __name__ == '__main__':
    solve()