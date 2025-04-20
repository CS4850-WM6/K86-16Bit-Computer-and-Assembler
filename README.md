# K86 16Bit Computer and Assembler

A Multisim and Python implementation of a custom computer architecture design in 16-bit.

With this project, we designed a general-purpose 16-bit RISC+CISC computer architecture, alongside an assembler, and instruction loader. Our computer architecture, K86 (Kennesaw 86), is inspired by the Intel x86 and ARM architectures that have enabled computing systems to perform many of the modern functionalities we rely on today. To allow for fluid programming and processing, KASM (Kennesaw Assembler) translates assembly code into machine instructions which will be stored in the computer memory by the loader. With all these components integrated together, our project defines much of the foundation of a sophisticated computing system.

## Project Overview

Our K86 hybrid RISC+CISC instruction set architecture (ISA) contains 61 different machine instructions capable of performing 6 different instruction types, including arithmetic, logic, branching, data movement, control flow, and I/O. RISC (Reduced Instruction Set Computer) design principles were incorporated with additional CISC (Complex ISC) instructions where useful. Escape codes and variable-length instructions were used to garner as much bandwidth as possible from our 16-bit instruction words, by adding both to the number of instructions and operand length.

The hardware organization and architecture (Fig. 1) follows the Von Neumann model, meaning the control unit and ALU (Arithmetic-Logical Unit) are connected to a single memory bank through one bus. To improve upon the x86 architecture, we incorporated a bank of 16 different general-purpose registers for greater operand and address storage. A fully autonomous control unit, containing an instruction decoder and read-only special-purpose registers, runs continuous FDE (Fetch-Decode-Execute) cycles to process instructions.
![Figure 1](https://github.com/user-attachments/assets/6604c0a0-6570-4d54-9ffe-ade2aa0a14b1)

To make the computer usable, the KASM assembler translates K86 code into machine instructions which can be uploaded directly to the computer memory in the digital circuit simulation. These data are stored into the 8 KB memory in big endian format, then executed by the control unit with the click of a button. 

## Components

K86 Instruction Set
To define the basic aspects of K86 architecture, we used x86 CISC and ARM RISC architecture as our primary references when designing our instruction set. An ISA table was created to define all instructions the computer is capable of processing as well as the syntax for writing them. A snippet of the table is shown by Fig. 2. The full ISA table is available on our website, kowi.cc.

KASM Assembler
The KASM assembler is written in Python and can process K86 code with two main sections, .data, for declaring variable names and their values, and .code, where instructions and subprocesses are written. When a variable is declared in the .data section, its value is loaded into R0, it is assigned a memory address and is then stored into that address. Instructions in the .code section are checked for correct syntax and processed according to the instruction set. Fig. 3 shows sample code of a program for calculating the factorial of an input, and Fig.4 is the output for that code with comments explaining what instruction each line does. More detailed examples and process explanations can be found on our website.

![Figure 3](https://github.com/user-attachments/assets/9d8180cb-0727-4b56-b3d3-d81e96e4ef31)

![Figure 4](https://github.com/user-attachments/assets/dce10b19-6aa6-42bc-a831-00751ac2342d)

Digital Logic Circuit Simulation
NI Multisim was used to create the circuit design of the computer. TIL (technology independent logic) components were used when possible to keep our simulation free of analog factors. Hierarchical blocks were used for modularity. Fig. 5 demonstrates the computer memory design, including the circuit to upload assembly code. Fig. 6 shows the instruction and address mode selector of the instruction decoder.

![Figure 5](https://github.com/user-attachments/assets/7d4036de-da9e-4fb7-95c5-dc5bb3518f8f)

![Figure 6](https://github.com/user-attachments/assets/d92fa062-e183-4416-a417-a2d00d70faa4)
