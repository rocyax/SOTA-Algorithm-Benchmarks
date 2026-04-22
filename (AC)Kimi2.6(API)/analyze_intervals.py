def generate(N):
    a=[0,1,2]
    diffs=set([1])
    for n in range(3,N+1):
        if n&1:
            a.append(2*a[-1])
        else:
            r=1
            while r in diffs:
                r+=1
            a.append(a[-1]+r)
        for i in range(1,n):
            diffs.add(a[n]-a[i])
    return a, diffs

a, diffs = generate(670)
B = 10**100
diag=set()
max_t = len(a)//2
for t in range(1, max_t+1):
    diag.add(a[2*t]-a[2*t-1])
U = sorted([x for x in diffs if x not in diag and x <= B])
Z = [u - i - 1 for i,u in enumerate(U)]
print('len U', len(U))
print('len set(Z)', len(set(Z)))
print('Z[:20]', Z[:20])
print('gaps in Z', sum(1 for i in range(1,len(Z)) if Z[i]>Z[i-1]))

# count empty vs non-empty intervals
empty = 0
nonempty = 1  # j=0
for j in range(1, len(U)):
    if Z[j] > Z[j-1]:
        nonempty += 1
    else:
        empty += 1
print('nonempty', nonempty, 'empty', empty)
