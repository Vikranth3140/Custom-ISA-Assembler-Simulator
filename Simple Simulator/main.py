# CO_PROJECT_2023 - Vikranth, Rohan, Pritha, Swara

import sys

# opcode (predefined)
opcode={"add": "00000","sub": "00001","mov2": "00010","mov": "00011","ld": "00100","st": "00101","mul": "00110","div": "00111","rs": "01000","ls": "01001","xor": "01010","or": "01011","and": "01100","not": "01101","cmp": "01110","jmp": "01111","jlt": "11100","jgt": "11101","je": "11111","hlt": "11010"}

# registers (predefined) and default values = 0
register={"R0": "000","R1": "001","R2": "010","R3": "011","R4": "100","R5": "101","R6": "110","FLAGS": "111"}
register_value={"R0":0,"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0,"FLAGS":"0000000000000000"}

# flags (predefined)
flags={"V": "0000000000001000","L": "0000000000000100","G": "0000000000000010","E": "0000000000000001"}

# dictionary of variable names and values
variable={}
variable_values={}

# dictionary of labels names
labels={}

# error flag
error=0

# # input from file
# with open("stdin.txt") as fin:
#     l=[]
#     for i in fin:
#         if i.split()!=[]:
#             l.append(i.split())

# input
l=[]
input=sys.stdin
for elt in input:
    if(elt.strip()!=''):
        l.append(elt.split())
    # if elt.strip()=="":
        # l.append(elt.strip().split())

# for i in l:
#     print(i)


# final output
output=[]

# decimal to binary
def dec_to_bin(n):
    if n == 0:
        return '0000000'
    val = ''
    while n > 0:
        val = str(n%2)+val
        n//=2
    val = (7-len(val))*"0"+val
    return val

# list to string
def listToString(instruction):
    str = ""
    for i in instruction:
        str += i
        str += " "
    return str


# final instructions to be executed
instructions_with_pc={}

# functions for error checking and printing

# TYPE A FUNCTIONS
def check_error_type_A(instruction,line):
    if len(instruction)!=4:
        output.append("Error: "+str(instruction[0])+" instruction must have 3 parameters, line = "+str(line))
        return 0
    elif instruction[1] not in register or instruction[2] not in register or instruction[3] not in register:
        output.append("Error: No such registers is available, line = "+str(line))
        return 0
    elif instruction[1] == "FLAGS" or instruction[2] == "FLAGS" or instruction[3]=="FLAGS":
        output.append("Error: FLAGS can't be used as register, line = "+str(line))
        return 0
    else:
        return 1

def print_type_A(instruction):
    output.append(opcode[instruction[0]] + "0"*2 + register[instruction[1]] + register[instruction[2]]+register[instruction[3]])


# TYPE B FUNCTIONS
def check_error_type_B(instruction,line):
    imm_val=instruction[2][1:]
    check = 1
    # print(imm_val)
    if imm_val!="":
        for elt in imm_val:
            if elt not in '1234567890':
                check=0
                break
    else:
        check = 0
    if len(instruction)!=3:
        output.append("Error: "+str(instruction[0])+" instruction must have 2 parameters, line = "+str(line))
        return 0
    elif instruction[1] not in register:
        output.append("Error: register named "+str(instruction[1])+" is not available , line = "+str(line))
        return 0
    elif instruction[1]=="FLAGS":
        output.append("Error: FLAGS can't be used as register, line = "+str(line))
        return 0
    elif instruction[2][0] != "$":
        output.append("Error: "+instruction[2]+" doesn't contain $, line = "+str(line))
        return 0
    elif check==0:
        output.append("Error: "+instruction[2]+" is not an immediate value, line = "+str(line))
        return 0
    elif int(imm_val)<0 or int(imm_val)>127:
        output.append("Error: Immediate values is out of range (7 bits), line = "+str(line))
        return 0
    else:
        return 1
    
def print_type_B(instruction):
    imm_val=instruction[2][1:]
    imm_val_final=dec_to_bin(int(imm_val))
    if instruction[0]=="mov":
        output.append(opcode["mov2"] + "0"*1 + register[instruction[1]] + imm_val_final)
    else:
        output.append(opcode[instruction[0]] + "0"*1 + register[instruction[1]] + imm_val_final)


# TYPE C FUNCTIONS 
def check_error_type_C(instruction,line):
    if instruction[0]=="cmp" and len(instruction)!=3:
        output.append("Error: can't compare more than 2 registers, line = "+str(line))
        return 0
    elif len(instruction)!=3:
        output.append("Error: "+str(instruction[0])+" instruction must have 2 parameters, line = "+str(line))
        return 0
    elif instruction[1] not in register:
        output.append("Error: "+str(instruction[1])+" is not a register name, line = "+str(line))
        return 0
    elif instruction[2] not in register:
        output.append("Error: "+str(instruction[1])+" is not a register name, line = "+str(line))
        return 0
    elif instruction[0]!="mov" and (instruction[1] == "FLAGS" or instruction[2] == "FLAGS"):
        output.append("Error: FLAGS can't be used as register, line = "+str(line))
        return 0
    else:
        return 1

def print_type_C(instruction):
    output.append(opcode[instruction[0]] + "0"*5 + register[instruction[1]] + register[instruction[2]])


# TYPE D FUNCTIONS
def check_error_type_D(instruction,line):
    if len(instruction)!=3:
        output.append("Error: "+str(instruction[0])+" instruction must have 2 parameters, line = "+str(line))
        return 0
    elif instruction[1] not in register:
        output.append("Error: "+str(instruction[1])+" is not a register name, line = "+str(line))
        return 0
    elif instruction[2] not in variable:
        output.append("Error: "+str(instruction[2])+" is not defined, line = "+str(line))
        return 0
    elif instruction[2] in labels:
        output.append("Error: "+str(instruction[2])+" is not a label, line = "+str(line))
        return 0
    elif instruction[1] == "FLAGS" or instruction[2] == "FLAGS":
        output.append("Error: FLAGS can't be used as register, line = "+str(line))
        return 0
    else:
        return 1

def print_type_D(instruction):
    output.append(opcode[instruction[0]] + "0" + register[instruction[1]] + variable[instruction[2]])



# TYPE E FUNCTIONS
def check_error_type_E(instruction,line):
    if len(instruction)!=2:
        output.append("Error: "+str(instruction[0])+" instruction must have only 1 address, line = "+str(line))
        return 0
    elif instruction[1] not in labels:
        output.append("Error: "+str(instruction[1])+" is not a defined label, line = "+str(line))
        return 0
    elif instruction[1] in variable:
        output.append("Error: We can't use variable "+str(instruction[1])+" as a label, line = "+str(line))
        return 0
    elif instruction[1] == "FLAGS":
        output.append("Error: We can't use FLAGS register "+str(instruction[1])+" as a label, line = "+str(line))
        return 0
    elif instruction[1] in register:
        output.append("Error: We can't use registers "+str(instruction[1])+" as a label, line = "+str(line))
        return 0
    else:
        return 1

def print_type_E(instruction):
    output.append(opcode[instruction[0]] + "0"*4 + labels[instruction[1]])



#TYPE F FUNCTIONS
def check_error_type_F(instruction,line):
    if len(instruction)!=1:
        output.append("Error: hlt instruction shouldn't have any parameters, line = "+str(line))
        return 0
    else:
        return 1
  

def print_type_F(instruction):
    output.append(opcode[instruction[0]] + "0"*11 )
    

# hlt code count (only 1 allowed in code)
htl_count=0

# program counter and temp counter (for variables)
program_counter=0
temp_counter=0

# checking intitial errors in input and making final instructions list and creating variables
for j in range(0,len(l)):
    i = l[j]

    # Invalid Codes
    if i[0] not in opcode.keys() and i[0] != "var" and ":" not in i[0]:
        output.append("Error: Typos in instruction name or register name, line "+str(program_counter+temp_counter+1))
        error=1
        break

    # hlt not used at last
    if i[-1]=="hlt" and j!=len(l)-1:
        output.append("Error: hlt not being used as the last instruction, line "+str(program_counter+temp_counter+1))
        error=1
        break

    # missing hlt instruction-1
    if i[-1]=="hlt" and j==len(l)-1:
        htl_count+=1

    # Variable defining not at beginning
    if i[0]=="var" and program_counter==0:
        # adding vairable names in a dictionary
        variable_values[i[1]]=0
        temp_counter+=1

    # adding labels
    if ":" in i[0]:
        labels[(i[0].split(":"))[0]]=dec_to_bin(program_counter)

    # variable not declared at start
    if i[0]=="var" and program_counter!=0:
        output.append("Error: Variables not declared at the beginning, line "+str(program_counter+temp_counter+1))
        error=1
        break

    # making final instructions
    if i[0]!="var":
        if ":" in i[0]:
            instructions_with_pc[(i[0].split(":"))[0]]=i[1:]
            program_counter+=1
        else:
            instructions_with_pc[program_counter]=i
            program_counter+=1

# making mem_addr for variables
for i in variable_values.keys():
    variable[i]=dec_to_bin(program_counter)
    program_counter+=1

# missing hlt instruction-2
if htl_count==0 and error==0:
    output.append("Error: Missing hlt instruction")
    error=1

if error==0 and len(list(instructions_with_pc.keys())) > 128:
    output.append("Error: Length of instructions is more than 128")
    error=1


program_counter=1+temp_counter
if error==0:

    # checking errors
    for keys in instructions_with_pc:

        if instructions_with_pc[keys][0] == "add" or instructions_with_pc[keys][0] == "sub" or instructions_with_pc[keys][0] == "mul" or instructions_with_pc[keys][0] == "xor" or instructions_with_pc[keys][0] == "or" or instructions_with_pc[keys][0] == "and":
            if(check_error_type_A(instructions_with_pc[keys],program_counter)==0):
                error=1
                break

        elif instructions_with_pc[keys][0]=="rs" or instructions_with_pc[keys][0]=="ls" or (instructions_with_pc[keys][0] == "mov" and instructions_with_pc[keys][2] not in register_value):
            if(check_error_type_B(instructions_with_pc[keys],program_counter)==0):
                error=1
                break

        elif instructions_with_pc[keys][0] == "mov" or instructions_with_pc[keys][0] == "div" or instructions_with_pc[keys][0] == "not" or instructions_with_pc[keys][0] == "cmp":
            if(check_error_type_C(instructions_with_pc[keys],program_counter)==0):
                error=1
                break

        elif instructions_with_pc[keys][0] == "ld" or instructions_with_pc[keys][0] == "st":
            if(check_error_type_D(instructions_with_pc[keys],program_counter)==0):
                error=1
                break

        elif instructions_with_pc[keys][0] == "jmp" or instructions_with_pc[keys][0] == "jlt" or instructions_with_pc[keys][0] == "jgt" or instructions_with_pc[keys][0] == "je":
            if(check_error_type_E(instructions_with_pc[keys],program_counter)==0):
                error=1
                break

        elif instructions_with_pc[keys][0] == "hlt":
            if(check_error_type_F(instructions_with_pc[keys],program_counter)==0):
                error=1
                break

        else:
            output.append("Typos in instruction name or register name, line = ",program_counter)
            error=1
            break

        program_counter+=1


    # output.txt file
    if error == 0:
        output=[]

        # adding starting part
        # for i in l:
        #     output.append(listToString(i))
        # # adding line break
        # output.append("************binary**code************")

        # adding machine lang codes
        for keys in instructions_with_pc:

            if instructions_with_pc[keys][0] == "add" or instructions_with_pc[keys][0] == "sub" or instructions_with_pc[keys][0] == "mul" or instructions_with_pc[keys][0] == "xor" or instructions_with_pc[keys][0] == "or" or instructions_with_pc[keys][0] == "and":
                print_type_A(instructions_with_pc[keys])

            elif instructions_with_pc[keys][0]=="rs" or instructions_with_pc[keys][0]=="ls" or (instructions_with_pc[keys][0] == "mov" and instructions_with_pc[keys][2] not in register_value):
                print_type_B(instructions_with_pc[keys])

            elif instructions_with_pc[keys][0] == "mov" or instructions_with_pc[keys][0] == "div" or instructions_with_pc[keys][0] == "not" or instructions_with_pc[keys][0] == "cmp":
                print_type_C(instructions_with_pc[keys])

            elif instructions_with_pc[keys][0] == "ld" or instructions_with_pc[keys][0] == "st":
                print_type_D(instructions_with_pc[keys])

            elif instructions_with_pc[keys][0] == "jmp" or instructions_with_pc[keys][0] == "jlt" or instructions_with_pc[keys][0] == "jgt" or instructions_with_pc[keys][0] == "je":
                print_type_E(instructions_with_pc[keys])

            elif instructions_with_pc[keys][0] == "hlt":
                print_type_F(instructions_with_pc[keys])


# # writing output in output.txt file
# with open ('stdout.txt', 'w') as fout:
#     for i in output:
#         fout.write(str(i))
#         fout.write("\n")

# output
for i in output:
    sys.stdout.write(str(i)+"\n")

# END OF THE ASSIGNMENT