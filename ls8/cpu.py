"""CPU functionality."""

import sys


HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256
        self.reg = [None] * 8
        self.pc = 0
        self.sp = 0
        self.index = 0
        self.functions = {
            PUSH: self.push,
            POP: self.pop,
            LDI: self.ldi,
            PRN: self.prn,
            MUL: self.mul,
        }

    def ldi(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
        self.pc += 3
        print("ldi reg:", self.reg)

    def prn(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def mul(self):
        self.alu("MUL", self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
        self.pc += 3

    def push(self):
        self.pc -= 1
        value = self.reg[self.index]
        self.index += 1
        print(f"Push value {value} into spot {self.index}")
        self.ram_write(self.pc, value)

    def pop(self):
        target = operand[0]
        value = self.ram_read(self.pc)
        self.reg[target] = value
        self.pc += 1

    def load(self, file):
        """Load a program into memory."""

        address = 0

        program = []

        with open(file) as f:
            for line in f:
                line = line.split("#")
                line = line[0].strip()
                program.append(int(line, 2))

            for command in program:
                self.ram[address] = command
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def run(self):
        """Run the CPU."""
        while self.ram_read(self.pc) != HLT:
            command = self.ram_read(self.pc)
            # print(command)
            try:
                self.functions[command]()
            except Exception:
                return print(f"Command: {command} was not found at index {self.pc}")

    def ram_read(self, key):
        # print("RAM read:", key, self.ram[key])
        return self.ram[key]

    def ram_write(self, key, value):
        # print(f"{value} written to {key} in RAM")
        self.ram[key] = value
