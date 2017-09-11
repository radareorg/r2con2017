from triton import *

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
    resetEngines()
    # dummy rbp value
    rbp = 0x1234
    setConcreteRegisterValue(Register(REG.RBP, rbp))

def process_single(ip, opcode):
        inst = Instruction()
        inst.setOpcodes(opcode)
        inst.setAddress(ip)
        processing(inst)
        return inst

if __name__ == '__main__':

    init_machine()

    rbp = getConcreteRegisterValue(REG.RBP)
    setConcreteMemoryValue(MemoryAccess(rbp-4,  CPUSIZE.QWORD, 0xdeadbeef))

    # Definde symbolic variables
    a = convertMemoryToSymbolicVariable(MemoryAccess(rbp-4, CPUSIZE.QWORD))

    ip = ENTRY

    while ip in function:

        inst = Instruction()
        inst.setOpcodes(function[ip])
        inst.setAddress(ip)

        processing(inst)
        print inst

        rax = getConcreteRegisterValue(REG.RAX)

        if ip == 0x004004d3 and rax !=0x1f02 :
            print "[+] rax has wrong value ({:#x})".format(rax)
            zfExpr  = getFullAst(buildSymbolicRegister(REG.ZF))
            newExpr    = ast.assert_(ast.equal(zfExpr, ast.bvtrue()))
            print "[+] requesting new model"
            models = getModel(newExpr)
            ip = ENTRY
            init_machine()
            print "[+] injecting new model and restarting"
            setConcreteMemoryValue(MemoryAccess(rbp-4, CPUSIZE.QWORD, models[0].getValue()))
            continue

        # Next instruction
        ip = buildSymbolicRegister(REG.RIP).evaluate()
    print "[+] input:", models[0].getValue()

