#!/usr/bin/env python
# coding: utf-8


class Computer:
    
    def __init__(self, data, inputs):
    
        self.data = data
        self.inputs = [inputs]
        self.pointer = 0
        

        # dict for finding how many parameters in instruction
        self.instruction_length_dict = {
            99: 1,
            1: 3,
            2: 3,
            3: 1,
            4: 1,
            5: 2,
            6: 2,
            7: 3,
            8: 3
        }


    # returns opcode of instruction, and modes of the parameters
    def process_instruction(self, instruct_value):

        if instruct_value == 99:
            return instruct_value, [0]

        op_length = len(str(instruct_value))

        # assume all params in position mode in this case
        if op_length == 1:
            length = self.instruction_length_dict[instruct_value]

            modes = [0 for _ in range(length)]
            opcode = instruct_value

        else:
            opcode = instruct_value % 100
            length = self.instruction_length_dict[opcode]

            instruct_value = [int(x) for x in str(instruct_value)]
            modes = [instruct_value[-i-3] if i < len(instruct_value)-2 else 0 for i in range(length)]
        return opcode, modes




    def get_param(self, instruction, modes, idx):
    
        if modes[idx] == 0:
            return self.data[instruction[idx]]
        else:
            return instruction[idx]



    # computer, returns output as first arg, and either data or True for second arg
    # data if the computer is outputting, True if the computer is halting
    def run_computer(self, inputs):
        
        self.inputs += inputs
        computer_output = 0

        # loop until halt with opcode 99
        while True:

            opcode_instruction = self.data[self.pointer]

            opcode, modes = self.process_instruction(opcode_instruction)

            instruction = self.data[self.pointer + 1 : self.pointer + len(modes) + 1]

            if opcode == 99:
                print(f"Opcode 99, halt for inputs {inputs}")
                return computer_output, True
            elif opcode == 1:

                param_1 = self.get_param(instruction, modes, 0)
                param_2 = self.get_param(instruction, modes, 1)
                output_idx = instruction[2]
                addition = param_1 + param_2
                self.data[output_idx] = addition
                self.pointer += len(modes) + 1 

            elif opcode == 2:

                param_1 = self.get_param(instruction, modes, 0)
                param_2 = self.get_param(instruction, modes, 1)
                output_idx = instruction[2]

                multiply = param_1 * param_2
                self.data[output_idx] = multiply
                self.pointer += len(modes) + 1 

            elif opcode == 3:

                input_idx = instruction[0]
                self.data[input_idx] = self.inputs.pop(0)
                self.pointer += len(modes) + 1 

            elif opcode == 4:

                output = self.get_param(instruction, modes, 0)
                print(f"Opcode 4 output: {output}, for inputs {self.inputs}")
                self.pointer += len(modes) + 1 
                computer_output = output
                return computer_output, False

            elif opcode == 5:

                param_1 = self.get_param(instruction, modes, 0)
                param_2 = self.get_param(instruction, modes, 1)
                if param_1 != 0:
                    self.pointer = param_2
                else:
                    self.pointer += len(modes) + 1 

            elif opcode == 6:

                param_1 = self.get_param(instruction, modes, 0)
                param_2 = self.get_param(instruction, modes, 1)
                if param_1 == 0:
                    self.pointer = param_2
                else:
                    self.pointer += len(modes) + 1

            elif opcode == 7:

                param_1 = self.get_param(instruction, modes, 0)
                param_2 = self.get_param(instruction, modes, 1)
                param_3 = instruction[2]
                if param_1 < param_2:
                    self.data[param_3] = 1
                else:
                    self.data[param_3] = 0
                self.pointer += len(modes) + 1

            elif opcode == 8:

                param_1 = self.get_param(instruction, modes, 0)
                param_2 = self.get_param(instruction, modes, 1)
                param_3 = instruction[2]
                if param_1 == param_2:
                    self.data[param_3] = 1
                else:
                    self.data[param_3] = 0
                self.pointer += len(modes) + 1

            else:
                print("Opcode Error")     
