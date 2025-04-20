#     KASM Version 1
#     WM-6 AdvCompArch

 
import sys

# Memory sizes
instruction_memory_size = 2048
data_memory_size = 1024

# Global variables
line = ""
linenumber = 0
mode = 0
filename = ""

# Keeps track of if a memory location is assigned to something
instruction_memory = [False] * instruction_memory_size
data_memory = [False] * data_memory_size

# Stores the instructions before they are written to the output file,
# this is needed because in the first pass through the file, because subprocesses can be anywhere in the file.
# Their tokens, when used, are written as text into the binary, for example JMP Finish, would store as
# 0000Finish in the memory lines array. Once the file is fully scanned once, it goes through these memory lines
# and replaces all the tokens with their actual values. If the token doesn't exist, it throws an error
memory_lines = []

# Keeps track of user-made subprocess names
subprocess_names = {}

# Variable names
user_defined_tokens = {}

# Dictionary of all the K86 instruction codes
k86_tokens = {
    "JMP": "0001",
    "JZ": "0010",
    "JNZ": "0011",
    "JC": "0100",
    "JNC": "0101",
    "JGT": "0110",
    "JLT": "0111",
    "JO": "1000",
    "JNO": "1001",
    "JP": "1010",
    "JNP": "1011",
    "ADD": "11110000",
    "SUB": "11110001",
    "MULT": "11110010",
    "DIV": "11110011",
    "AND": "11110100",
    "OR": "11110101",
    "XOR": "11110110",
    "SHL": "11110111",
    "SHR": "11111000",
    "ROL": "11111001",
    "ROR": "11111010",
    "LOADR": "11111011",
    "SWAP": "11111100",
    "CMP": "11111101",
    "TEST": "11111110",
    "ADDI": "111111110000",
    "SUBI": "111111110001",
    "MULTI": "111111110010",
    "DIVI": "111111110011",
    "LOADI": "111111110100",
    "LOADM": "111111110101",
    "LOADA": "111111110110",
    "STORE": "111111110111",
    "CLEAR": "111111111000",
    "NOT": "111111111001",
    "NEG": "111111111010",
    "PUSH": "111111111011",
    "POP": "111111111100",
    "PRINT": "111111111110",
    "SKIPZ": "1111111111110000",
    "SKIPNZ": "1111111111110001",
    "SKIPC": "1111111111110010",
    "SKIPNC": "1111111111110011",
    "SKIPGT": "1111111111110100",
    "SKIPLT": "1111111111110101",
    "SKIPO": "1111111111110110",
    "SKIPNO": "1111111111110111",
    "SKIPP": "1111111111111000",
    "SKIPNP": "1111111111111001",
    "PUSHPC": "1111111111111010",
    "RET": "1111111111111011",
    "INPUT": "1111111111111100",
    "NOP": "1111111111111101",
    "SYS": "1111111111111110",
    "HALT": "1111111111111111"}

# Register Names
registers = {
    "R0": "0000",
    "R1": "0001",
    "R2": "0010",
    "R3": "0011",
    "R4": "0100",
    "R5": "0101",
    "R6": "0110",
    "R7": "0111",
    "R8": "1000",
    "R9": "1001",
    "R10": "1010",
    "R11": "1011",
    "R12": "1100",
    "R13": "1101",
    "R14": "1110",
    "R15": "1111",

}


def run():
    global line
    global filename
    global linenumber
    global mode
    with open(filename, "r") as reader:
        for line in reader:
            linenumber += 1
            line = line.strip()  # Removes whitespace surrounding line
            temp = line.split("#")  # makes '#' into the comment character
            tempstr = temp[0]
            lineargs = tempstr.split()
            if len(lineargs) > 0:  # this if statement just makes sure to skip all empty lines

                # parse statement can do multiple things depending on if it's in the .data or
                # .code section, so this changes it if a new section appears, otherwise parses the line
                if lineargs[0] == ".data":
                    mode = 1
                elif lineargs[0] == ".code":
                    mode = 2
                else:
                    parse(lineargs)

    # After the file is fully scanned, this replaces any subprocess and variable names that were defined,
    # then writes it to the file
    index = 0
    for line in memory_lines:
        if not isdigit(line[4:]):
            if line[4:] in subprocess_names:
                memory_lines[index] = line[0:4] + subprocess_names[line[4:]]
            elif line[4:] in user_defined_tokens:
                memory_lines[index] = line[0:4] + user_defined_tokens[line[4:]]
            else:
                sys.exit(f"Undefined token at line {linenumber}")
        index += 1
    fileparts = filename.split('.')
    filename =fileparts[0]
    file = open(f"{filename}.bin", "w")
    for i in memory_lines:
        file.write(i + "\n")

        # if there's no halt command, the program will run forever, since 16
        # zeros is technically an instruction, this adds a halt at the end in case
    if "1111111111111111" not in memory_lines:
        file.write("1111111111111111\n")


