from triton import *

color_green = '\033[92m'
color_reset = '\033[0m'

ENTRY = 0x004004b1
function = {
    ENTRY:      "8b45fc".decode("hex"),      # mov eax, dword [rbp - 4]
    0x004004b4: "01c0".decode("hex"),        # add eax, eax
    0x004004b6: "8945f8".decode("hex"),      # mov dword [rbp - 8], eax
    0x004004b9: "8b45f8".decode("hex"),      # mov eax, dword [rbp - 8]
    0x004004bc: "8d50eb".decode("hex"),      # lea edx, [rax - 0x15]
    0x004004bf: "8b45f8".decode("hex"),      # mov eax, dword [rbp - 8]
    0x004004c2: "01d0".decode("hex"),        # add eax, edx
    0x004004c4: "8945f8".decode("hex"),      # mov dword [rbp - 8], eax
    0x004004c7: "8b45f8".decode("hex"),      # mov eax, dword [rbp - 8]
    0x004004ca: "6bc036".decode("hex"),      # imul eax, eax, 0x36
    0x004004cd: "8945f8".decode("hex"),      # mov dword [rbp - 8], eax
    0x004004d0: "8b45f8".decode("hex"),      # mov eax, dword [rbp - 8]
    0x004004d3: "3d021f0000".decode("hex"),  # cmp eax, 0x1f02
    0x004004d8: "7507".decode("hex"),        # jne 0x4004e1
    0x004004da: "b801000000".decode("hex"),  # mov eax, 1
    0x004004df: "eb05".decode("hex"),        # jmp 0x4004e6
    0x004004e1: "b800000000".decode("hex"),  # mov eax, 0
    0x004004e6: "c3".decode("hex"),          # ret
}


def init_machine():
    setArchitecture(ARCH.X86_64)
    setAstRepresentationMode(AST_REPRESENTATION.PYTHON)


if __name__ == '__main__':

    init_machine()
    ip = ENTRY
    while ip in function:
        # Build instruction
        inst = Instruction()

        # Setup Opcodes
        inst.setOpcodes(function[ip])

        # Setup Address
        inst.setAddress(ip)

        # Process instruction
        processing(inst)

        print "{}{}{}".format(color_green, str(inst), color_reset)
        for symExpr in inst.getSymbolicExpressions():
            print "\t{}".format(symExpr)
        print

        # Next instruction
        ip = getConcreteRegisterValue(REG.RIP)

