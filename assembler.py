import numpy as np
rv32isa = {'add'  : {'type': 'R', 'funct3': '000', 'funct7': '0000000', 'opcode': '0110011'},
           'sub'  : {'type': 'R', 'funct3': '000', 'funct7': '0100000', 'opcode': '0110011'},
           'and'  : {'type': 'R', 'funct3': '111', 'funct7': '0000000', 'opcode': '0110011'},
           'or'   : {'type': 'R', 'funct3': '110', 'funct7': '0000000', 'opcode': '0110011'},
           'xor'  : {'type': 'R', 'funct3': '100', 'funct7': '0000000', 'opcode': '0110011'},
           'sll'  : {'type': 'R', 'funct3': '001', 'funct7': '0000000', 'opcode': '0110011'},
           'srl'  : {'type': 'R', 'funct3': '101', 'funct7': '0000000', 'opcode': '0110011'},
           'sra'  : {'type': 'R', 'funct3': '101', 'funct7': '0100000', 'opcode': '0110011'},
           'slt'  : {'type': 'R', 'funct3': '010', 'funct7': '0000000', 'opcode': '0110011'},
           'sltu' : {'type': 'R', 'funct3': '011', 'funct7': '0000000', 'opcode': '0110011'},
           'addi' : {'type': 'I', 'funct3': '000', 'funct7': None     , 'opcode': '0010011'},
           'andi' : {'type': 'I', 'funct3': '111', 'funct7': None     , 'opcode': '0010011'},
           'ori'  : {'type': 'I', 'funct3': '110', 'funct7': None     , 'opcode': '0010011'},
           'xori' : {'type': 'I', 'funct3': '100', 'funct7': None     , 'opcode': '0010011'},
           'slli' : {'type': 'I', 'funct3': '001', 'funct7': '0000000', 'opcode': '0010011'},
           'srli' : {'type': 'I', 'funct3': '101', 'funct7': '0000000', 'opcode': '0010011'},
           'srai' : {'type': 'I', 'funct3': '101', 'funct7': '0100000', 'opcode': '0010011'},
           'slti' : {'type': 'I', 'funct3': '010', 'funct7': None     , 'opcode': '0010011'},
           'sltiu': {'type': 'I', 'funct3': '011', 'funct7': None     , 'opcode': '0010011'},
           'lb'   : {'type': 'I', 'funct3': '000', 'funct7': None     , 'opcode': '0000011'},
           'lbu'  : {'type': 'I', 'funct3': '100', 'funct7': None     , 'opcode': '0000011'},
           'lh'   : {'type': 'I', 'funct3': '001', 'funct7': None     , 'opcode': '0000011'},
           'lhu'  : {'type': 'I', 'funct3': '000', 'funct7': None     , 'opcode': '0000011'},
           'lw'   : {'type': 'I', 'funct3': '010', 'funct7': None     , 'opcode': '0000011'},
           'sb'   : {'type': 'S', 'funct3': '000', 'funct7': None     , 'opcode': '0100011'},
           'sh'   : {'type': 'S', 'funct3': '001', 'funct7': None     , 'opcode': '0100011'},
           'sw'   : {'type': 'S', 'funct3': '010', 'funct7': None     , 'opcode': '0100011'},
           'beq'  : {'type': 'B', 'funct3': '000', 'funct7': None     , 'opcode': '1100011'},
           'bge'  : {'type': 'B', 'funct3': '101', 'funct7': None     , 'opcode': '1100011'},
           'bgeu' : {'type': 'B', 'funct3': '111', 'funct7': None     , 'opcode': '1100011'},
           'blt'  : {'type': 'B', 'funct3': '100', 'funct7': None     , 'opcode': '1100011'},
           'bltu' : {'type': 'B', 'funct3': '110', 'funct7': None     , 'opcode': '1100011'},
           'bne'  : {'type': 'B', 'funct3': '001', 'funct7': None     , 'opcode': '1100011'},
           'jal'  : {'type': 'J', 'funct3': None , 'funct7': None     , 'opcode': '1101111'},
           'jalr' : {'type': 'I', 'funct3': '000', 'funct7': None     , 'opcode': '1100111'},
           'auipc': {'type': 'U', 'funct3': None , 'funct7': None     , 'opcode': '0010111'},
           'lui'  : {'type': 'U', 'funct3': None , 'funct7': None     , 'opcode': '0110011'},
           'ebreak':{'type': 'I', 'funct3': '000', 'funct7': None     , 'opcode': '1110011'},
           'ecall' :{'type': 'I', 'funct3': '000', 'funct7': None     , 'opcode': '1110011'}
           }
