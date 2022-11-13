import numba
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

@numba.jit()
def hex_to_bit(s, op):
    hex_num = eval(s)
    if rv32isa[op]['type'] == 'J':
        if hex_num < 0:
            return str(bin(hex_num & 0xfffff))[2:]
        else:
            bin_str = str(bin(hex_num))[2:]
            if len(bin_str) > 20:
                return bin_str[-20:]
            result = ''
            for j in range(0, 20 - len(bin_str)):
                result += '0'
            result += bin_str
            return result
    else:
        if hex_num < 0:
            return str(bin(hex_num & 0xfff))[2:]
        else:
            bin_str = str(bin(hex_num))[2:]
            if len(bin_str) > 12:
                return bin_str[-12:]
            result = ''
            for j in range(0, 12 - len(bin_str)):
                result += '0'
            result += bin_str
            return result


def main():
    with open("assembly_code.txt", encoding='utf-8') as file_obj:
        cnt = -4
        alter = {}
        out = []
        for line in file_obj:
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
                if arr[0][-1] == ':':
                    if len(arr) == 1:
                        alter.update({arr[0][:-1]: str(hex(cnt+4))})
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
                out.append(res)
                # print(res)
        for i in range(len(out)):
            op = out[i][0]
            for j in range(len(out[i][1])):
                out[i][1][j] = alter.get(out[i][1][j], out[i][1][j])
                if out[i][1][j][0:2] == '0x' or out[i][1][j][0:3] == '-0x':
                    out[i][1][j] = hex_to_bit(out[i][1][j], op)
        print(out)
        print(alter)
main()
