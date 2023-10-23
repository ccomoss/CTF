"""
1. 有nsPack壳，脱之
2. 程序逻辑:
    1) flag长度42字节
    2) flag与byte_402130异或的结果是dword_402150
"""

byte_402130 = "this_is_not_flag"
dword_402150 = [
      18,
  4,
  8,
  20,
  36,
  92,
  74,
  61,
  86,
  10,
  16,
  103,
  0,
  65,
  0,
  1,
  70,
  90,
  68,
  66,
  110,
  12,
  68,
  114,
  12,
  13,
  64,
  62,
  75,
  95,
  2,
  1,
  76,
  94,
  91,
  23,
  110,
  12,
  22,
  104,
  91,
  18
]

assert(len(byte_402130) == 16)
assert(len(dword_402150) == 42)

flag = ""
for i in range(42):
    flag += chr(ord(byte_402130[i%16]) ^ dword_402150[i])

print(flag)