registers = {'x0': '00000',
             'ra': '00001',
             'sp': '00010',
             'gp': '00011',
             'tp': '00100',
             't0': '00101',
             't1': '00110',
             't2': '00111',
             's0': '01000',
             's1': '01001',
             'a0': '01010',
             'a1': '01011',
             'a2': '01100',
             'a3': '01101',
             'a4': '01110',
             'a4': '01111',
             'a5': '10000',
             'a6': '10001',
             's2': '10010',
             's3': '10011',
             's4': '10100',
             's5': '10101',
             's6': '10110',
             's7': '10111',
             's8': '11000',
             's9': '11001',
             's10': '11010',
             's11': '11011',
             't3': '11100',
             't4': '11101',
             't5': '11110',
             't6': '11111'}

class AssemblyCode:
    def __init__(self, inst_name, ops):
        self.type = rv32isa[inst_name]['type']
        self.funct3 = list(rv32isa[inst_name]['funct3']) if rv32isa[inst_name]['funct3'] else None
        self.funct7 = list(rv32isa[inst_name]['funct7']) if rv32isa[inst_name]['funct7'] else None
        self.opcode = list(rv32isa[inst_name]['opcode'])
        self.op = ops
        self.inst = []
        if inst_name == 'ecall':
            self.inst = 
        self.convert()
    
    def convert(self):
        binary_inst_array = np.array(list('00000000000000000000000000000000'))
        binary_inst_array[0:7] = self.opcode
        if self.type == 'R':
            binary_inst_array[7:12] = list(registers[self.op[0]])
            binary_inst_array[12:15] = self.funct3
            binary_inst_array[15:20] = list(registers[self.op[1]])
            binary_inst_array[20:25] = list(registers[self.op[2]])
            binary_inst_array[25:] = self.funct7
        if self.type == 'I':
            binary_inst_array[7:12] = list(registers[self.op[0]])
            binary_inst_array[12:15] = self.funct3
            binary_inst_array[15:20] = list(registers[self.op[1]])
            binary_inst_array[20:] = list(self.op[2])
        if self.type == 'S':
            binary_inst_array[7:12] = list(self.op[2])[0:5]
            binary_inst_array[12:15] = self.funct3
            binary_inst_array[15:20] = list(registers[self.op[0]])
            binary_inst_array[20:25] = list(registers[self.op[1]])
            binary_inst_array[25:] = list(self.op[2])[5:]
        if self.type == 'B':
            binary_inst_array[7:12] = list(self.op[2][11])+list(self.op[2][1:5])
            binary_inst_array[12:15] = self.funct3
            binary_inst_array[15:20] = list(registers[self.op[0]])
            binary_inst_array[20:25] = list(registers[self.op[1]])
            binary_inst_array[25:] = list(self.op[2][5:11])+list(self.op[2][12])
        if self.type == 'U':
            binary_inst_array[7:12] = list(registers[self.op[0]])
            binary_inst_array[12:] = list(self.op[1])
        if self.type == 'J':
            binary_inst_array[7:12] = list(registers[self.op[0]])
            binary_inst_array[12:] = list(self.op[1][12:20])+list(self.op[1][11])+list(self.op[1][1:11])+list(self.op[1][20])
        for i in range(0, 32, 4):
            self.inst.append(hex(int(binary_inst_array[i]+binary_inst_array[i+1]+binary_inst_array[i+2]+binary_inst_array[i+3], 2))[-1])
        # print(binary_inst_array)
        
    def __str__(self) -> str:
        inst_str = ""
        inst_str = inst_str.join(self.inst)
        return inst_str

if __name__ == 'main':
    array = [['add', ['x0', 'x0', 'x0']], ['addi', ['s1', 'x0', '000011111001']]]
    for e in array:
        hex_inst = AssemblyCode(e[0], e[1])
        print(hex_inst)

