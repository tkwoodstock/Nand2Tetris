# built upon VMTranslator in part2 week1
# used to complete project 8

import sys
import os


def get_vm_files(input_file):
    '''
    Creates and returns list of all files  with ".vm" extension
    List contains multiples elements if input is a directory
    List contains only 1 element if the input is a file instead of a directory
    '''
    # functionality must allow for either one or multiple files output into a single file
    vm_files = [] # empty directory to store all input files (or single file)
    # clean input so all directories represented by "/" not "\"
    input_file = input_file.replace("\\", "/")
    # check if input has trailing slash (for directories)
    trailing_slash = input_file[-1] == "/" 


    # input argument is a directory
    if os.path.isdir(input_file):
        # save ".vm" file names
        for file in os.listdir(input_file):
            # create list of input files to iterate over and read one by one, put translation in target file
            if ".vm" in str(file): 
                if not trailing_slash:
                    vm_files.append(input_file + "/" + file)
                else:
                    vm_files.append(input_file + file)
    # input argument is a file
    elif os.path.isfile(input_file):
        # append single ".vm" file
        vm_files.append(input_file) 

    return vm_files



def get_output_file(input_file):
    '''
    Creates a name for a output file to write a translation based on the input path
    If directory, the new files will have a path inside the given directory
    If file, the new file will be inside the same directory as the given file
    '''
    # clean input so all directories represented by "/" not "\"
    input_file = input_file.replace("\\", "/")
    # check if input has trailing slash (for directories)
    trailing_slash = input_file[-1] == "/" 

    # input argument is a directory
    if os.path.isdir(input_file):
        # create target file name
        dir_input_split = input_file.split("/")
        if not trailing_slash: 
            output_file = input_file + "/" + dir_input_split[-1]  + ".asm" 
        else:
            output_file = input_file + dir_input_split[-2] + ".asm"

    # input argument is a file
    elif os.path.isfile(input_file):
        # create target file (same name as input file but with ".asm" instead of ".vm")
        if "/" in input_file:
            parts = input_file.split("/")[0:-1]
            end = parts[-1] + ".asm"
            output_file = "/".join(parts) + "/" + end
        else:
            output_file = input_file.split(".")[0] + ".asm" 

    return output_file




def clean_line(line):
    '''
    Cleans each line to facilitate parsing
    Returns a list of strings for each word in a command, e.g., "push constant 4" becomes ["push", "constant", "4"]
    '''


    # remove whitespace and newline charcter
    line = line.strip() 

    # commented lines are to be ignored
    if line and line[0] == '/' and line[1] == '/':
        return False 
    
    # stop reading after // , the remaining chars are comments
    clean1_line = ""
    for char in line:
        if char == "/" and prev_char == "/":
            line = clean1_line[0:-1].strip() # take all chars up to first / in //
            break
        clean1_line += char
        prev_char = char

    # split command into a list
    parsed_line = line.split()


    return parsed_line




