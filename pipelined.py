import controlpath as con

default_pipereg = {
    "ifid" : {},
    "idex" : {},
    "exmem" : {},
    "memwb" : {}
}

registers_opcode = {
    "$zero":"00000",
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
    "$s5": "10101"
}

registers_opcode = {j:i for i,j in registers_opcode.items()}
print(registers_opcode)
default_regval = {
    "$zero" : 0,
    "$t1": 0,
    "$t2": 0,
    "$t3": 0,
    "$t4": 0,
    "$t5": 0,
    "$t6": 0,
    "$t7": 0,
    "$t8": 0,
    "$t9": 0,
    "$s0": 0,
    "$s1": 0,
    "$s4": 0,
    "$s5": 0
}

n=0
start = 0
end = 20

startAddress = 4194304
pc = startAddress
memory = {}


file_name = "fact.txt"
for i in range(start,end+1):
    memory[i] = 0 

with open(file_name,'r') as file:
    code = file.readlines()
    n = len(code)

# main()
# cp = con.controlpaths
# pass to each fn : inst_fetch(cp)

def instruction_fetch():
    print("HI I am in IF")
    print(default_regval)
    global pc
    if((pc-startAddress)//4<len(code)):
        print(f"pc in IF = {(pc-startAddress)//4}")
        linecode = code[(pc-startAddress)//4]
        default_pipereg['ifid']['instruction'] = linecode
        return linecode
    else:
        default_pipereg['ifid']['instruction'] = None
        return None

def instruction_decode(linecode,cs):
    rs=0
    rd=0
    rt=0
    imm=0
    if(cs["JMP"]):
        global pc
        imm = "0000" + default_pipereg['ifid']['instruction'][6:32] + "00"
        imm = int(imm,2)
        print('I am jumping',imm)
        pc = imm -4
        default_pipereg["idex"]['rs'] = 0
        default_pipereg["idex"]['rt'] = 0
        default_pipereg["idex"]['rd'] = 0
        default_pipereg["idex"]['imm'] = 0
        return [0,0,0,0]
    rs = default_pipereg['ifid']['instruction'][6:11]
    rt = default_pipereg['ifid']['instruction'][11:16]
    if cs['RegDst']:
        rd = default_pipereg['ifid']['instruction'][16:21]
    else:
        rd = rt
    #convert it to integer
    imm = int(default_pipereg['ifid']['instruction'][17:32],2)
    if default_pipereg['ifid']['instruction'][16] == '1':
        imm = imm + ~(2**15 - 1)
    instruction_fetch()
    default_pipereg["idex"]['rs'] = rs
    default_pipereg["idex"]['rt'] = rt
    default_pipereg["idex"]['rd'] = rd
    default_pipereg["idex"]['imm'] = imm
    return rs,rt,rd,imm

def instruction_execute(rs,rt,imm,cs):
    
    if(cs["JMP"]):
        return
    x = default_regval[registers_opcode[default_pipereg["idex"]['rs']]]
    y = default_regval[registers_opcode[default_pipereg['idex']['rt']]]

    print("Hi I am In Execute")
    print(f"This is my value for x and y {x} , , {y}")
    print(f"these are my registers   {default_regval[registers_opcode[rs]]} and {default_regval[registers_opcode[rt]]}  and aluop = {cs['AluOP']}")
    result = 0
    if(cs["ALUSrc"]):
        y = default_pipereg['idex']['imm']
    else:
        y = default_regval[registers_opcode[default_pipereg['idex'][rt]]]  # value of rt
    if(cs["AluOP"] == 2):
        result = x + y
    elif(cs["AluOP"] == 3):
        result = x-y
        if(cs["Branch"]):
            print(result)
        if(result == 0 and cs["Branch"]):
            global pc
            print("branching to",pc + 4*imm)
            pc = pc + 4*imm
    if(cs["AluOP"] == 4):
        result = x * y
    instruction_decode(linecode,cs)
    default_pipereg["exmem"]['result'] = result

def instruction_memory(result,rt,cs):
    
    if(cs["JMP"] or cs["Branch"]):
        default_pipereg["memwb"]['rd'] = None
        return
    if(cs["MemRd"]):
        readData = memory[result]
        default_pipereg["memwb"]['rd'] = memory[result]
        return readData
    if(cs["MemWr"]):
        memory[default_regval[registers_opcode[rt]]] = default_pipereg["exmem"]['result']
    instruction_execute(rs,rt,imm,cs)

def instruction_writeback(writeReg,cs,result,readData):
    
    global pc
    pc = pc + 4
    print("pc: ",pc)
    if(cs["JMP"] or cs["Branch"]):
        return
    if(cs["MemReg"]):
        default_regval[registers_opcode[writeReg]] = default_pipereg["memwb"]['rd']
    else:
        print("result",result)
        default_regval[registers_opcode[writeReg]] = default_pipereg["exmem"]['result']
    instruction_memory(result,rt,cs)


# call as follows
# IF
# ID
# EX
# MEM
# WB
# while condition:
#   WB



count=0
linecode = instruction_fetch()
controlsignals = con.pass_signals(linecode)
print(linecode[0:6],controlsignals)
rs,rt,rd,imm = instruction_decode(linecode,controlsignals)
result = instruction_execute(rs,rt,imm,controlsignals)
print("EX:",result)
readData = instruction_memory(result,rt,controlsignals)
instruction_writeback(rd,controlsignals,result,readData)
while((pc-startAddress)//4 < n):
    instruction_writeback(rd,controlsignals,result,readData)
    count+=1
    # time.sleep(1)
print(default_regval)
print(registers_opcode)
