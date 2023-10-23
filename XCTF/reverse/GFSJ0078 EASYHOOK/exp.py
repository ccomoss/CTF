"""
程序逻辑：
    1) flag长度为19字节
    2) WriteFile函数被hook到0x401080（x32dbg调试），实际加解密函数是0x401000
"""

byte_40A030 = [
    0x61, 0x6A, 0x79, 0x67, 0x6B, 0x46, 0x6D, 0x2E, 0x7F, 0x5F, 
  0x7E, 0x2D, 0x53, 0x56, 0x7B, 0x38, 0x6D, 0x4C, 0x6E
]

flag = ['0'] * 19

for i in range(19):
    if i == 18:
        flag[18] = chr(byte_40A030[i] ^ 0x13)
    else:
        tmp_f = byte_40A030[i] ^ i
        if (i % 2):
            flag[i] = chr(tmp_f + i)
        else:
            flag[i+2] = chr(tmp_f)

print(''.join(flag))