def translate_arithmetic(command, output_file, line_number):
    '''
    Translates arithmetic vm command into Hack assembly code
    '''
    
    assembly_translation = [] # list to append lines after translation of given command, this lines are written to the target file

    assembly_translation.append("//" + command) # append original vm command as a comment


    with open (output_file, "a") as tf: # append lines translated into assembly into final translation

        # add
        if command.lower() == "add":
            assembly_translation.append("@SP") # stack pointer
            assembly_translation.append("M=M-1") # SP-- to point to address of last added number n1
            assembly_translation.append("A=M") # target address of n1 
            assembly_translation.append("D=M") # store number D = n1
            assembly_translation.append("@SP")
            assembly_translation.append("M=M-1") # move back to next number n2
            assembly_translation.append("A=M") # target address of n2 = SP
            assembly_translation.append("M=M+D") # n1 (D) + n2 (M). and store in M
        
        # sub
        elif command.lower() == "sub":
            assembly_translation.append("@SP") # stack pointer
            assembly_translation.append("M=M-1") # SP-- to point to address of last added number n1
            assembly_translation.append("A=M") # target address of n1 
            assembly_translation.append("D=M") # store number D = n1
            assembly_translation.append("@SP")
            assembly_translation.append("M=M-1") # move back to next number n2
            assembly_translation.append("A=M") # target address of n2 = SP
            assembly_translation.append("M=M-D") # n2 (M) - n1 (D) and store in M

        # eq, ly, gt
        elif command.lower() in ["eq", "lt", "gt"]: 
            # same first lines for comparator operations
            assembly_translation.append("@SP") # stack pointer
            assembly_translation.append("M=M-1") # SP--
            assembly_translation.append("A=M") # target address of first number 
            assembly_translation.append("D=M") # D = first number n1
            assembly_translation.append("@SP")
            assembly_translation.append("M=M-1") # SP-- 
            assembly_translation.append("A=M") # target address of second number (M now = n2)
            assembly_translation.append("D=M-D") # compare n1 and n2

            # final lines different depending on specific comparator operation
            # jump to different code locations depending on true or false result

            assembly_translation.append(f"@true_case{line_number}") 

            if command.lower() == "eq": 
                assembly_translation.append("D;JEQ") # n2 - n1 (eq true then this is 0)
            elif command.lower() == "lt": # case: n2 < n1 ?
                assembly_translation.append("D;JLT") # n2 - n1 (if this is <0 then n2 < n1)
            elif command.lower() == "gt": # case: n2 > n1?
                assembly_translation.append("D;JGT") # n2 - n1 (if >0 then n2 > n1)

            # false case (no jump)
            assembly_translation.append("D=0") 
            assembly_translation.append("@SP")
            assembly_translation.append("A=M") 
            assembly_translation.append("M=D") # set *SP to 0 (false, numbers not equal)
            assembly_translation.append(f"@false_case{line_number}") 
            assembly_translation.append("0;JMP") # jump to skip writing true case logic

            # true case (jumped here from above, false skipped)
            assembly_translation.append(f"(true_case{line_number})") # will jump here if numbers are equal
            assembly_translation.append("D=-1")
            assembly_translation.append("@SP")
            assembly_translation.append("A=M")
            assembly_translation.append("M=D") # -1 in binary is all 1's which means true 
            assembly_translation.append(f"(false_case{line_number})") # -1 in binary is all 1's which means true 

        # and, or
        elif command.lower() in ["and", "or"]: 
            # same first lines for comparator operations
            assembly_translation.append("@SP") # stack pointer
            assembly_translation.append("M=M-1") # SP--
            assembly_translation.append("A=M") # target address of first number 
            assembly_translation.append("D=M") # D = first number n1
            assembly_translation.append("@SP")
            assembly_translation.append("M=M-1") # SP-- 
            assembly_translation.append("A=M") # target address of second number (M now = n2)

            if command.lower() == "and":
                assembly_translation.append("M=D&M")

            elif command.lower() == "or":
                assembly_translation.append("M=D|M")
            
        # neg, not
        elif command.lower() in ["neg", "not"]:
            assembly_translation.append("@SP")
            assembly_translation.append("M=M-1")
            assembly_translation.append("A=M")
            if command.lower() == "neg":
                assembly_translation.append("M=-M")
            elif command.lower() == "not":
                assembly_translation.append("M=!M")


        # all arithmetic operations must end by moving stack pointer +1 (SP++)
        assembly_translation.append("@SP")
        assembly_translation.append("M=M+1") # move stack pointer to next spot


        # write full arithmetic translation of vm line to target file
        for line in assembly_translation: # will be multiple output file lines for each input file line
            tf.write(line+"\n")


    # exit function when translation has been written 
    return 0




