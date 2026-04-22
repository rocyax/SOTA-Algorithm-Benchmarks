import time
MOD = 10**9+7
inv2 = (MOD+1)//2
phi = MOD-1

# generate some large exponents
exps = [10**100 + i for i in range(200000)]

t0 = time.time()
for e in exps:
    pow(inv2, e, MOD)
t1 = time.time()
print('full exp', t1-t0)

t0 = time.time()
for e in exps:
    pow(inv2, e % phi, MOD)
t1 = time.time()
print('reduced exp', t1-t0)
