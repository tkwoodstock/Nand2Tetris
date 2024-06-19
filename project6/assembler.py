from assembler_functions.to_binary import to_binary
from assembler_functions.cleanline import clean_line
from assembler_functions.a_instruction import translate_a_instruction
from assembler_functions.c_instruction import translate_c_instruction


## note in this script the label variables described in nand2tetris lectures
## are referred to as jump variables


def assembler(in_file, out_file):

    jump_variables = [] # list that stores all variables that have a jump referenced (e.g., appears in code as "(ABC)")
    jump_variables_locations = [] # list that stores the line number of the jump variable
    translated = [] # array that stores each line translated to machine code (binary), each element is written as a line to outfile
    blank_lines = 0 # need to store number of blank lines to correctly remember location of jump references

    # list that stores all assigned variables: all stored in upper case
    # predefined registers 0-15, and others such as SCREEN, KBD, and SP, are all stored in this list by default
    variables = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15", "SCREEN", "KBD", "SP", "LCL", "ARG", "THIS", "THAT"] 
    # list that stores the addresses of each allocated variable
    variables_addresses = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16384,24576,0,1,2,3,4]
    # address of first free register R16, allocate to variable and then increment by one to allocate to next variable
    next_free_register = 16 


    ## first pass: read each line, store list of jump variables (any variable enclosed in brackets)
    # jump condition, if referenced elsewhere will be written in machine language as the line number of the reference
    # e.g., "@LOOP" will jump to the line after (LOOP)
    with open(in_file) as f:
        counter = 1 # count lines to remember location of jump variable locations
        for line in f.readlines():

            line = clean_line(line)

            jump_variable = ""
            enclosed_in_second_bracket = False # jump variable should have brackets on both sides: "(" and ")"
            blank_line = False

            if len(line) == 0:
                blank_lines += 1
                counter += 1
                blank_line = True

            if not blank_line:


                if line[0] == "(":
                    for char in line[1:]:
                        if char == ")":
                            enclosed_in_second_bracket = True
                            break
                        jump_variable += char

                if enclosed_in_second_bracket: # if syntax is correct, add to list of jump variables
                    jump_variables.append(jump_variable)
                    jump_variables_locations.append(counter - len(jump_variables_locations) - blank_lines - 1) 
                    # jump vars not written into machine language so len(jump_vars) as of current iteration 
                    # must be subtracted each time to get accurate line number

                counter += 1


    #print(jump_variables)
    #print(jump_variables_locations)


    ## second pass - translate instructions into machine code:
    with open(in_file) as f:
        for line in f.readlines():

            ## clean read line
            line = clean_line(line)

            blank_line = False
            if len(line) == 0:
                blank_line = True

            # view result of cleaning line
            #print(line)

            if not blank_line:
                    

                ## if A instruction
                if line[0] == "@":

                    # if number address (variables not allowed to start with a number)
                    if ord(line[1]) <= 57 and ord(line[1]) >= 48:
                        translated.append(translate_a_instruction(line))
                    
                    # if variable (starts with a letter):
                    elif ord(line[1].upper()) >= 65 and ord(line[1].upper()) <= 90:
                        
                        # if the variable name appears in jump variables list, append the corresponding line number in binary to the translation
                        jmp_allocated = False
                        counter = 0     
                        for jump_var in jump_variables:
                            if jump_var == line[1:]:
                                translated.append(to_binary(jump_variables_locations[counter], to_16 = True))
                                jmp_allocated = True
                                break
                            counter += 1
                        
                        # if the variable name was not in jmp var list, assign it to the next free address 
                        # and increment next free address for subsequent variable
                        if not jmp_allocated and line[1:].upper() not in variables:
                            translated.append(to_binary(next_free_register, to_16 = True))
                            variables.append(line[1:].upper())
                            variables_addresses.append(next_free_register)
                            next_free_register += 1
                        elif not jmp_allocated and line[1:].upper() in variables:
                            # if not a jmp variable but IS found in variables list
                            # the translated line should be the address assigned to the variable
                            counter = 0
                            for var in variables:
                                if line[1:].upper() == var:
                                    translated.append(to_binary(variables_addresses[counter], to_16 = True))
                                counter += 1

            
            
                ## if reference point for jumping: (VAR_NAME)
                elif line[0] == "(": # or (line[0] == "/" and line[1] == "/"):
                    pass # ignore jump references and comment lines, these arent translated


                ## if C instruction (translation will start with a 1)
                else:
                    translated.append(translate_c_instruction(line))



    ## write translated code to an output file
    with open(out_file, "w") as f:
        for i in translated:
            f.write(i)
            f.write("\n")


if __name__ == "__main__":
    assembler(in_file = "in_out_docs/sample_assembly.txt", out_file = "in_out_docs/translated_to_machine_code.txt")
