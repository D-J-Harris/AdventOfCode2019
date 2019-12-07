#!/usr/bin/env python
# coding: utf-8



# dict for finding how many parameters in instruction
instruction_length_dict = {
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
def process_instruction(instruct_value):

    if instruct_value == 99:
        return instruct_value, [0]
    
    op_length = len(str(instruct_value))
    
    # assume all params in position mode in this case
    if op_length == 1:
        length = instruction_length_dict[instruct_value]
        
        modes = [0 for _ in range(length)]
        opcode = instruct_value
    
    else:
        opcode = instruct_value % 100
        length = instruction_length_dict[opcode]
        
        instruct_value = [int(x) for x in str(instruct_value)]
        modes = [instruct_value[-i-3] if i < len(instruct_value)-2 else 0 for i in range(length)]
    return opcode, modes




def get_param(data, instruction, modes, idx):
    
    if modes[idx] == 0:
        return data[instruction[idx]]
    else:
        return instruction[idx]



# computer, returns output as first arg, and either data or True for second arg
# data if the computer is outputting, True if the computer is halting
def computer(data, inputs, pointer):
 
    input_pointer = 0
    computer_output = 0
    
    # loop until halt with opcode 99
    while True:

        opcode_instruction = data[pointer]

        opcode, modes = process_instruction(opcode_instruction)

        instruction = data[pointer + 1 : pointer + len(modes) + 1]

        if opcode == 99:
            print(f"Opcode 99, halt for inputs {inputs}")
            return computer_output, data, True, pointer
        elif opcode == 1:
    
            param_1 = get_param(data, instruction, modes, 0)
            param_2 = get_param(data, instruction, modes, 1)
            output_idx = instruction[2]
            
            addition = param_1 + param_2
            data[output_idx] = addition
            pointer += len(modes) + 1 
            
        elif opcode == 2:
            
            param_1 = get_param(data, instruction, modes, 0)
            param_2 = get_param(data, instruction, modes, 1)
            output_idx = instruction[2]
            
            multiply = param_1 * param_2
            data[output_idx] = multiply
            pointer += len(modes) + 1 
            
        elif opcode == 3:
            
            input_idx = instruction[0]
            data[input_idx] = inputs[input_pointer]
            input_pointer += 1
            pointer += len(modes) + 1 
            
        elif opcode == 4:
            
            output = get_param(data, instruction, modes, 0)
            print(f"Opcode 4 output: {output}, for inputs {inputs}")
            pointer += len(modes) + 1 
            computer_output = output
            return computer_output, data, False, pointer
            
        elif opcode == 5:
            
            param_1 = get_param(data, instruction, modes, 0)
            param_2 = get_param(data, instruction, modes, 1)
            if param_1 != 0:
                pointer = param_2
            else:
                pointer += len(modes) + 1 
        
        elif opcode == 6:
            
            param_1 = get_param(data, instruction, modes, 0)
            param_2 = get_param(data, instruction, modes, 1)
            if param_1 == 0:
                pointer = param_2
            else:
                pointer += len(modes) + 1
                
        elif opcode == 7:
            
            param_1 = get_param(data, instruction, modes, 0)
            param_2 = get_param(data, instruction, modes, 1)
            param_3 = instruction[2]
            if param_1 < param_2:
                data[param_3] = 1
            else:
                data[param_3] = 0
            pointer += len(modes) + 1
                
        elif opcode == 8:
            
            param_1 = get_param(data, instruction, modes, 0)
            param_2 = get_param(data, instruction, modes, 1)
            param_3 = instruction[2]
            if param_1 == param_2:
                data[param_3] = 1
            else:
                data[param_3] = 0
            pointer += len(modes) + 1
  
        else:
            print("Opcode Error")     
