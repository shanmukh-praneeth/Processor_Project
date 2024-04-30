import controlpath as con

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


file_name = "fib.txt"
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
        
        return linecode
    else:
        return None

def instruction_decode(linecode,cs):
    rs=0
    rd=0
    rt=0
    imm=0
    if(cs["JMP"]):
        global pc
        imm = "0000" + linecode[6:32] + "00"
        imm = int(imm,2)
        print('I am jumping',imm)
        pc = imm -4
        return [0,0,0,0]
    rs = linecode[6:11]
    rt = linecode[11:16]
    if cs['RegDst']:
        rd = linecode[16:21]
    else:
        rd = rt
    #convert it to integer
    imm = int(linecode[17:32],2)
    if linecode[16] == '1':
        imm = imm + ~(2**15 - 1)
    return rs,rt,rd,imm

def instruction_execute(rs,rt,imm,cs):
    if(cs["JMP"]):
        return
    x = default_regval[registers_opcode[rs]]
    y = default_regval[registers_opcode[rt]]

    print("Hi I am In Execute")
    print(f"This is my value for x and y {x} , , {y}")
    print(f"these are my registers   {default_regval[registers_opcode[rs]]} and {default_regval[registers_opcode[rt]]}  and aluop = {cs['AluOP']}")
    result = 0
    if(cs["ALUSrc"]):
        y = imm
    else:
        y = default_regval[registers_opcode[rt]]  # value of rt
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
    return result

def instruction_memory(result,rt,cs):
    if(cs["JMP"] or cs["Branch"]):
        return
    if(cs["MemRd"]):
        readData = memory[result]
        return readData
    if(cs["MemWr"]):
        memory[default_regval[registers_opcode[rt]]] = result

def instruction_writeback(writeReg,cs,result,readData):
    global pc
    pc = pc + 4
    print("pc: ",pc)
    if(cs["JMP"] or cs["Branch"]):
        return
    if(cs["MemReg"]):
        default_regval[registers_opcode[writeReg]] = readData
    else:
        print("result",result)
        default_regval[registers_opcode[writeReg]] = result

count=0
while((pc-startAddress)//4 < n):
    linecode = instruction_fetch()
    controlsignals = con.pass_signals(linecode)
    print(linecode[0:6],controlsignals)
    rs,rt,rd,imm = instruction_decode(linecode,controlsignals)
    print("ID:",rs,rt,rd,imm)
    result = instruction_execute(rs,rt,imm,controlsignals)
    print("EX:",result)
    readData = instruction_memory(result,rt,controlsignals)
    instruction_writeback(rd,controlsignals,result,readData)
    count+=1
    # time.sleep(1)
print(default_regval)
print(registers_opcode)

# rint(memory)