def translate_push_pop(p, seg, i, output_file, line_number, input_file=""):
    '''
    Translates push or pop vm command into Hack assembly code, and writes result into target file
    Args:
        p = push or pop
        seg = segment (local, argument, constant etc)
        i = index (e.g., pop local 4)
        output_file = file translation is written to
        line_number = line number of vm code, to show developer where errors lie when exceptions raised 
    '''

    assembly_translation = [] # list to append lines after translation of given command, this lines are written to the target file

    assembly_translation.append("//" + p + ' ' + seg + ' ' + i) # append original vm command as a comment

    # map given segment command to assembly symbol
    segments = ["argument", "local", "this", "that", "temp", "pointer", "constant", "static"]
    assembly_symbol = ["ARG", "LCL", "THIS", "THAT", "5", "?", i, input_file.split('.')[0].split("/")[-1]+'.'+i]

    # assembly RAM variable/location for command given in vm code
    assembly_seg = [assembly_symbol[i] for i, segment in enumerate(segments) if segment == seg.lower()][0]
    

    # append lines translated into assembly into final translation
    with open (output_file, "a") as tf: 

        # 6 command possibilities with grouped implementation
        if seg.lower() in ["argument", "local", "this", "that", "temp"]:
            if p.lower() == "pop":
                assembly_translation.append(f"@{i}") # address within segment (i)
                assembly_translation.append(f"D=A")
                assembly_translation.append(f"@R13") # target address variable
                assembly_translation.append("M=D") # 
                assembly_translation.append(f"@{assembly_seg}") # address of segment base (e.g, LCL)
                if seg.lower() == "temp":
                    assembly_translation.append("D=A") 
                else:
                    assembly_translation.append("D=M") 
                assembly_translation.append(f"@R13")
                assembly_translation.append("M=D+M") # addr = i + segment base (address of target RAM)
                assembly_translation.append("@SP")
                assembly_translation.append("AM=M-1") # move stack pointer back 1 to most recent number (SP--)
                assembly_translation.append("D=M") # D = value of most recent number on stack
                assembly_translation.append(f"@R13")
                assembly_translation.append("A=M") # address of target RAM (segment address + i)
                assembly_translation.append("M=D") # place most recent stack number in target address 
                # SP now in position to replace number just copied into assembly_seg, no need to SP++

            if p.lower() == "push":
                assembly_translation.append(f"@{i}") # address within segment (i)
                assembly_translation.append("D=A")
                assembly_translation.append(f"@{assembly_seg}") # address of segment base (e.g., @ARG)
                if seg.lower() == "temp":
                    assembly_translation.append("D=D+A") 
                else:
                    assembly_translation.append("D=D+M") 
                assembly_translation.append("A=D") # A = address of target position in segment (base + i)
                assembly_translation.append("D=M") # D = value inside target address in segment
                assembly_translation.append("@SP")
                assembly_translation.append("A=M") # A = address of stack pointer
                assembly_translation.append("M=D") # push D (value) onto position stack pointer is pointing to
                assembly_translation.append("@SP") 
                assembly_translation.append("M=M+1") # increment stack pointer to next space on stack


        # static (6th command possibility)
        elif seg.lower() == "static":
            if p.lower() == "pop":
                assembly_translation.append("@SP")
                assembly_translation.append("M=M-1")
                assembly_translation.append("A=M")
                assembly_translation.append("@" + assembly_seg)
                assembly_translation.append("M=D")
            elif p.lower() == "push":
                assembly_translation.append("@" + assembly_seg)
                assembly_translation.append("D=M")
                assembly_translation.append("@SP")
                assembly_translation.append("A=M")
                assembly_translation.append("M=D")
                assembly_translation.append("@SP")
                assembly_translation.append("M=M+1")

        # constant (7th command possibility)  
        elif seg.lower() == "constant": 

            if p.lower() == "pop": # must be a push 
                raise Exception(f"cannot 'pop' a constant. Error on line {line_number}: '{p} + {seg} + {i}'")
            
            # push constant i
            assembly_translation.append(f"@{i}") # constant number
            assembly_translation.append("D=A")
            assembly_translation.append("@SP") 
            assembly_translation.append("A=M") # A = address of current position on stack
            assembly_translation.append("M=D") # push constant i onto stack
            assembly_translation.append("@SP")
            assembly_translation.append("M=M+1") # increment stack pointer to next space on stack

            

        # pointers (8th and final command possibility)
        elif seg.lower() == "pointer":

            # for pointers i must be 0 or 1
            if i not in ["0", "1"]:
                raise Exception(f"can only push/pop pointer to index 0 or 1, error on line {line_number}: '{p} + {seg} + {i}'")

            # set index to correct assembly variable when command is a pointer type
            # if i == "0":
            #     assembly_seg = "THIS"
            # elif i == "1":
            #     assembly_seg = "THAT"

            assembly_seg = "THIS"

            # translate
            if p.lower() == "push":
                assembly_translation.append(f"@{str(i)}") 
                assembly_translation.append(f"D=A") 
                assembly_translation.append(f"@{assembly_seg}") # @THIS or @THAT, depending on i
                assembly_translation.append(f"A=D+A") 
                assembly_translation.append(f"D=M") # D = target value
                assembly_translation.append(f"@SP")
                assembly_translation.append(f"A=M") # address of stack position
                assembly_translation.append(f"M=D") # push value onto stack
                assembly_translation.append(f"@SP")
                assembly_translation.append(f"M=M+1") # increment stack SP++

            elif p.lower() == "pop":
                assembly_translation.append(f"@{str(i)}") 
                assembly_translation.append(f"D=A") 
                assembly_translation.append(f"@{assembly_seg}") 
                assembly_translation.append(f"D=D+A")
                assembly_translation.append(f"@R13")
                assembly_translation.append(f"M=D")   
                assembly_translation.append(f"@SP") 
                assembly_translation.append(f"AM=M-1") # move sp to address of last placed onto stack
                assembly_translation.append(f"D=M") # D = value most recently placed onto stack
                assembly_translation.append(f"@R13") 
                assembly_translation.append(f"A=M") 
                assembly_translation.append(f"M=D") # pop stack value into *THIS or *THAT


        # write push/pop translation of vm line to target file
        for line in assembly_translation: # will be multiple output file lines for each input file line
            tf.write(line+"\n")


    return 0




