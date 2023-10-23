"""
使用ILSpy反编译.NET程序
"""
import hashlib

array = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
	31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
	73, 79, 83, 89, 97, 101, 103, 107, 109, 113
]

strr = "CreateByTenshine"

A_2 = ""

for cr in strr:
    num2 = 1
    c = ord(cr)
    while num2 < 15:
        c = array[num2] ^ c
        num2 += 1
    A_2 += chr(c)

print("flag{" + hashlib.md5(A_2.encode()).hexdigest().upper() + "}")
