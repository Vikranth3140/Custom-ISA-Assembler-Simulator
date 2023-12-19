# CO_PROJECT_2023 - Rohan, Pritha, Swara, Vikranth

import sys

# opcode (predefined)
opcode={"00000":"add", "00001": "sub", "00010":"mov2", "00011":"mov", "00100":"ld", "00101":"st", "00110":"mul", "00111":"div", "01000":"rs", "01001":"ls", "01010":"xor", "01011":"or", "01100":"and", "01101":"not", "01110":"cmp", "01111":"jmp", "11100":"jlt", "11101":"jgt", "11111":"je", "11010":"hlt"}

# registers (predefined) and default values = 0
register={"000": "R0","001": "R1","010": "R2","011": "R3","100": "R4","101": "R5","110": "R6","111": "FLAGS"}
register_value={"R0":"0000000000000000","R1":"0000000000000000","R2":"0000000000000000","R3":"0000000000000000","R4":"0000000000000000","R5":"0000000000000000","R6":"0000000000000000","FLAGS":"0000000000000000"}
memory_dictionary={}

# flags (predefined)
flags={"V":"0000000000001000","L": "0000000000000100","G": "0000000000000010","E": "0000000000000001","reset":"0000000000000000"}

# input

# initialise mem

def initialise(l):
    # with open("sampletest_sim.txt") as fin:
    #     for i in fin:
    #         l.append(str(i.strip()))

    input=sys.stdin
    for elt in input:
        l.append(elt.strip())

l=[]
initialise(l)

program_counter = 0
end = 0
temp_flag = flags["reset"]
temp_pc = 0

halted = False

# for i in l:
#     print(i)

output_file=[]
line=0

def bin_to_floating(binary):
    exp = binary[:3]
    mant = binary[3:]

    exp = exp[::-1]

    result1 = 0
    for i, digit in enumerate(exp):
        digit_value = int(digit)
        result1 += digit_value * (2 ** i)

    result2 = 0
    for i in range(len(mant)):
        digit_value = int(mant[i])
        power = -i - 1
        result2 += digit_value * (2 ** power)

    return (result1+result2)
def floating_to_bin(val):
    if val <= 0.0:
        return '00000000'

    binary = ''

    integer_part = int(val)
    binary += bin(integer_part)[2:]
    binary = "0"*(3-len(binary)) + binary

    fractional_part = val - integer_part
    while fractional_part != 0:
        fractional_part *= 2
        bit = str(fractional_part).split('.')[0]
        binary += bit
        fractional_part -= int(bit)

    binary = "00000000"+((binary + "0"*(8-len(binary)))[:8])

    return binary

# def bin_to_dec(val): # R
#     # val = str(val)
#     if val == '0000000000000000':
#         return 0
#     val_f = 0
#     for i in range(len(val)):
#         val_f += int(val[15-i])*(2**i)
#     return val_f

def bin_to_dec(val):
    if len(val) < 16:
        val = '0' * (16 - len(val)) + val

    if val == '0000000000000000':
        return 0

    val_f = 0
    for i in range(len(val)):
        val_f += int(val[15-i]) * (2 ** i)
    return val_f


def dec_to_bin(val): # R
    if val <= 0:
        return '0000000000000000'
    val_f = ''
    while val > 0:
        val_f = str(val%2)+val_f
        val//=2
    val_f = (16-len(val_f))*"0"+val_f
    return val_f

def dec_to_bin_program_counter(val): # R
    if val == 0:
        return '0000000'
    val_f = ''
    while val > 0:
        val_f = str(val%2)+val_f
        val//=2
    val_f = (7-len(val_f))*"0"+val_f
    return val_f

def bin_to_dec_program_counter(val): # R
    if val == '0000000':
        return 0
    val_f = 0
    for i in range(len(str(val))):
        val_f += int(val[6-i])*(2**i)
    return val_f

def add_registers(register1, register2, register3): # V
    temp = bin_to_dec(register_value[register2]) + bin_to_dec(register_value[register3])
    if temp >= (2**16)-1:
        register_value['FLAGS'] = flags['V']
        register_value[register1] = "0000000000000000"
    else:
        register_value[register1] = dec_to_bin(temp)

def sub_registers(register1, register2, register3): # V
    if bin_to_dec(register_value[register3]) > bin_to_dec(register_value[register2]):
        register_value['FLAGS'] = flags['V']
        register_value[register1] = "0000000000000000"
    else:
        register_value[register1] = dec_to_bin(bin_to_dec(register_value[register2]) - bin_to_dec(register_value[register3]))

