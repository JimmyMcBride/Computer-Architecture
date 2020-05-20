"""CPU functionality."""
import sys

PC = 4
SP = 7

START = 0b11110011

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001

MUL = 0b10100010
ADD = 0b10100000


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [None] * 256
        self.reg = [None] * 8
        self.reg[PC] = 0
        self.reg[SP] = START

        self.operations = {
            PRN: self.prn,
            LDI: self.ldi,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret,
        }

    def load(self, file):
        address = 0
        with open(file) as f:
            for line in f:
                line = line.split("#")
                line = line[0].strip()

                if line == "":
                    continue
                self.ram[address] = int(line, 2)
                address += 1

    def alu(self, op, operands):
        """ALU operations."""
        reg_a, reg_b = operands

        if op == ADD:
            print("ADD")
            print(f"{reg_a} is {self.reg[reg_a]}")
            print(f"{reg_b} is {self.reg[reg_b]}")
            self.reg[reg_a] += self.reg[reg_b]
            print("equals...")
            print(f"{self.reg[reg_a]}")
        elif op == MUL:
            print("MUL")
            print(f"{reg_a} is {self.reg[reg_a]}")
            print(f"{reg_b} is {self.reg[reg_b]}")
            self.reg[reg_a] *= self.reg[reg_b]
            print("equals...")
            print(f"{self.reg[reg_a]}")
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.reg[PC],
                # self.fl,
                # self.ie,
                self.ram_read(self.reg[PC]),
                self.ram_read(self.reg[PC] + 1),
                self.ram_read(self.reg[PC] + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def ram_read(self, key):
        return self.ram[key]

    def ram_write(self, key, value):
        self.ram[key] = value

    def run(self):
        halted = False
        while not halted:
            next_command = self.ram_read(self.reg[PC])
            halted = self.execute(next_command)

    def execute(self, command):
        cmd = self.parse_command(command)
        if command is HLT:
            return True

        num_ops, is_alu, sets_pc, cmd_id = cmd.values()
        operands = [None] * num_ops

        for i in range(len(operands)):
            operand = self.ram_read(self.reg[PC] + i + 1)
            operands[i] = operand
        if is_alu:
            self.alu(command, operands)
        else:
            self.operations[command](operands)

        if not sets_pc:
            self.reg[PC] += num_ops + 1

        return False

    def parse_command(self, cmd):
        num_ops = int((0b11000000 & cmd) >> 6)
        is_alu = bool((0b00100000 & cmd) >> 5)
        sets_pc = bool((0b00010000 & cmd) >> 4)
        cmd_id = 0b00001111 & cmd

        return {
            "num_ops": num_ops,
            "is_alu": is_alu,
            "sets_pc": sets_pc,
            "cmd_id": cmd_id,
        }

    def prn(self, operand):
        index = operand[0]
        print("[prn] op_index", operand[0])
        value = self.reg[index]
        print(value)

    def ldi(self, operands):
        index, value = operands
        print(f"[ldi] op's:// index: {index}, value: {value}")
        self.reg[index] = value
        print(f"[ldi] reg: {self.reg}")

    def push(self, operand):
        index = operand[0]
        print("[push] op_index", operand[0])
        self.reg[SP] -= 1
        value = self.reg[index]
        stack_address = self.reg[SP]
        self.ram_write(stack_address, value)
        print(f"[push] reg: {self.reg}")

    def pop(self, operand):
        index = operand[0]
        print("[pop] op_index", operand[0])
        stack_address = self.reg[SP]
        value = self.ram_read(stack_address)
        self.reg[index] = value
        self.reg[SP] += 1
        print(f"[pop] reg: {self.reg}")

    def call(self, operand):
        index = operand[0]
        print("[call] op_index", operand[0])
        self.reg[PC] += 2
        self.push([PC])
        sub_routine_address = self.reg[index]
        self.reg[PC] = sub_routine_address
        print(f"[call] reg: {self.reg}")

    def ret(self, operand):
        self.pop([PC])
        print(f"[ret] reg: {self.reg}")
