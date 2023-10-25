# Custom ISA Assembler

This is an assembler for a custom Instruction Set Architecture (ISA) implemented in Python. The assembler can decode and process a set of instructions, check for errors, and generate binary code for a CPU with limited instruction formats.

## Table of Contents

- [Introduction](#introduction)
- [Instruction Format](#instruction-format)
- [Usage](#usage)
- [Contributors](#contributors)

## Introduction

This assembler is designed for a custom ISA with a limited set of instructions, each represented by a specific opcode and operand format. The supported instruction types are A, B, C, D, E, and F, each with its own unique encoding format. The program reads input instructions from a file named "stdin.txt" and outputs the corresponding binary code to "stdout.txt".

## Instruction Format

The ISA supports six types of instructions, each with a specific format:

- Type A Instructions (add, sub, mul, xor, or, and):
  ```
  <Opcode>     <Unused>   <reg 1>    <reg 2>   <reg 3>
   5 bits        2 bits     3 bits     3 bits     3 bits
  ```

- Type B Instructions (mov, ls, rs):
  ```
  <Opcode>    <Unused>   <reg 1>    <Immediate>
  5 bits     1 bit     3 bits         7 bits
  ```

- Type C Instructions (mov, div, not, cmp):
  ```
  <Opcode>    <Unused>   <reg 1>    <reg 2>
   5 bits     5 bits   3 bits      3 bits
  ```

- Type D Instructions (ld, st):
  ```
  <Opcode> <Unused>   <reg 1>   <Memory Address>
  5 bits    1 bit   3 bits         7 bits
  ```

- Type E Instructions (jmp, jlt, je, jgt):
  ```
  <Opcode>  <Unused>  <Memory Address>
  5 bits  4 bits       7 bits
  ```

- Type F Instructions (hlt):
  ```
  <Opcode>   <Unused>
  5 bits    11 bits
  ```

## Usage

1. Clone this repository to your local machine:
   ```shell
   git clone https://github.com/your-username/custom-isa-assembler.git
   ```

2. Navigate to the project directory:
   ```shell
   cd custom-isa-assembler
   ```

3. Prepare the input file "stdin.txt" with a list of instructions to be processed.

4. Run the assembler with Python:
   ```shell
   python assembler.py
   ```

5. The assembler will process the input instructions and write the binary output to "stdout.txt." Any encountered errors will also be displayed in "stdout.txt."

## Contributors

This project was created by the following contributors in 2023:

- [Vikranth](https://github.com/Vikranth3140)
- [Rohan](https://github.com/rohan-0448)
- [Pritha](https://github.com/pritha-ctrl)
- [Swara](https://github.com/swara14)

Please feel free to contribute to this project, report issues, or suggest improvements.

Happy coding! 🚀