def translate_branching(command, output_file, in_file_name, function_name):
    '''
    translates branching command
    args:
        command: array of length 2 containing
            command[0]: if-goto, goto or label
            command[1]: location/label name
    '''
    with open(output_file, "a") as tf:
        # write vm code command as a comment to help debug
        tf.write("//" + command[0] + " " + command[1] + "\n")

        if command[0].lower() == "label":
            if function_name:
                tf.write("(" + function_name + "$" + command[1].upper() + ")" + "\n")
            else:
                tf.write("(" + in_file_name.replace(".vm", "") + "." + command[1].upper() + ")" + "\n")
            return 0
        
        elif command[0].lower() == "goto":
            if function_name:
                tf.write("@" + function_name + "$" + command[1].upper() + "\n")
            else:
                tf.write("@" + in_file_name.replace(".vm", "") + "." + command[1].upper() + "\n")
            tf.write("0;JMP" + "\n")

        elif command[0].lower() == "if-goto":
            tf.write("@SP" + "\n")
            tf.write("M=M-1" + "\n")
            tf.write("A=M" + "\n")
            tf.write("D=M" + "\n")
            if function_name:
                tf.write("@" + function_name + "$" + command[1].upper() + "\n")
            else:
                tf.write("@" + in_file_name.replace(".vm", "") + "." + command[1].upper() + "\n")
            tf.write("D;JGT" + "\n") # D;JNE?




def translate_function_declaration(function_name, nargs , output_file):
    with open(output_file, "a") as of:
        # write vm code command as a comment to help debug
        of.write("//function " + function_name + " " + nargs + "\n")

        # write function label entry point
        of.write("(" + function_name + ")" + "\n")

        ## set up function execution
        # push 0 nvars times
        for i in range(int(nargs)):
            of.write("@0" + "\n")
            of.write("D=A" + "\n")
            of.write("@SP" + "\n")
            of.write("A=M" + "\n")
            of.write("M=D" + "\n")
            of.write("@SP" + "\n")
            of.write("M=M+1" + "\n")

        # function now executes until reaching a return





