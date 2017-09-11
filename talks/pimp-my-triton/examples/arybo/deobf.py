from triton import *
from arybo.tools.triton_ import tritonexprs2arybo, tritonast2arybo
from arybo.lib.exprs_asm import to_llvm_function
import os

code = [
    (0x004005a3, "488b45f8".decode("hex")),        # mov rax, qword [rbp - 8]
    (0x004005a7, "4889c1".decode("hex")),          # mov rcx, rax
    (0x004005aa, "51".decode("hex")),              # push rcx
    (0x004005ab, "48c7c162010000".decode("hex")),  # mov rcx, 0x162
    (0x004005b2, "69c91fa0bc38".decode("hex")),    # imul ecx, ecx, 0x38bca01f
    (0x004005b8, "488b5df0".decode("hex")),        # mov rbx, qword [rbp - 0x10]
    (0x004005bc, "4989d8".decode("hex")),          # mov r8, rbx
    (0x004005bf, "4989c9".decode("hex")),          # mov r9, rcx
    (0x004005c2, "4d89c2".decode("hex")),          # mov r10, r8
    (0x004005c5, "4d89cb".decode("hex")),          # mov r11, r9
    (0x004005c8, "49f7d2".decode("hex")),          # not r10
    (0x004005cb, "49f7d3".decode("hex")),          # not r11
    (0x004005ce, "4c21db".decode("hex")),          # and rbx, r11
    (0x004005d1, "4c21d1".decode("hex")),          # and rcx, r10
    (0x004005d4, "4809cb".decode("hex")),          # or rbx, rcx
    (0x004005d7, "4c89c9".decode("hex")),          # mov rcx, r9
    (0x004005da, "51".decode("hex")),              # push rcx
    (0x004005db, "4889cf".decode("hex")),          # mov rdi, rcx
    (0x004005de, "50".decode("hex")),              # push rax
    (0x004005df, "4869cb38435600".decode("hex")),  # imul rcx, rbx, 0x564338
    (0x004005e6, "4889da".decode("hex")),          # mov rdx, rbx
    (0x004005e9, "4831fa".decode("hex")),          # xor rdx, rdi
    (0x004005ec, "48c7c045030000".decode("hex")),  # mov rax, 0x345
    (0x004005f3, "4869c325450300".decode("hex")),  # imul rax, rbx, 0x34525
    (0x004005fa, "59".decode("hex")),              # pop rcx
    (0x004005fb, "5e".decode("hex")),              # pop rsi
    (0x004005fc, "48f7d1".decode("hex")),          # not rcx
    (0x004005ff, "51".decode("hex")),              # push rcx
    (0x00400600, "48c7c162010000".decode("hex")),  # mov rcx, 0x162
    (0x00400607, "69c91fa0bc38".decode("hex")),    # imul ecx, ecx, 0x38bca01f
    (0x0040060d, "48f7d2".decode("hex")),          # not rdx
    (0x00400610, "59".decode("hex")),              # pop rcx
    (0x00400611, "58".decode("hex")),              # pop rax
    (0x00400612, "51".decode("hex")),              # push rcx
    (0x00400613, "4821d0".decode("hex")),          # and rax, rdx
    (0x00400616, "59".decode("hex")),              # pop rcx
    (0x00400617, "4831f3".decode("hex")),          # xor rbx, rsi
    (0x0040061a, "4821cb".decode("hex")),          # and rbx, rcx
    (0x0040061d, "4809d8".decode("hex")),          # or rax, rbx
    (0x00400620, "4889c6".decode("hex")),          # mov rsi, rax
]


def process_inst(addr, opcodes):
    inst = Instruction()

    # Setup opcodes
    inst.setOpcodes(opcodes)

    # Setup Address
    inst.setAddress(addr)

    # Process everything
    processing(inst)
    return inst


def rebuild_bin(se, sv):
    arybo_se = tritonexprs2arybo(se)
    arybo_sv = list()
    for v in sv.values():
        arybo_sv.append(tritonast2arybo(ast.variable(v)).v)

    M = to_llvm_function(arybo_se, arybo_sv)

    output = "arybo_llvmir.ll"
    opti_output = "opti_llvmir.ll"

    fd = open(output, 'w')
    fd.write(str(M))
    fd.close()
    os.system("clang -O2 -S -emit-llvm -o - %s > %s" % (output, opti_output))
    print '[+] LLVM module wrote in %s' % (output)
    print '[+] Recompiling deobfuscated binary...'
    dst = './deobf.out'
    os.system("clang  %s  ./run.c -o %s" % (opti_output, dst))
    print '[+] Deobfuscated binary recompiled: %s' % (dst)

if __name__ == '__main__':

    # Set the arch
    setArchitecture(ARCH.X86_64)

    # Reprentation for dummies
    setAstRepresentationMode(AST_REPRESENTATION.PYTHON)

    # dummy rbp value
    rbp = 0x1234
    setConcreteRegisterValue(Register(REG.RBP, rbp))

    # Definde symbolic variables
    a = convertMemoryToSymbolicVariable(MemoryAccess(rbp-8, CPUSIZE.QWORD))
    b = convertMemoryToSymbolicVariable(MemoryAccess(rbp-16, CPUSIZE.QWORD))

    print "[+] Emulating execution:"
    for (addr, opcodes) in code:
        # Build an instruction
        inst = process_inst(addr, opcodes)
        print inst

    rsi_expr = getSymbolicExpressionFromId(getSymbolicRegisterId(REG.RSI))
    rsi_ast = getFullAst(rsi_expr.getAst())
    print "[+] RSI's symbolic expression before Z3 simplification"
    print str(rsi_ast)

    print "[+] Simplifying expression"

    rsi_ast = simplify(rsi_ast, True)
    rsi_expr.setAst(rsi_ast)
    exprs = sliceExpressions(rsi_expr)
    print "[+] RSI's symbolic expression after Z3 simplification"
    print rsi_expr
    print

    rebuild_bin(exprs, getSymbolicVariables())
