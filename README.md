# K86 16-Bit Computer and Assembler

This is a Multisim and Python implementation of a custom computer architecture design in 16-bit.

With this project, we designed a general-purpose 16-bit RISC+CISC computer architecture, alongside an assembler, and instruction loader. Our computer architecture, Kennesaw State 86 (K86), is inspired by the Intel x86 and ARM architectures that have enabled computing systems to perform many of the modern functionalities we rely on today. To allow for fluid programming and processing, the assembler translates Kennesaw State Assembly (KASM) code into machine instructions which will be stored in the computer memory by the loader. With all these components integrated together, our project defines much of the foundation of a sophisticated computing system (Fig. 1).

![System Components](https://github.com/user-attachments/assets/f0121835-141d-45e4-b595-85cc112722a9)

*Figure 1: Project Components*


## Project Overview

Our K86 hybrid RISC+CISC instruction set architecture (ISA) contains 61 different machine instructions capable of performing 6 different instruction types, including arithmetic, logical, branching, data movement, control flow, and I/O. RISC (Reduced Instruction Set Computer) design principles were incorporated with additional CISC (Complex Instruction Set Computer) instructions where useful. Variable-length opcode and variable-length instructions were used to garner as much bandwidth as possible from our 16-bit instruction words, by adding both to the number of instructions and operand length.

The hardware organization and architecture (Fig. 2) follow the Von Neumann model, meaning the control unit and ALU (Arithmetic-Logical Unit) are connected to a single memory bank through one bus. To improve upon the x86 architecture, we incorporated a bank of 16 different general-purpose registers for greater operand and address storage. A fully autonomous control unit, containing an instruction decoder and read-only special-purpose registers, runs continuous FDE (Fetch-Decode-Execute) cycles to process instructions.

![Architectural Block Diagram](https://github.com/user-attachments/assets/ff32e526-153c-4d0c-bc0e-ed609bee5f53)

*Figure 2: Architectural Block Diagram*

To make the computer usable, the assembler translates KASM assembly code into K86 machine instructions which can be uploaded directly to the computer memory in the digital circuit simulation. These data are stored into the 8 KB memory in big endian format, then executed by the control unit with the click of a button. 

## Components

### K86 Instruction Set
To define the basic aspects of K86 architecture, we used x86 CISC and ARM RISC architecture as our primary references when designing our instruction set. An ISA table was created to define all instructions the computer is capable of processing as well as the syntax for writing them. To get as many instructions out of a 16-bit word as possible, longer opcodes are used for instructions which require less operand space in the instruction word. Additionally, certain instructions use double-length words so that a second word can hold an entire 16-bit operand value for full use of the 16-bit ALU.

#### ISA Tables

![ISA Table Section 1](https://github.com/user-attachments/assets/37fb192f-6fd7-4957-9f3d-c12f68fd8a0a)
![ISA Table Section 2](https://github.com/user-attachments/assets/5b3977a4-8f81-401d-aca8-3ba494aae433)
![ISA Table Section 3](https://github.com/user-attachments/assets/4e2cefd5-dcb9-4ead-8fec-1fdc5fdae9e1)
![ISA Table Section 4](https://github.com/user-attachments/assets/0e3fa716-6fb1-471c-9dc0-18727dbf68f6)

*Figures 3-7: ISA Tables*

### KASM Assembler
The KASM assembler is written in Python and can process KASM with two main sections, .data, for declaring variable names and their values, and .code, where instructions and subprocesses are written. When a variable is declared in the .data section, its value is loaded into R0, it is assigned a memory address and is then stored into that address. Instructions in the .code section are checked for correct syntax and processed according to the instruction set. Fig. 8 shows sample code of a program for calculating the factorial of an input, and Fig. 9 is the output for that code with comments explaining what instruction each line does. More detailed examples and process explanations can be found on our website.

![KASM Programming](https://github.com/user-attachments/assets/dce10b19-6aa6-42bc-a831-00751ac2342d)

*Figure 8: Factorial Program in KASM*

*Figure 9: Resulting Binary Output*

### Digital Logic Circuit Simulation
NI Multisim was used to create the circuit design of the computer. TIL (technology independent logic) components were used when possible to keep our simulation free of analog factors. Hierarchical blocks were used for modularity. Two examples of our circuits are given below. Fig. 10 demonstrates the computer memory design, including the circuit to upload assembled machine instructions. Fig. 11 shows the instruction and address mode selector of the instruction decoder.

![Memory Unit](https://github.com/user-attachments/assets/f8fc3eb9-a69c-4623-85d7-f5aff4a42a34)

*Figure 10: Memory Unit*

![Instruction Decoder](https://github.com/user-attachments/assets/d92fa062-e183-4416-a417-a2d00d70faa4)

*Figure 11: Instruction and Addressing Selector*

## Setup

To simulate the use of this 16-bit computer, the following setup process will be used.

1. A user will first generate a program in the KASM assembler. Users may reference
the programming manual on our website, which will detail the syntax, instruction
mnemonics, and functions of those mnemonics. Once a program is ran, the
resulting list of binary instructions will save to a .dp file may be input into
Multisim.

3. The user will start the simulation in Multisim and load the .dp file into the Word
Generator within the Memory Unit (Fig. 12). This will be done using digital inputs
connected to the logic circuit control unit, which will save these instructions into
the instruction memory in order of arrival.

![Word Generator Upload](https://github.com/user-attachments/assets/d5a97a82-7a69-40bf-8d15-4560acec6287)

*Figure 12: Inputting Instructions into Word Generator*

3. Once in the instruction memory, the control unit will automatically execute the
instructions until the instruction memory is empty. To view the execution results,
a user may store outputs in a chosen memory location and then print them using
the PRINTM instruction. After the program is complete, the user may stop the
simulation to end execution.

## Presentation and Project Website

Video presentation of our computer architecture: https://vimeo.com/1075565416

Our project website: https://kowi.cc