def translate_call_declaration(called_function_name, nargs, output_file, current_function_name, n_returns: str):
    with open(output_file, "a") as of:
        # write vm code command as a comment to help debug
        of.write("//call " + called_function_name + " " + nargs + "\n")

        # push return location onto stack to come back to after function is called
        return_address = current_function_name + "$" + "ret" + n_returns
        of.write("@" + return_address + "\n")
        of.write("D=A" + "\n")
        of.write("@SP" + "\n")
        of.write("A=M" + "\n")
        of.write("M=D" + "\n")
        of.write("@SP" + "\n")
        of.write("M=M+1" + "\n")


        ## TODO push LCL, ARG, THIS, THAT 
        # see unit 2.6 video for translating call statement (first half of video I think)
        # LCL
        of.write("@LCL" + "\n")
        of.write("D=M" + "\n")
        of.write("@SP" + "\n")
        of.write("A=M" + "\n")
        of.write("M=D" + "\n")
        of.write("@SP" + "\n")
        of.write("M=M+1" + "\n")
        # ARG
        of.write("@ARG" + "\n")
        of.write("D=M" + "\n")
        of.write("@SP" + "\n")
        of.write("A=M" + "\n")
        of.write("M=D" + "\n")
        of.write("@SP" + "\n")
        of.write("M=M+1" + "\n")
        # THIS
        of.write("@THIS" + "\n")
        of.write("D=M" + "\n")
        of.write("@SP" + "\n")
        of.write("A=M" + "\n")
        of.write("M=D" + "\n")
        of.write("@SP" + "\n")
        of.write("M=M+1" + "\n")
        # THAT
        of.write("@THAT" + "\n")
        of.write("D=M" + "\n")
        of.write("@SP" + "\n")
        of.write("A=M" + "\n")
        of.write("M=D" + "\n")
        of.write("@SP" + "\n")
        of.write("M=M+1" + "\n")

        # reposition ARG = SP - 5 - nargs
        of.write("@" + nargs + "\n")
        of.write("D=A" + "\n")
        of.write("@5" + "\n")
        of.write("D=D+A" + "\n")
        of.write("@SP" + "\n")
        of.write("D=M-D" + "\n")
        of.write("@ARG" + "\n")
        of.write("M=D" + "\n")

        # reposition LCL = SP
        of.write("@SP" + "\n")
        of.write("D=M" + "\n")
        of.write("@LCL" + "\n")
        of.write("M=D" + "\n")

        # write a goto called function
        of.write("@" + called_function_name + "\n")
        of.write("0;JMP" + "\n")

        # write return address
        of.write("(" + return_address + ")" + "\n")




def translate_return(output_file):
    with open(output_file, "a") as of:
        of.write("//RETURN"+"\n")

        # store LCL in temporary variable
        of.write("@LCL" + "\n")
        of.write("D=M" + "\n")
        of.write("@endFrame" + "\n")
        of.write("M=D" + "\n")

        # return address = *(endFrame - 5)
        of.write("@endFrame" + "\n")
        of.write("D=M" + "\n")
        of.write("@5" + "\n")
        of.write("D=D-A" + "\n") # D = address of target value 
        of.write("A=D" + "\n") # look at target value address
        of.write("D=M" + "\n") # store target value (held inside address)
        of.write("@retAddr" + "\n")
        of.write("M=D" + "\n") # retAddr holds return address

    # pop return value to ARG
    translate_push_pop("pop", "argument", "0", output_file, 0)

    
    with open(output_file, "a") as of:
        # SP = ARG + 1
        of.write("@ARG" + "\n")
        of.write("D=M" + "\n")
        of.write("@SP" + "\n")
        of.write("M=D+1" + "\n")

        # THAT = *(endFrame - 1) | THis = *(endFrame - 2) | ARG = *(endFrame - 3) | LCL = *(endFrame - 4)
        for seg, i in zip(["THAT", "THIS", "ARG", "LCL"], ["1", "2", "3", "4"]):
            of.write("@endFrame" + "\n")
            of.write("D=M" + "\n")
            of.write("@"+ str(i) + "\n")
            of.write("D=D-A" + "\n")
            of.write("A=D" + "\n")
            of.write("D=M" + "\n")
            of.write("@" + seg + "\n")
            of.write("M=D" + "\n")

        # goto retAddr
        of.write("@retAddr" + "\n")
        of.write("A=M" + "\n")
        # TODO problem here (jumping to arbitrary location as return address was not written: there was no call statement, so @Addr just stores 0 and the program runs again from the start)
        # up until this point, SimpleFunction works correctly (bootstrap initialisation code??) 
        of.write("0;JMP" + "\n")