def parse(lineargs):
    global linenumber

    # Mode 1 is the .data section, is used for defining variable names
    if mode == 1:
        if len(lineargs) != 2:
            sys.exit(
                f"Error at line {linenumber}:  Variable declarations in the .data section must be 2 arguments: a "
                f"token and a value.")
        else:
            if lineargs[0] in k86_tokens or lineargs[0] in registers:
                sys.exit(f"Error at line {linenumber}:  Provided token is a K86 token.")
            if lineargs[0] in user_defined_tokens:
                sys.exit(f"Error at line {linenumber}:  Duplicate token.")
            else:
                memalloc(lineargs[0], lineargs[1])

    # Mode 2 is the .code section, mostly made of one switch statement
    # which decides how to process each line in the code section
    if mode == 2:
        match lineargs[0]: # Ugliest part of the code
            case "JMP":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                jump_type(lineargs[0], lineargs[1])
            case "JZ":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                jump_type(lineargs[0], lineargs[1])
            case "JNZ":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                jump_type(lineargs[0], lineargs[1])
            case "JC":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                jump_type(lineargs[0], lineargs[1])
            case "JNC":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                jump_type(lineargs[0], lineargs[1])
            case "JGT":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                jump_type(lineargs[0], lineargs[1])
            case "JLT":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                jump_type(lineargs[0], lineargs[1])
            case "JO":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                jump_type(lineargs[0], lineargs[1])
            case "JNO":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                jump_type(lineargs[0], lineargs[1])
            case "JP":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                jump_type(lineargs[0], lineargs[1])
            case "JNP":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                jump_type(lineargs[0], lineargs[1])
            case "ADD":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_register(lineargs[0], lineargs[1], lineargs[2])
            case "SUB":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_register(lineargs[0], lineargs[1], lineargs[2])
            case "MULT":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_register(lineargs[0], lineargs[1], lineargs[2])
            case "DIV":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_register(lineargs[0], lineargs[1], lineargs[2])
            case "AND":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_register(lineargs[0], lineargs[1], lineargs[2])
            case "OR":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_register(lineargs[0], lineargs[1], lineargs[2])
            case "XOR":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_register(lineargs[0], lineargs[1], lineargs[2])
            case "SHL":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                shifters(lineargs[0], lineargs[1], lineargs[2])
            case "SHR":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                shifters(lineargs[0], lineargs[1], lineargs[2])
            case "ROL":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                shifters(lineargs[0], lineargs[1], lineargs[2])
            case "ROR":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                shifters(lineargs[0], lineargs[1], lineargs[2])
            case "LOADR":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_register(lineargs[0], lineargs[1], lineargs[2])
            case "SWAP":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_register(lineargs[0], lineargs[1], lineargs[2])
            case "CMP":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_register(lineargs[0], lineargs[1], lineargs[2])
            case "TEST":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_register(lineargs[0], lineargs[1], lineargs[2])
            case "ADDI":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                immediate_type(lineargs[0], lineargs[1], lineargs[2])
            case "SUBI":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                immediate_type(lineargs[0], lineargs[1], lineargs[2])
            case "MULTI":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                immediate_type(lineargs[0], lineargs[1], lineargs[2])
            case "DIVI":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                immediate_type(lineargs[0], lineargs[1], lineargs[2])
            case "LOADI":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                immediate_type(lineargs[0], lineargs[1], lineargs[2])
            case "LOADM":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_word_memory_type(lineargs[0], lineargs[1], lineargs[2])
            case "LOADA":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_word_memory_type(lineargs[0], lineargs[1], lineargs[2])
            case "STORE":
                if len(lineargs) != 3: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                two_word_memory_type(lineargs[0], lineargs[1], lineargs[2])
            case "CLEAR":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                one_operand(lineargs[0], lineargs[1])
            case "NOT":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                one_operand(lineargs[0], lineargs[1])
            case "NEG":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                one_operand(lineargs[0], lineargs[1])
            case "PUSH":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                one_operand(lineargs[0], lineargs[1])
            case "POP":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                one_operand(lineargs[0], lineargs[1])
            case "PRINT":
                if len(lineargs) != 2: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                one_operand(lineargs[0], lineargs[1])
            case "SKIPZ":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "SKIPNZ":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "SKIPC":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "SKIPNC":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "SKIPGT":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "SKIPLT":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "SKIPO":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "SKIPNO":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "SKIPP":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "SKIPNP":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "PUSHPC":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "RET":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "INPUT":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "NOP":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "SYS":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case "HALT":
                if len(lineargs) != 1: sys.exit(f"Error at line {linenumber}: Invalid instruction syntax.")
                no_operand(lineargs[0])
            case _:  # This case handles the subprocess names
                temp = lineargs[0]
                length = len(temp)
                if len(lineargs) == 1 and temp[length - 1] == ':':
                    temp = temp[0:length - 1]
                    subprocess_names[temp] = get_next_instr_addr()
                else:
                    sys.exit(f"Unexpected token at line {linenumber}")


