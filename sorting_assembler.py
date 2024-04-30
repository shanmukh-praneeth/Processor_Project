
import re

#stores the opcodes of R formatf
RInstruct = {
    'sub': '000000'
}

#stores the opcodes of I format
IInstruct = {'addi': '001000', 'lw': '100011', 'sw': '101011', 'beq': '000100', "ble" : "000110"
}

#stores the opcode of J format
JInstruct = {
    'j': '000010'
}

#stores opcode of registers used
registers_opcode = {
    "$zero" : "00000",
    "$t1": "01001",
    "$t2": "01010",
    "$t3": "01011",
    "$t4": "01100",
    "$t5": "01101",
    "$t6": "01110",
    "$t7": "01111",
    "$t8": "11000",
    "$t9": "11001",
    "$s0": "10000",
    "$s1": "10001",
    "$s4": "10100",
    "$s5": "10101",
}

#stores address of procedures performed
label_address = {
    "nextElement": "0000100000101010",
    "exitInner": "0000000000001010",
    "BubbleSort_OuterLoop": "00000100000000000000011101",
    "BubbleSort_InnerLoop": "01101011010000000000000100",
    "exit": "0000000000010001"
}

#Converts decimal to binary
def DectoBinary(dec):
    binary =""
    while dec > 0:
        binary = str(dec % 2) + binary
        dec = dec //2
    return binary

file = open('bubblesort.asm', 'r') #reads the file
binarycode = []

for line_no,line in enumerate(file.readlines()):
    if line.strip() and line_no > 49 and line_no < 81:
        line = line.strip()
        a = 0
        if("beq" in line):
                print(IInstruct["beq"],end="")
                items = re.split(r'[,\s()]+', line)
                print(registers_opcode[items[1]],end="")
                print(registers_opcode[items[2]],end="")
                print(label_address[items[3]])
                continue
        if("ble" in line):
            # print(IInstruct["ble"],end="")
            # items = re.split(r'[,\s()]+', line)
            # print(items)
            # print(registers_opcode[items[2]],end="")
            # print(registers_opcode[items[1]],end="")
            # print(label_address[items[3]])
            print("00000010101101000000100000101010")
            print("00010000001000000000000000000011")
            continue
        if("lw" in line):
            print(IInstruct["lw"],end="")
            items = re.split(r'[,\s()]+', line)
            print(registers_opcode[items[3]],end="")
            print(registers_opcode[items[1]],end="")
            imm = DectoBinary(int(items[2]))
            for i in range(16 - len(imm)):
                imm = "0" + imm
            print(imm)
            continue
        if("sw" in line):
            print(IInstruct["sw"],end="")
            items = re.split(r'[,\s()]+', line)
            print(registers_opcode[items[3]],end="")
            print(registers_opcode[items[1]],end="")
            imm = DectoBinary(int(items[2]))
            for i in range(16 - len(imm)):
                imm = "0" + imm
            print(imm)
            continue
        for instruction in RInstruct:
            if(instruction in line):
                print(RInstruct[instruction],end="")
                items = re.split(r'[,\s()]+', line) 
                print(registers_opcode[items[2]],end="")
                print(registers_opcode[items[3]],end="")
                print(registers_opcode[items[1]],end="")
                print("00000100010")
                break
        for instruction in IInstruct:
            if(instruction in line):
                print(IInstruct[instruction],end="")
                items = re.split(r'[,\s()]+', line)
                print(registers_opcode[items[2]],end="")
                print(registers_opcode[items[1]],end="")
                imm = DectoBinary(int(items[3]))
                for i in range(16 - len(imm)):
                    imm = "0" + imm
                print(imm)
                break
        for instruction in JInstruct:
            if(instruction in line):
                print(JInstruct[instruction],end="")
                items = re.split(r'[,\s()]+', line)
                print(label_address[items[1]])
                break
#        if("li" in line):