def main():


    # process input arguments (arg1 should be directory or file to be translated)
    if len(sys.argv) > 1:
        
        if os.path.isdir(sys.argv[1]) or os.path.isfile(sys.argv[1]):
            # get target file name from input argument (output_file is where translation is written)
            output_file = get_output_file(sys.argv[1])
            # get list of ".vm" files from input argument
            vm_files = get_vm_files(sys.argv[1])
        else:
            raise Exception(f"invlaid input '{sys.argv[1]}' is not a valid file or directory")

        # TODO sys.argv[2]??

    else:
        raise Exception("must provide path of input file as first argument")


    # create a single blank target file on each script run (only one target file even if multiple input files) 
    f = open(output_file, "w")
    # close file (append content in smaller chunks later on) 
    f.close() 


    print("\nTARGET FILE NAME:", output_file)
    print("INPUT VM FILE LIST:", vm_files)
    print()


    ## BOOTSTRAP CODE, intialise program (if it is a directory, i.e., more than one file)
    if os.path.isdir(sys.argv[1]):
        print("DIRECTORY")
        with open(output_file, "a") as of:
            #SP = 256
            of.write("@256" + "\n")
            of.write("D=A" + "\n")
            of.write("@SP" + "\n")
            of.write("M=D" + "\n") 

        # call sys.init
        translate_call_declaration("Sys.init", "0", output_file, "Sys.init", "0")


    # now translate contents of individual files
    ## iterate over vm file list, read vm file(s) and translate accordingly into single output file
    for vm_file in vm_files:

        # get name of file being read without parent path
        vm_file_name = ""
        if "/" in vm_file:
            vm_file_name = vm_file.split("/")[-1]
        else:
            vm_file_name = vm_file
        
        with open(vm_file) as f:
            line_number = 1 # line number in each source file
            current_function_name = "" # empty until it reaches a function
            current_function_nargs = 0 # number of arguments to current function
            n_function_returns = 0 # number of times function is returned to after performing a different function

            for line in f.readlines():
                # get list of each word in the command (e.g., ["pop", "local", "2"])
                command = clean_line(line) 

                # move to next line if its a comment line or a blank line (command will be empty)
                if not command: 
                    line_number += 1
                    continue
                
                # push/pop translation 
                if command[0].lower() in ["push", "pop"] and len(command) == 3 and command[1] in ["argument", "local", "static", "constant", "this", "that", "pointer", "temp"] and command[2].isnumeric():
                    # if command syntax is correct then translate and append using function
                    # TODO write function to push and pop
                    translate_push_pop(command[0], command[1], command[2], output_file, f"{line_number}", vm_file) # now line_number argument contains both file name and line number
                
                # arithmetic translation
                elif command[0].lower() in ["add", "sub", "eq", "lt", "gt", "neg", "and", "or", "not"] and len(command) == 1:
                    # if command syntax is correct then translate and append using function
                    # TODO write function to do arithmetic
                    translate_arithmetic(command[0], output_file, f"{line_number}") # now line_number argument contains both file name and line number

                
                # TODO if label/function etc do elif here 
                elif command[0].lower() in ["label", "if-goto", "goto"] and len(command) == 2:
                    translate_branching(command, output_file, vm_file_name, current_function_name)


                # TODO other functions for different commands e.g., function, call
                elif command[0].lower() == "function" and len(command) == 3:
                    current_function_name = command[1] # store name of current function being defined
                    current_function_nargs = command[2] # store number of arguments in function
                    n_function_returns = 0 # restore number of returns back to zero for new function
                    # write function label
                    translate_function_declaration(current_function_name, current_function_nargs, output_file)

                elif command[0].lower() == "call" and len(command) == 3:
                    called_function_name = command[1]
                    called_function_nargs = command[2]
                    n_function_returns += 1
                    translate_call_declaration(called_function_name, called_function_nargs, output_file, current_function_name, str(n_function_returns))


                elif command[0].lower() == "return" and len(command) == 1:
                    translate_return(output_file)


                ## if reach this condition then command syntax is invalid and raise exception
                else:
                    raise Exception(f"Invalid command in file {vm_file_name} at line {line_number}: {' '.join(command)}")
                
                
                line_number += 1 # move to next input file vm line and keep track of number




if __name__ == '__main__':
    main()