# Only being used by the subprocess handler above.
# it fetches the next unused instruction address without actually assigning it
def get_next_instr_addr():
    index = 0
    while instruction_memory[index]:
        index += 1
    return format(index, f'0{12}b')


# Allocates memory for the variables in the data section
def memalloc(token, value):
    finalval = ""

    # For unknown vars
    if value == "?":
        value = "0"
        finalval = to_signed_binary(0)

    # Hexadecimal value
    elif value.startswith("0x"):
        finalval = to_signed_binary(int(value, 16))

    # Decimal value
    elif isdigit(value) or (value[0] == "-" and isdigit(value[1:])):
        finalval = to_signed_binary(int(value))
    else:
        sys.exit(f"Invalid value format: {value}")

    # Allocates memory for whatever variable it's processing
    index = 0
    while data_memory[index]:
        index += 1
        if index >= data_memory_size:
            sys.exit("Out of data memory!")
    data_memory[index] = True
    index = index + instruction_memory_size  # puts it in the data memory zone

    # Adds the variable to the user defined tokens, then creates load and store instructions for that value
    user_defined_tokens[token] = format(index, f'0{12}b')
    immediate_type("LOADI", "R0", value)
    two_word_memory_type("STORE", "R0", index)


# Converts the input number to a signed binary value
def to_signed_binary(number):
    number = int(number)  # Ensure it's an integer
    if number < 0:
        number = (1 << 16) + number  # Convert to two's complement
    return format(number & 0xFFFF, f'0{16}b')


# ISA Section 1
# Handles all the jump instructions
def jump_type(instruction_code, op1):
    if isdigit(op1):
        temp = format(op1, f'0{12}b')
        memory_lines.append(k86_tokens[instruction_code] + temp)
    else:
        memory_lines.append(k86_tokens[instruction_code] + op1)
    setinstrmem1()


# ISA Section 2
# Handles add, sub, mult, div, and, or, xor, loadr, swap, cmp, test
def two_register(instruction_code, op1, op2):
    if ',' in op1:
        op1 = op1[0:op1.find(',')]
    if op1 in registers and op2 in registers:
        memory_lines.append(k86_tokens[instruction_code] + registers[op1] + registers[op2])
    else:
        sys.exit(f"Invalid format at line {linenumber}.")
    setinstrmem1()


# Handles shl, shr, rol, ror
def shifters(instruction_code, op1, op2):
    if ',' in op1:
        op1 = op1[0:op1.find(',')]
    if op1 in registers and isdigit(op2):
        memory_lines.append(k86_tokens[instruction_code] + registers[op1] + format(op2, f'0{4}b'))
    else:
        sys.exit(f"Invalid format at line {linenumber}.")
    setinstrmem1()


# ISA Section 3
# Handles addi, subi, multi, divi, loadi
def immediate_type(instruction_code, op1, op2):
    if ',' in op1:
        op1 = op1[0:op1.find(',')]
    if op1 in registers:
        memory_lines.append(k86_tokens[instruction_code] + registers[op1])
        memory_lines.append(to_signed_binary(op2))
    else:
        sys.exit(f"Invalid format at line {linenumber}.")
    index = 0
    while instruction_memory[index]:
        index += 1
    instruction_memory[index] = True
    instruction_memory[index + 1] = True


# Handles loadm, loada, store
def two_word_memory_type(instruction_code, op1, op2):
    if ',' in op1:
        op1 = op1[0:op1.find(',')]
    if op1 in registers:
        memory_lines.append(k86_tokens[instruction_code] + registers[op1])
        if isdigit(op2):
            memory_lines.append("0000" + format(op2, f'0{12}b'))
        else:
            memory_lines.append("0000" + op2)
        index = 0
        while instruction_memory[index]:
            index += 1
        instruction_memory[index] = True
        instruction_memory[index + 1] = True
    else:
        sys.exit(f"Invalid format at line {linenumber}.")


# Handles clear, not, neg, push, pop, ret, and print
def one_operand(instruction_code, op1):
    if op1 in registers:
        memory_lines.append(k86_tokens[instruction_code] + registers[op1])
        setinstrmem1()
    else:
        sys.exit(f"Invalid format at line {linenumber}.")


# ISA Section 4
# Handles the skips, input, nop, sys, halt
def no_operand(instruction_code):
    memory_lines.append(k86_tokens[instruction_code])
    setinstrmem1()


# Updates what instruction memory is being used
def setinstrmem1():
    index = 0
    while instruction_memory[index]:
        index += 1
    instruction_memory[index] = True


# Method for checking if a string is made of numbers only
def isdigit(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# Main, just checking the usage is right and then running
def main():
    global filename
    if len(sys.argv) != 2:  # Check if arguments were passed
        sys.exit("Usage: kasm.py [file name]")
    else:
        filename = sys.argv[1]
        temp = filename.split('.')
        if temp[1] == "k86":
            run()
        else:
            sys.exit("KASM can only process .k86 files!")


if __name__ == "__main__":
    main()
