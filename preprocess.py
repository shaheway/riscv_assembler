# import numba
import assembler
rv32isa = {'add': {'type': 'R', 'funct3': '000', 'funct7': '0000000', 'opcode': '0110011'},
           'sub': {'type': 'R', 'funct3': '000', 'funct7': '0100000', 'opcode': '0110011'},
           'and': {'type': 'R', 'funct3': '111', 'funct7': '0000000', 'opcode': '0110011'},
           'or': {'type': 'R', 'funct3': '110', 'funct7': '0000000', 'opcode': '0110011'},
           'xor': {'type': 'R', 'funct3': '100', 'funct7': '0000000', 'opcode': '0110011'},
           'sll': {'type': 'R', 'funct3': '001', 'funct7': '0000000', 'opcode': '0110011'},
           'srl': {'type': 'R', 'funct3': '101', 'funct7': '0000000', 'opcode': '0110011'},
           'sra': {'type': 'R', 'funct3': '101', 'funct7': '0100000', 'opcode': '0110011'},
           'slt': {'type': 'R', 'funct3': '010', 'funct7': '0000000', 'opcode': '0110011'},
           'sltu': {'type': 'R', 'funct3': '011', 'funct7': '0000000', 'opcode': '0110011'},
           'addi': {'type': 'I', 'funct3': '000', 'funct7': None, 'opcode': '0010011'},
           'andi': {'type': 'I', 'funct3': '111', 'funct7': None, 'opcode': '0010011'},
           'ori': {'type': 'I', 'funct3': '110', 'funct7': None, 'opcode': '0010011'},
           'xori': {'type': 'I', 'funct3': '100', 'funct7': None, 'opcode': '0010011'},
           'slli': {'type': 'I', 'funct3': '001', 'funct7': '0000000', 'opcode': '0010011'},
           'srli': {'type': 'I', 'funct3': '101', 'funct7': '0000000', 'opcode': '0010011'},
           'srai': {'type': 'I', 'funct3': '101', 'funct7': '0100000', 'opcode': '0010011'},
           'slti': {'type': 'I', 'funct3': '010', 'funct7': None, 'opcode': '0010011'},
           'sltiu': {'type': 'I', 'funct3': '011', 'funct7': None, 'opcode': '0010011'},
           'lb': {'type': 'I', 'funct3': '000', 'funct7': None, 'opcode': '0000011'},
           'lbu': {'type': 'I', 'funct3': '100', 'funct7': None, 'opcode': '0000011'},
           'lh': {'type': 'I', 'funct3': '001', 'funct7': None, 'opcode': '0000011'},
           'lhu': {'type': 'I', 'funct3': '000', 'funct7': None, 'opcode': '0000011'},
           'lw': {'type': 'I', 'funct3': '010', 'funct7': None, 'opcode': '0000011'},
           'sb': {'type': 'S', 'funct3': '000', 'funct7': None, 'opcode': '0100011'},
           'sh': {'type': 'S', 'funct3': '001', 'funct7': None, 'opcode': '0100011'},
           'sw': {'type': 'S', 'funct3': '010', 'funct7': None, 'opcode': '0100011'},
           'beq': {'type': 'B', 'funct3': '000', 'funct7': None, 'opcode': '1100011'},
           'bge': {'type': 'B', 'funct3': '101', 'funct7': None, 'opcode': '1100011'},
           'bgeu': {'type': 'B', 'funct3': '111', 'funct7': None, 'opcode': '1100011'},
           'blt': {'type': 'B', 'funct3': '100', 'funct7': None, 'opcode': '1100011'},
           'bltu': {'type': 'B', 'funct3': '110', 'funct7': None, 'opcode': '1100011'},
           'bne': {'type': 'B', 'funct3': '001', 'funct7': None, 'opcode': '1100011'},
           'jal': {'type': 'J', 'funct3': None, 'funct7': None, 'opcode': '1101111'},
           'jalr': {'type': 'I', 'funct3': '000', 'funct7': None, 'opcode': '1100111'},
           'auipc': {'type': 'U', 'funct3': None, 'funct7': None, 'opcode': '0010111'},
           'lui': {'type': 'U', 'funct3': None, 'funct7': None, 'opcode': '0110011'},
           'ebreak': {'type': 'I', 'funct3': '000', 'funct7': None, 'opcode': '1110011'},
           'ecall': {'type': 'I', 'funct3': '000', 'funct7': None, 'opcode': '1110011'}
           }

Pseu = ['nop', 'mv', 'not', 'neg', 'negw', 'sext.w', 'seqz', 'snez', 'sltz', 'sgtz']


