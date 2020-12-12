"""CPU functionality."""

import sys

class methods:
    LDI = 0b10000010
    PRN = 0b1000111
    HLT = 0b1
    MUL = 0b10100010
    POP = 0b01000110
    RET = 0b00010001
    PUSH = 0b01000101
    CALL = 0b01010000
    ADD = 0b10100000
    CMP = 0b10100111
    JMP = 0b01010100
    JEQ = 0b01010101
    JNE = 0b01010110
    
class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.flag = 0b00000000
    
    def ram_read(self,address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        address = 0
        try:
            with open(f'{filename}.ls8') as f:
                for line in f:
                    line = line.strip()
                    if line == '' or line[0] == "#":
                        continue
                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, 2)
                    except ValueError:
                        sys.exit(0)
                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            sys.exit(0)
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        sp = 7
        while self.running:
            command = self.ram_read(self.pc)
            op_1 = self.ram_read(self.pc + 1)
            op_2 = self.ram_read(self.pc + 2)
            if command == methods.LDI:
                self.reg[op_1] = op_2
                self.pc += 3
            elif command == methods.PRN:
                print(self.reg[op_1])
                self.pc += 2
            elif command == methods.ADD:
                self.reg[op_1] += self.reg[op_2]
                self.pc += 3
            elif command == methods.MUL:
                self.reg[op_1] = op_1 * op_2
                self.pc += 3
            elif command == methods.HLT:
                self.running = False
                self.pc = 0
            elif command == methods.PUSH:
                sp -= 1
                self.ram_write(self.reg[op_1], sp)
                self.pc += 2
            elif command == methods.POP:
                self.reg[op_1] = self.ram[sp]
                sp += 1
                self.pc += 2
            elif command == methods.CALL:
                address = self.pc + 2
                sp -= 1
                self.ram_write(address, sp)
                self.pc = self.reg[op_1]
            elif command == methods.RET:
                self.pc = self.ram[sp]
                sp += 1
            elif command == methods.CMP:
                a = self.reg[op_1]
                b = self.reg[op_2]
                #Compares two registers and sets the value depending on the outcome
                if a == b:
                    self.flag = 0b00000001
                elif a < b:
                    self.flag = 0b00000100
                elif a > b:
                    self.flag = 0b00000010
                self.pc += 3
            elif command == methods.JMP:
                #Set the `PC` to the address stored in the given register.
                self.pc = self.reg[op_1]
            elif command == methods.JEQ:
                #If `equal` flag is set (true), jump to the address stored in the given register.
                if self.flag == 0b00000001:
                    self.pc = self.reg[op_1]
                else:
                    self.pc += 2
            elif command == methods.JNE:
                #If `E` flag is clear (false, 0), jump to the address stored in the given
                #register.
                if self.flag != 0b00000001:
                    self.pc = self.reg[op_1]
                else:
                    self.pc += 2
            else:
                print(command)


