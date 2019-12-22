#!/usr/bin/env python
# coding: utf-8

from itertools import repeat
import numpy as np


class Computer:
    
    def __init__(self, data, inputs=[], verbose=False, input_func=None):
    
        self.data = data
        self.inputs = inputs
        self.input_func = input_func
        self.pointer = 0
        self.rel_base = 0
        self.verbose = verbose
        self.halted = False
        self.output = 0
        
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
            8: 3,
            9: 1
        }

        
    def increase_memory(self, amount):
        for _ in range(amount):
            self.data.append(0)
        

    # returns opcode of instruction, and modes of the following parameters
    def process_instruction(self, instruct_value):

        if instruct_value == 99:
            return instruct_value, [0]

        opcode = instruct_value % 100
        length = self.instruction_length_dict[opcode]

        # modes is an array of the mode for each following parameter
        modes = np.array([int(x) for x in str(instruct_value)[:-2:][::-1]])
        extra_modes = length - len(modes)
        modes = np.pad(modes, (0, extra_modes), 'constant')
        
        return opcode, modes
    
    
    # get the parameter according to mode
    def param(self, pos, modes):

        if modes[pos-1] == 0:
            return self.data[self.data[self.pointer + pos]]
        
        elif modes[pos-1] == 1:
            return self.data[self.pointer + pos]
        
        elif modes[pos-1] == 2:
            return self.data[self.data[self.pointer + pos] + self.rel_base]
        
    # get the index of inputs/outputs according to mode
    def index(self, pos, modes):
        if modes[pos-1] == 0:
            return self.data[self.pointer + pos]
        
        elif modes[pos-1] == 1:
            return self.pointer + pos
        
        elif modes[pos-1] == 2:
            return self.data[self.pointer + pos] + self.rel_base


    # computer, returns output as first arg, and either data or True for second arg
    # data if the computer is outputting, True if the computer is halting
    def run_computer(self, inputs=None):
        
        if inputs is not None:
            self.inputs += inputs
            
        # increase memory by an arbitrary amount
        self.increase_memory(3000)
                      
        # loop until halt with opcode 99
        while not self.halted:

            # get the instruction (following opcode) and its respective modes
            opcode_instruction = self.data[self.pointer]
            opcode, modes = self.process_instruction(opcode_instruction)


            if opcode == 99:
                
                self.halted = True
                if self.verbose:
                    print("Opcode 99, halt")
                return self.output
               
            elif opcode == 1:

                output_idx = self.index(3, modes)
                self.data[output_idx] = self.param(1, modes) + self.param(2, modes)
                self.pointer += 4

            elif opcode == 2:

                output_idx = self.index(3, modes)
                self.data[output_idx] = self.param(1, modes) * self.param(2, modes)
                self.pointer += 4

            elif opcode == 3:

                input_idx = self.index(1, modes)
                self.data[input_idx] = self.inputs.pop(0) if self.inputs else self.input_func()
                self.pointer += 2

            elif opcode == 4:
                
                output_idx = self.index(1, modes)
                self.output = self.data[output_idx]
                self.pointer += 2
                
                if self.verbose:
                    print(f"Opcode 4 output: {self.output}")
                return self.output
                
            elif opcode == 5:

                if self.param(1, modes):
                    self.pointer = self.param(2, modes)
                else:
                    self.pointer += 3 
                    
            elif opcode == 6:
                
                if self.param(1, modes):
                    self.pointer += 3
                else:
                    self.pointer = self.param(2, modes)
                    
            elif opcode == 7:
                
                store_idx = self.index(3, modes)
                if self.param(1, modes) < self.param(2, modes):
                    self.data[store_idx] = 1
                else:
                    self.data[store_idx] = 0
                self.pointer += 4
                    
            elif opcode == 8:

                store_idx = self.index(3, modes)
                if self.param(1, modes) == self.param(2, modes):
                    self.data[store_idx] = 1
                else:
                    self.data[store_idx] = 0
                self.pointer += 4
                
            elif opcode == 9:
                
                self.rel_base += self.param(1, modes)
                self.pointer += 2

            else:
                print("Opcode Error")     