def move_immediate(register, immediate): # S
    register_value[register] = "000000000" + immediate

def move_registers(register1, register2): # P
    register_value[register1] = register_value[register2]

def load_from_memory(register, memory): # P
    if memory in memory_dictionary.keys():
        register_value[register] = memory_dictionary[memory]
    else:
        register_value[register] = "0000000000000000"
        memory_dictionary[memory] = "0000000000000000"

def store_into_memory(register, memory): # P
    # if  memory not in memory_dictionary.keys():
    memory_dictionary[memory] = register_value[register]

def multiply_registers(register1, register2, register3): # V
    temp = bin_to_dec(register_value[register2]) * bin_to_dec(register_value[register3])
    if temp > (2**16)-1:
        register_value['FLAGS'] = flags['V']
        register_value[register1] = "0000000000000000"
    else:
        register_value[register1] = dec_to_bin(temp)

def divide_registers(register1, register2): # P
    if bin_to_dec(register_value[register2])==0:
       register_value["R0"]=register_value["R1"]="0000000000000000"
       register_value["FLAGS"]=flags["V"]
    else:
        # register_value["R0"]=floating_to_bin(float(int(bin_to_dec(str(register_value[register1]))) / int(bin_to_dec(str(register_value[register2])))))
        register_value["R0"]=floating_to_bin(float(int(bin_to_floating(str(register_value[register1]))) / (bin_to_floating(str(register_value[register2])))))
        # register_value["R0"]=dec_to_bin(bin_to_dec(register_value[register1])//bin_to_dec(register_value[register2]))
        register_value["R1"]=dec_to_bin(bin_to_dec(register_value[register1]) % bin_to_dec(register_value[register2]))

def right_shift_by_imm(register, immediate): # S
    register_value[register] = dec_to_bin(bin_to_dec(register_value[register]) >> int(immediate))

def left_shift_by_imm(register, immediate): # S
    register_value[register] = dec_to_bin(bin_to_dec(register_value[register]) << int(immediate))

def xor_registers(register1, register2, register3): # V
    register_value[register1] = dec_to_bin(bin_to_dec(register_value[register2]) ^ bin_to_dec(register_value[register3]))

def or_registers(register1, register2, register3): # V
    register_value[register1] = dec_to_bin(bin_to_dec(register_value[register2]) | bin_to_dec(register_value[register3]))

def and_registers(register1, register2, register3): # V
    register_value[register1] = dec_to_bin(bin_to_dec(register_value[register2]) & bin_to_dec(register_value[register3]))

def not_registers(register1, register2): # P
    new_reg = ''
    temp = register_value[register2]
    for i in range(len(register_value[register2])):
        if temp[i] == '0':
            new_reg = new_reg + '1'
        elif temp[i] == '1':
            new_reg = new_reg + '0'
    register_value[register1] = new_reg

def compare_registers(register1, register2): # P
    if bin_to_dec(register_value[register1]) > bin_to_dec(register_value[register2]):
        register_value["FLAGS"] = flags["G"]
    elif bin_to_dec(register_value[register1]) < bin_to_dec(register_value[register2]):
        register_value["FLAGS"] = flags["L"]
    else:
        register_value["FLAGS"] = flags["E"]

def jump_to(memory): # P
    return bin_to_dec_program_counter(memory)

# def jump_lessthan(memory): # P
#     if register_value["FLAGS"]==flags["L"]:
#         return bin_to_dec_program_counter(memory)
#     else:
#         return memory

# def jump_greaterthan(memory): # R
#     if register_value["FLAGS"]==flags["G"]:
#         return bin_to_dec_program_counter(memory)
#     else:
#         return memory

# def jump_equal(memory): # R
#     if register_value["FLAGS"]==flags["E"]:
#         return bin_to_dec_program_counter(memory)
#     else:
#         return memory

def floating_add(register1, register2, register3): # V
    temp = bin_to_floating(register_value[register2][8:]) + bin_to_floating(register_value[register3][8:])
    if temp > 7.96875:
        register_value['FLAGS'] = flags['V']
        register_value[register1] = "0000000000000000"
    else:
        register_value[register1] = floating_to_bin(temp)

def floating_sub(register1, register2, register3): # V
    if bin_to_floating(register_value[register3]) > bin_to_floating(register_value[register2]):
        register_value['FLAGS'] = flags['V']
        register_value[register1] = "0000000000000000"
    else:
        register_value[register1] = floating_to_bin(bin_to_floating(register_value[register2][8:]) - bin_to_floating(register_value[register3][8:]))

def move_floating_immediate(register, immediate): # S
   register_value[register] = floating_to_bin(immediate)

