"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*256
        self.flags = 0b00000000
        self.running = False
        self.pc = 0
        self.sp = 7
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.ADD = 0b10100000
        self.SUB = 0b10100001
        self.MUL = 0b10100010
        self.DIV = 0b10100011
        self.CMP = 0b10100111
        self.ALU = [self.ADD, self.SUB, self.MUL, self.DIV, self.CMP]
        self.POP = 0b01000110
        self.PUSH = 0b01000101
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.JEQ = 0b01010101
        self.JNE = 0b01010110

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            self.reg[self.sp] = 244
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    val = int(n, 2)
                    self.ram[address] = val

                    address += 1

                    # print(f"{x:08b}: {x:d}")

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
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

        if op == self.ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == self.SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == self.MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == self.DIV:
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == self.CMP:
            a = self.reg[reg_a]
            b = self.reg[reg_b]

            if a == b:
                self.flag = 0b00000001
            elif a > b:
                self.flag = 0b00000010
            elif a < b:
                self.flag = 0b00000100

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

    def ram_read(self, adress):
        return self.ram[adress]

    def ram_write(self, adress, value):
        self.ram[adress] = value

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            cmd = self.ram[self.pc]
            op_size = 0

            if cmd == self.HLT:
                self.running = False
                op_size = 1

            elif cmd == self.LDI:
                reg_index = self.ram[self.pc+1]
                value = self.ram[self.pc+2]

                self.reg[reg_index] = value

                op_size = 3

            elif cmd == self.PRN:
                reg_index = self.ram[self.pc+1]
                value = self.reg[reg_index]
                print(value)

                op_size = 2

            elif cmd in self.ALU:
                reg_index_a = self.ram[self.pc+1]
                reg_index_b = self.ram[self.pc+2]
                self.alu(cmd, reg_index_a, reg_index_b)

                op_size = 3

            elif cmd == self.PUSH:
                reg_index = self.ram[self.pc + 1]
                val = self.reg[reg_index]

                self.reg[self.sp] -= 1

                self.ram[self.reg[self.sp]] = val

                op_size = 2

            elif cmd == self.POP:
                reg_index = self.ram[self.pc + 1]
                val = self.ram[self.reg[self.sp]]

                self.reg[reg_index] = val

                self.reg[self.sp] += 1

                op_size = 2

            elif cmd == self.CALL:
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2

                index = self.ram[self.pc + 1]
                self.pc = self.reg[index]

                op_size = 0

            elif cmd == self.RET:
                self.pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1

                op_size = 0

            elif cmd == self.JEQ:
                if self.flag == 0b00000001:
                    reg_index = self.ram[self.pc+1]
                    self.pc = self.reg[reg_index]
                else:
                    op_size = 2

            elif cmd == self.JNE:
                if self.flag != 0b00000001:
                    reg_index = self.ram[self.pc+1]
                    self.pc = self.reg[reg_index]
                else:
                    op_size = 2

            self.pc += op_size
