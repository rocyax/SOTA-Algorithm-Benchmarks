MOD = 10**9 + 7

def brute(n):
    a = [0, 1, 2]
    diffs = {1}
    for idx in range(3, n + 1):
        if idx & 1:
            a.append(2 * a[-1])
        else:
            r = 1
            while r in diffs:
                r += 1
            a.append(a[-1] + r)
        for i in range(1, idx):
            diffs.add(a[idx] - a[i])
    return sum(a[1:n+1]) % MOD

print(brute(500))