# @numba.jit()
def to_bit(s: str, op: str) -> str:
    num = eval(s)
    # print(type(num))
    if rv32isa[op]['type'] == 'J':
        if num < 0:
            return str(bin(num & 0xfffff))[2:][::-1]
        else:
            bin_str = str(bin(num))[2:]
            if len(bin_str) > 21:
                return bin_str[-21:][::-1]
            result = ''
            for j in range(0, 21 - len(bin_str)):
                result += '0'
            result += bin_str
            return result[::-1]
    elif rv32isa[op]['type'] == 'U':
        if num < 0:
            return str(bin(num & 0xfffff))[2:][::-1]
        else:
            bin_str = str(bin(num))[2:]
            if len(bin_str) > 32:
                return bin_str[-32:][::-1]
            result = ''
            for j in range(0, 32 - len(bin_str)):
                result += '0'
            result += bin_str
            return result[::-1]
    elif rv32isa[op]['type'] == 'B':
        if num < 0:
            return str(bin(num & 0xffff))[2:][::-1]
        else:
            bin_str = str(bin(num))[2:]
            if len(bin_str) > 13:
                return bin_str[-13:][::-1]
            result = ''
            for j in range(0, 13 - len(bin_str)):
                result += '0'
            result += bin_str
            return result[::-1]
    else:
        if num < 0:
            return str(bin(num & 0xfff))[2:][::-1]
        else:
            bin_str = str(bin(num))[2:]
            if len(bin_str) > 12:
                return bin_str[-12:][::-1]
            result = ''
            for j in range(0, 12 - len(bin_str)):
                result += '0'
            result += bin_str
            return result[::-1]


def pseudo(res):
    if res[0] not in Pseu:
        return res
    if res[0] == 'nop':
        return ['addi', ['x0', 'x0', '0x0']]
    elif res[0] == 'mv':
        res[0] = 'addi'
        res[1].append('0x0')
    elif res[0] == 'not':
        res[0] = 'xori'
        res[1].append('-0x1')
    elif res[0] == 'neg':
        res[0] = 'sub'
        res[1].insert(1, 'x0')
    elif res[0] == 'negw':
        raise RuntimeError('negwError')
    # elif res[0] == 'sext.w':
    #     res[0] = 'addiw'
    #     res[1].append('0x0')
    elif res[0] == 'seqz':
        res[0] = 'sltiu'
        res[1].append('0x1')
    elif res[0] == 'snez':
        res[0] = 'sltu'
        res[1].insert(1, 'x0')
    elif res[0] == 'sltz':
        res[0] = 'slt'
        res[1].append('x0')
    elif res[0] == 'sgtz':
        res[0] = 'slt'
        res[1].insert(1, 'x0')
    return res


def main(infile_name):
    with open(infile_name, encoding='utf-8') as file_obj:
        cnt = -4        # address
        alter = {}      # labels
        out = []        # output
        for line in file_obj:   # process the input
            if line == '\n':
                continue
            end = line.find('#')
            if end != -1:
                init = line[:end]
            else:
                init = line
            if init:
                arr = init.split()
                if arr[-1] == '':
                    arr.pop()
                if arr[0][-1] == ':':   # build label dictionary
                    if len(arr) == 1:
                        alter.update({arr[0][:-1]: str(hex(cnt + 4))})
                        continue
                    else:
                        cnt += 4
                        alter.update({arr[0][:-1]: str(hex(cnt))})
                        arr.pop(0)
                else:
                    cnt += 4
                res = [arr[0]]
                op_str = ''
                for i in range(1, len(arr)):
                    op_str += arr[i]
                op_addr = op_str.split(",")
                if arr[0] in ['lb', 'lbu', 'lh', 'lhu', 'lw', 'sb', 'sh', 'sw']:
                    tmp = op_addr[1].split("(")
                    tmp[1] = tmp[1][:-1]
                    op_addr[1] = tmp[1]
                    op_addr.append(tmp[0])
                # for i in range(len(op_addr)):
                #     if op_addr[i][0:2] == '0x' or op_addr[i][0:3] == '-0x':
                #         op_addr[i] = hex_to_bit(op_addr[i], arr[0])
                if op_str == '':
                    res.append([])
                else:
                    res.append(op_addr)
                res = pseudo(res)   # pseudo instructions
                if res[0] == 'li':
                    imm = eval(res[1][1])
                    if 0 <= imm <= 4096:
                        res = ['addi', [res[1][0], 'x0', res[1][1]], cnt]
                        out.append(res)
                    else:
                        res = ['lui', [res[1][0], str(hex(imm >> 12))], cnt]
                        out.append(res)
                        cnt += 4
                        res = ['addi', [res[1][0], res[1][0], str(hex(imm & 0xfff))], cnt]
                        out.append(res)
                else:
                    res.append(cnt)     # add the address
                    out.append(res)
                # print(res)
        for i in range(len(out)):
            op = out[i][0]
            for j in range(len(out[i][1])):
                if out[i][1][j] in alter:
                    out[i][1][j] = alter.get(out[i][1][j], out[i][1][j])
                    out[i][1][j] = str(eval(out[i][1][j])-out[i][2])
                    # print(out[i][1][j])
                if out[i][1][j][0] == '-' or ('0' <= out[i][1][j][0] <= '9'):   # change number to bit
                    out[i][1][j] = to_bit(out[i][1][j], op)
        print(out)
        # print(alter)
        return out


raw_inst = main("loop_add.txt")
outfile = open()
for e in raw_inst:
    hex_inst = assembler.AssemblyCode(e[0], e[1])
