"""CPU functionality."""

import sys

# opcodes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
ADD = 0b10100000
SUB = 0b10100001
DIV = 0b10100011
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False
        self.sp = 7             # R7, from specs
        self.reg[self.sp] = 244     # F4, from specs
        self.fl = 0b00000000

    def ram_read(self, mem_address):
        """
        Standard CPUs contain a register called
        Memory Address Register(MAR). MAR contains mem addreses
        being read/written to. [Google] Memory Data Register.

        """
        return self.ram[mem_address]

    def ram_write(self, mem_address, data):
        self.ram[mem_address] = data

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        try:
            with open(filename) as f:
                for line in f:
                    line_split = line.split("#")
                    num = line_split[0].strip()

                    if num == "":
                        continue

                    self.ram[address] = int(num, 2)

                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found!")
            sys.exit(2)

        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000110,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "DIV":
            # Floor division because we don't want to store floats. Headick!
            self.reg[reg_a] //= self.reg[reg_b]
        elif op == "CMP":
            if reg_a == reg_b:
                self.fl = 0b00000001
            elif reg_a < reg_b:
                self.fl = 0b00000100
            else:
                self.fl = 0b00000010
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while True:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            instruction_length = (ir >> 6) + 1

            if ir == LDI:
                self.reg[operand_a] = operand_b
            elif ir == PRN:
                print(self.reg[operand_a])
            elif ir == HLT:
                break
            elif ir == ADD:
                self.alu("ADD", operand_a, operand_b)
            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
            elif ir == SUB:
                self.alu("SUB", operand_a, operand_b)
            elif ir == CMP:
                self.alu("CMP", operand_a, operand_b)
            elif ir == DIV:
                self.alu("DIV", operand_a, operand_b)
            elif ir == PUSH:
                val = self.reg[operand_a]

                self.reg[self.sp] -= 1   # decrement whats in R7 by 1
                # place the `val` in memory, at the sp address
                self.ram[self.reg[self.sp]] = val

            elif ir == POP:
                """
                Place the value in top of stack into given register address
                """
                val = self.ram[self.reg[self.sp]]

                self.reg[operand_a] = val

                self.reg[self.sp] += 1

            else:
                print("I do not understand that command")

            self.pc += instruction_length
