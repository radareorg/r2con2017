e asm.arch = arm
e asm.cpu = cortex
e asm.bits = 16

e bin.baddr = 0x80000000

f boot = 0x80000000
f system = 0x8000c000
# allocate secondary tcram (faster and non-executable)
S 0 0x10000000 0 256K tcram rw-
# allocate secondary tcram (faster and non-executable)
S 0 0x40000000 0 256K iodev rw-
# allocate cortex peripherals region
S 0 0xe0000000 0 256K cortex rw-
#allocate ram 
S 0 0x20000000 0 0x000f0000 ram r-x
S 0 boot $s $s boot rwx 

f system = 0x8000c000
on newfw.bin system

S 0 system $s $s firmware rwx