def halt(): # R
    return True

def print_all(counter): # R
    global line
    line += 1
    print(dec_to_bin_program_counter(counter), end = " ")
    for keys in register_value:
        print(register_value[keys], end=" ")
    print()

while halted==False: # R
    instruction = l[program_counter]
    
    if instruction[:5]=="00000":
        add_registers(register[instruction[7:10]],register[instruction[10:13]],register[instruction[13:16]])
    elif instruction[:5]=="00001":
        sub_registers(register[instruction[7:10]],register[instruction[10:13]],register[instruction[13:16]])
    elif instruction[:5]=="00010":
        move_immediate(register[instruction[6:9]],instruction[9:16])
    elif instruction[:5]=="00011":
        move_registers(register[instruction[10:13]],register[instruction[13:16]])
    elif instruction[:5]=="00100":
        load_from_memory(register[instruction[6:9]],instruction[9:16])
    elif instruction[:5]=="00101":
        store_into_memory(register[instruction[6:9]],instruction[9:16])
    elif instruction[:5]=="00110":
        multiply_registers(register[instruction[7:10]],register[instruction[10:13]],register[instruction[13:16]])
    elif instruction[:5]=="00111":
        divide_registers(register[instruction[10:13]],register[instruction[13:16]])
    elif instruction[:5]=="01000":
        right_shift_by_imm(register[instruction[6:9]],instruction[9:16])
    elif instruction[:5]=="01001":
        left_shift_by_imm(register[instruction[6:9]],instruction[9:16])
    elif instruction[:5]=="01010":
        xor_registers(register[instruction[7:10]],register[instruction[10:13]],register[instruction[13:16]])
    elif instruction[:5]=="01011":
        or_registers(register[instruction[7:10]],register[instruction[10:13]],register[instruction[13:16]])
    elif instruction[:5]=="01100":
        and_registers(register[instruction[7:10]],register[instruction[10:13]],register[instruction[13:16]])
    elif instruction[:5]=="01101":
        not_registers(register[instruction[10:13]],register[instruction[13:16]])
    elif instruction[:5]=="01110":
        compare_registers(register[instruction[10:13]],register[instruction[13:16]])
        temp_flag = register_value["FLAGS"]
    elif instruction[:5]=="01111":
        temp_pc = jump_to(instruction[9:16])
    elif instruction[:5]=="11100":
        if register_value["FLAGS"]==flags["L"]:
            temp_pc = jump_to(instruction[9:16])
    elif instruction[:5]=="11101":
        if register_value["FLAGS"]==flags["G"]:
            temp_pc = jump_to(instruction[9:16])
    elif instruction[:5]=="11111":
        if register_value["FLAGS"]==flags["E"]:
            temp_pc = jump_to(instruction[9:16])
    elif instruction[:5]=="10000":
        floating_add(register[instruction[7:10]],register[instruction[10:13]],register[instruction[13:16]])
    elif instruction[:5]=="10001":
        floating_sub(register[instruction[7:10]],register[instruction[10:13]],register[instruction[13:16]])
    elif instruction[:5]=="10010":
        move_floating_immediate(register[instruction[5:8]],instruction[8:16])
    
    elif instruction[:5]=="11010":
        halted = halt()

    # print_all(program_counter)
    # register_value["FLAGS"] = flags["reset"]

    # pc + rf dump
    output_file.append(str(dec_to_bin_program_counter(program_counter)+"        "+register_value["R0"]+" "+register_value["R1"]+" "+register_value["R2"]+" "+register_value["R3"]+" "+register_value["R4"]+" "+register_value["R5"]+" "+register_value["R6"]+" "+temp_flag))
    if temp_pc != 0:
        program_counter = temp_pc
        temp_pc = 0
    else:
        program_counter += 1

    temp_flag = flags["reset"]

    if line == 128:
        halted = True

    if program_counter >= len(l):
        halted = True

    if halted == True:
        break
    

for i in l:
    output_file.append(i)
    line+=1

# mem dump
mem_dump=list(memory_dictionary.keys())
mem_dump.sort()
for i in mem_dump:
    output_file.append(memory_dictionary[i])
    line+=1

for i in range(128-line): # P
    output_file.append("0000000000000000")
    # print("0000000000000000")

# with open('sample_output.txt', 'w') as fout:
#     for i in output_file:
#         fout.write(str(i)+"\n")

for i in range(len(output_file)):
    # print(i,type(i))
    sys.stdout.write(str(output_file[i]))
    if i != len(output_file)-1:
        sys.stdout.write("\n")
