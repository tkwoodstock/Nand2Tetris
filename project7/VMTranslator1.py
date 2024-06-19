# used to complete project 7 (week1 of nand2tetris part 2)

import sys


def clean_line(line):
    '''
    Cleans each line to facilitate parsing
    '''

    line = line.strip() # remove whitespace and newline charcter

    if line and line[0] == '/' and line[1] == '/':
        return False # commented lines are to be ignored

    parsed_line = line.split()

    return parsed_line



def translate_arithmetic(command, target_file, counter):
    '''
    Translates arithmetic vm command into Hack assembly code
    '''
    
    assembly_translation = [] # list to append lines after translation of given command, this lines are written to the target file

    assembly_translation.append("//" + command) # append original vm command as a comment


    with open (target_file, "a") as tf: # append lines translated into assembly into final translation

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

            assembly_translation.append(f"@true_case{counter}") 

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
            assembly_translation.append(f"@false_case{counter}") 
            assembly_translation.append("0;JMP") # jump to skip writing true case logic

            # true case (jumped here from above, false skipped)
            assembly_translation.append(f"(true_case{counter})") # will jump here if numbers are equal
            assembly_translation.append("D=-1")
            assembly_translation.append("@SP")
            assembly_translation.append("A=M")
            assembly_translation.append("M=D") # -1 in binary is all 1's which means true 
            assembly_translation.append(f"(false_case{counter})") # -1 in binary is all 1's which means true 

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




def main():

    # # manual input and output file declaration:
    # input_file = r"7\MemoryAccess\BasicTest\BasicTest.vm"
    # target_file = "BasicTest.asm"

    # cli functionality for input and output files
    # command skeleton for current directory structure: 
    if len(sys.argv) > 1:
        
        input_file = sys.argv[1]
        target_file = sys.argv[1].split(".")[0] + ".asm"
        #sys.argv[2]??
    else:
        raise Exception("must provide path of input file as first argument")


    f = open(target_file, "w") # create a blank target file on each run 
    f.close() # close file (append content in smaller chunks later on)


    ## read vm file
    with open(input_file) as f:
        counter = 1 # keeps reference to each line in source file

        for line in f.readlines():
            translated = [] # translated command into multiple assembly lines

            command = clean_line(line) # see function above

            if not command: # move to next line if its a commend line or a blank line
                counter += 1
                continue
            
            # push/pop translation 
            if command[0].lower() in ["push", "pop"] and len(command) == 3 and command[1] in ["argument", "local", "static", "constant", "this", "that", "pointer", "temp"] and command[2].isnumeric():
                # if command syntax is correct then translate and append using function
                # TODO write function to push and pop
                translate_push_pop(command[0], command[1], command[2], target_file, counter, input_file)
                

            # arithmetic translation
            elif command[0].lower() in ["add", "sub", "eq", "lt", "gt", "neg", "and", "or", "not"] and len(command) == 1:
                # if command syntax is correct then translate and append using function
                # TODO write function to do arithmetic
                translate_arithmetic(command[0], target_file, counter)

            # if reach this condition then command syntax is invalid and raise exception
            else:
                raise Exception(f"Invalid command at line {counter}: {' '.join(command)}")
            
            
            counter += 1 # move to next input file vm line and keep track of number




if __name__ == '__main__':
    main()