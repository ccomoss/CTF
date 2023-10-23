"""
flag满足三个条件:
1) 一共20行
2) 形似杨辉三角(check 1)
    a0 = 0
    a1+a2 = 2
    a3+a4+a5 = 4
    a6+a7+a8+a9 = 8
    a10+a11+a12+a13+a14 = 16
    a15+a16+a17+a18+a19+a20 = 32
3) 就是杨辉三角(check 2)
"""
import hashlib

LEN = 20
yanghui = [[1],]

for idx in range(1, LEN):
    tmp = []
    for i in range(idx+1):
        if i == 0 or i == (idx):
            tmp.append(1)
        else:
            tmp.append(yanghui[idx-1][i-1] + yanghui[idx-1][i])
    
    yanghui.append(tmp)

# for i in range(LEN):
#     print(yanghui[i])

res = ''
for l in yanghui:
    for n in l:
        res += str(n)
print(res)
print(hashlib.md5(res.encode()).hexdigest())

