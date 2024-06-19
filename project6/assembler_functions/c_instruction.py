
def translate_c_instruction(line):
    #print(line)
    # format 111 a c1c2c3c4c5c6 d1d2d3 j1j2j3
    opcode = "111" # first 3 characters are always 1 in c instruction
    a = "0" # set to 1 if "M" is in the calculation, completed in the calccode (c1-c6) section
    calccode = "0" # set calccode for no matches, will raise exception as is not 6 characters long
    dest_condition = False # dest condition determines 3 binary numbers
    jump_condition = False # jmp condition determines the final 3 binary numbers
    eq_index = -1 # position of the equals sign, calculation starts here (position 0 if no equals sign)
    col_index = len(line) # position of the semicolon, calculation ends here (position max if no semi colon)


    # scan line to set dest condition and jump condition
    counter = 0
    for char in line:
        if char == "=":
            dest_condition = True
            eq_index = counter
        elif char == ";":
            jump_condition = True
            col_index = counter
        counter += 1
    

    ## apply logic to fill  dest code
    # set dest code to 0 if not present in C instruction
    d1 = "0"
    d2 = "0"
    d3 = "0"
    # fill dest code with appropriate numbers if present in C instruction
    if dest_condition:
        for char in line[0:eq_index]:
            if char == "A":
                d1 = "1"
            elif char == "D":
                d2 = "1"
            elif char == "M":
                d3 = "1"

    destcode = d1+d2+d3


    ## apply logic to fill jmp code
    # set jump code to 0 if not present in C instruction
    j1 = "0"
    j2 = "0"
    j3 = "0"
    # fill jump code with appropriate numbers if present in C instruction
    if jump_condition:
        j = ""
        for char in line[col_index+1:]:
            j += char


        if j == "JLT" or j == "JNE" or j == "JLE" or j == "JMP":
            j1 = "1"
        if j == "JEQ" or j == "JGE" or j == "JLE" or j == "JMP":
            j2 = "1"
        if j == "JGT" or j == "JGE" or j == "JNE" or j == "JMP":
            j3 = "1"
    
    jmpcode = j1+j2+j3


    ## apply logic to fill the calc code
    # 6 characters depending on a (see above)
    # get equation part of string
    eq = ""
    for char in line[eq_index+1:col_index]:
        eq += char
        if char == "M":
            a = "1" # set a to 1 if any of the expression is "M", regardless of whether there is "=" or ";"

    # write out equation-binary table for calculation (binary array holds c1-c6 that matches the equation)
    # a = 1 side (M IS in the expression)
    a1_equations = ["M", "!M", "-M", "M+1", "M-1", "D+M", "M+D", "D-M", "M-D", "D&M", "M&D", "D|M", "M|D"]
    a1_binary = ["110000", "110001", "110011", "110111", "110010", "000010", "000010", "010011", "000111", "000000", "000000", "010101", "010101"]
    # a = 0 side (M is NOT in the expression)
    a0_equations = ["0", "1", "-1", "D", "A", "!D", "!A", "-D", "-A", "D+1", "A+1", "D-1", "A-1", "D+A", "A+D", "D-A", "A-D", "D&A", "A&D", "D|A", "A|D"]
    a0_binary = ["101010", "111111", "111010", "001100", "110000", "001101", "110001", "001111", "110011", "011111", "110111", "001110", "110010", "000010", "000010", "010011", "000111", "000000", "000000", "010101", "010101"]
    
    # match equation to 6 binary numbers depending on a ("a" retrieved above)
    counter = 0
    if a == "1":
        for expr in a1_equations:
            if eq == expr:
                calccode = a1_binary[counter]
            counter += 1
    if a == "0":
        for expr in a0_equations:
            if eq == expr:
                calccode = a0_binary[counter]
            counter += 1


    if len(calccode) != 6:
        raise Exception(f"Invalid expression input, please review syntax (e.g. D+1), error found with input: {line}")

    ## append translated c instruction
    return opcode+a+calccode+destcode+jmpcode