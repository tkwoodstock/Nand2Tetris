import sys
import os



## Classes ##
class JackAnalyser():

    def __init__(self, files_in: list, files_out: list):
        self.files_in = files_in
        self.files_out = files_out
        self.keywords = ["class", "constructor", "function", "method", \
                         "field", "static", "var", "int", "char", "boolean", \
                         "void", "true", "false", "null", "this", "let", "do" \
                         "if", "else", "while", "return"]
        self.symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", \
                        "*", "/", "&", "|", "<", ">", "=", "~"]

        print("input files:", self.files_in)
        print("output files:", self.files_out)
        print()

    
    def create_blank_output_files(self):
        # create blank empty files for each jack input file
        for jack_file, xml_file in zip(self.files_in, self.files_out):
            f = open(xml_file, "w")


    def translate_files(self):
        # read each file provided and write to corresponding output file
        for in_file, out_file in zip(self.files_in, self.files_out):
            # debugging
            # see current file
            print(f"CURRENT FILE BEING READ: {in_file}")

            # 1. tokenise current file
            jacktokeniser = JackTokeniser(in_file, self.symbols, self.keywords)

            jacktokeniser.tokenise()

            ## manually review tokeniser output:
            # for token in jacktokeniser.tokens:
                #print(token)

            # 2. write tokenised text result to xml file output
            ## instanciate compilation engine
            compilation_engine = CompilationEngine(jacktokeniser, out_file)

            ## write to xml file 
            compilation_engine.compile_class()

            ## write newlines (to correct earlier mistake of writing everything on one line)
            write_xml_new_lines(out_file)
        
        
        # return to main after translating files
        return 0



class JackTokeniser():

    
    def __init__(self, file_in, symbols, keywords):
        self.current_file_in = file_in 
        self.tokens = [] # append each token one by one
        self.symbols = symbols
        self.keywords = keywords
        self.index = -1 # keeps track of current token requested by next_token method


    
    def tokenise(self):
        '''
        reads self.current_file and splits text into tokens
        returns a list of dictionaries of {"token": token, "token_type": token_type} in the order in which they appear in the current file
        '''

        with open(self.current_file_in) as f:
            
            # record whether reading a multi-line comment, default false
            open_comment = False
            for line_number, line in enumerate(f.readlines(), 1): # start line number at 1

                if is_comment_or_blank(line):
                    continue

                if is_open_comment(line):
                    open_comment = True
                
                if is_close_comment(line):
                    open_comment = False
                    continue

                if open_comment:
                    continue

                # remove mid-line comments and reduce multi white-space to single white-space between words
                cleaned_line = clean_line(line)

                ## now read cleaned line CHARACTER by CHARACTER and when you reach a token, add it to self.tokens
                # any time a token is appended to the list of tokens, reset variable token to an empty string
                # trash base token value
                token = "" 
                # boolean to control string tokens (these are handled slightly differently e.g., "function main () { } x = 1" is all 1 token if its a string)
                is_string_token = False
                
                for char in cleaned_line:  
                    # read char by char and build tokens      
                    if not is_string_token:
                        if char == '"':
                            token += char
                            is_string_token = True
                        # if you reach a symbol, assume previous chars form a token (these must be appended first for chronology)
                        # then append the symbol token
                        elif char in self.symbols and len(token) > 0:
                            self.tokens.append({"token": token, "token_type": self.token_type(token), "line_number": line_number})
                            token = ""
                            self.tokens.append({"token": char, "token_type": self.token_type(char), "line_number": line_number})
                        # if you reach a symbol and there are no previous chars, you can just append the symbol token
                        elif char in self.symbols and not token:
                            self.tokens.append({"token": char, "token_type": self.token_type(char), "line_number": line_number})
                            token = ""
                        # if you reach a space you have reached the end of a token 
                        # append this token if it contains at least 1 char
                        elif char == " " and token:
                            self.tokens.append({"token": token, "token_type": self.token_type(token), "line_number": line_number})
                            token = ""
                        # build up tokens (ignoring spces) e.g., "function void" is two seperate tokens
                        elif char != " ":
                            token += char 
                    # if reading a string:
                    else:
                        token += char
                        if char == '"':
                            self.tokens.append({"token": token, "token_type": self.token_type(token), "line_number": line_number}) # append full string enclosed in quotations
                            token = ""
                            is_string_token = False # return to normal token parsing

        # end of loop, return list of tokens in order of appearance         
        return self.tokens


    def token_type(self, token):

        if token.lower() in self.keywords:
            return "keyword"
        elif token in self.symbols:
            return "symbol"
        elif token.isnumeric():
            if int(token) >= 0 and int(token) <= 32767:
                return "integerConstant"
        elif token.strip()[0] == '"':
            return "stringConstant"
        else:
            for char in token:
                if ord(char) not in list(range(0,10)) + list(range(65,91)) + list(range(97,123)) + [95]:
                    raise Exception(f"\nINVALID TOKEN {token}")
            return "identifier"


    def next_token(self):
        if self.has_more_tokens():
            self.index += 1
            return self.tokens[self.index]
        else:
            raise Exception("No more tokens in list, reached final token")

    
    def current_token(self):
        if self.index >= 0:
            return self.tokens[self.index]
        else:
            raise Exception(f"\n Invalid token index: {self.index}")


    def previous_token(self):
        if self.index > 0:
            self.index -= 1
            return self.tokens[self.index]
        else:
            raise Exception("\nCannot go back further, no more previous tokens")


    def preview_next_token(self):
        return self.tokens[self.index+1]


    def has_more_tokens(self):
        if self.index < len(self.tokens):
            return True
        else:
            return False
        



class CompilationEngine():
    
    def __init__(self, jacktokeniser: JackTokeniser, file_out):
        self.jacktokensier = jacktokeniser
        self.out_file = file_out


    # first declaration must be a class (.jack file is a class)
    # xml file must be written in correct format
    def compile_class(self):
        with open(self.out_file, "a") as xml_file:
            
            # get first token
            print(len(self.jacktokensier.tokens))
            token =  self.jacktokensier.next_token()

            # write open class tag
            xml_file.write("<class>")

            # write class keyword 
            if token["token"] == "class":
                xml_file.write("<keyword> class </keyword>")
                token = self.jacktokensier.next_token()
            else:
                raise Exception("\nMissing keyword: 'class'")

            # write class identifier tags
            if token["token_type"] == "identifier":
                xml_file.write("<identifier> " + str(token["token"]) +  " </identifier>")
                token = self.jacktokensier.next_token()
            else:
                raise Exception("\nMissing identifier or keyword at line" + token["line_number"])
            
            # write class { symbol tags
            if token["token"] == "{":
                xml_file.write("<symbol> { </symbol>")
                token = self.jacktokensier.next_token()
            else:
                raise Exception("\nMissing symbol: '{'")
            
            # compile 1 or many class var declarations or  subroutines
            while True:
                token = self.jacktokensier.current_token()
                if token["token"] in ["static", "field"]:
                    self.compile_class_var_dec(xml_file)
                elif token["token"] in ["constructor", "function", "method"]:
                    self.compile_subroutine(xml_file)
                else:
                    break

            
            # write close class tag 
            token = self.jacktokensier.current_token()
            if token["token"] == "}":
                xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                xml_file.write("</class>")
            else:
                error = "\nMissing symbol " + "'}' at line " + str(token["line_number"]) + " to terminate class"
                raise Exception(error)

        # after end of all recursive calls, close file and return 
        return 0
            


    def compile_class_var_dec(self, xml_file):

        # open class_var_dec tag
        xml_file.write("<classVarDec>")

        # get next token in list
        token = self.jacktokensier.current_token()

        # static or field keyword
        if token["token"] in ["static", "field"]:
            xml_file.write("<keyword> " + str(token["token"]) + " </keyword>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("Missing keyword 'static' or 'field' at line " + str(token["line_number"]) + \
                            "\nInvalid token: " + str(token["token"]))

        # write var type (int, char, boolean, or custom class name (identifier))
        if token["token"] in ["int", "char", "boolean"]:
            xml_file.write("<keyword> " + str(token["token"]) + " </keyword>")
            token = self.jacktokensier.next_token()
        elif token["token_type"] == "identifier":
            xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
            token = self.jacktokensier.next_token()

        # compulsory varname
        if token["token_type"] == "identifier":
            xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("Missing identifier at line" + str(token["line_number"]) + \
                "\nInvalid token:" + str(token["token"]))

        # 0 or more varnames (identifiers)
        while True:
            # if no comma, there are no more varnames
            if token["token"] != ",":
                break
            else:
                # write comma 
                xml_file.write("<symbol> , </symbol>")
                # get next token
                token = self.jacktokensier.next_token()
                # varname?
                if token["token_type"] == "identifier":
                    xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
                    token = self.jacktokensier.next_token()
                else:
                    raise Exception("Missing identifier at line " + str(token["line_number"]) + \
                                    "\nInvalid token: " + str(token["token"]))


        # break from loop means all varnames declared
        
        # semi colon to terminate class_var_declaration
        if token["token"] == ";":
            xml_file.write("<symbol> ; </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("Missing ';' at line " + str(token["line_number"]) + \
            "\nInvalid token: " + str(token["token"]))
    
        # close class_var_dec tag
        xml_file.write("</classVarDec>")
        return 0
    


    def compile_subroutine(self, xml_file):

        # open subroutine tag
        xml_file.write("<subroutineDec>")

        # point token variable to current value in jacktokeniser
        token = self.jacktokensier.current_token()

        ## write keyword tag
        if token["token"] in ["constructor", "method", "function"]:
            xml_file.write("<keyword> " + str(token["token"]) + " </keyword>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nKeyword missing. 'constructor', " + \
                             "'method', or 'function' expected at line " +  str(token["line_number"]))
        
        
        ## write 'void' or type
        if token["token"] in ["void", "int", "char", "boolean"]:
            xml_file.write("<keyword> " + str(token["token"]) + " </keyword>")
            token = self.jacktokensier.next_token()
        elif token["token_type"] == "identifier":
            xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nInvalid syntax: " + str(token["token"])  + "of type" + {token["token_type"]} + \
                             " type must be an identier")
        
        ## write subroutine name
        if token["token_type"] == "identifier":
            xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing subroutine name at line " + str(token["line_number"]) + str(token["token"]) + \
                             + "is not a valid identifer")

        ## write open parenthesis
        if token["token"] == "(":
            xml_file.write("<symbol> ( </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing '(' at line " + str(token["line_number"]))
        
        ## write parameter list if next token is not closing the parentheses
        self.compile_parameter_list(xml_file)

        # exit function, realign token variable to point at current token value
        token = self.jacktokensier.current_token()
        ## write close parenthesis
        if token["token"] == ")":
            xml_file.write("<symbol> ) </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing ')' at line" + str(token["line_number"]) + \
                            "\ninvalid token: " + str(token["token"]))
        
        ## write subroutine body
        # open subroutine body tag
        xml_file.write("<subroutineBody>")
        # check for {
        if token["token"] == "{":
            xml_file.write("<symbol> { </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing '{' declaration at line " + str(token['line_number']) + "\ninvalid token: " + token['token'])
        
        # 0 or more var dec statements in subroutine body
        while True:
            if token["token"] != 'var':
                break
            self.compile_var_dec(xml_file)
            # repoint to current token after leaving function
            token = self.jacktokensier.current_token()

        # 0 or more statement(s) following var declaration
        self.compile_statements(xml_file)
        # repoint to current token after leaving function
        token = self.jacktokensier.current_token()

        # check for } to close subroutine body
        if token["token"] == "}":
            xml_file.write("<symbol> } </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing '}' declaration at line " + str(token['line_number']) + "\ninvalid token: " + token['token'])

        # close subroutine body tag
        xml_file.write("</subroutineBody>")

        # close subroutine tag
        xml_file.write("</subroutineDec>")
        return 0
    


    def compile_parameter_list(self, xml_file):

        # open parameter list tag
        xml_file.write("<parameterList>")

        # point token variable to current value in jacktokeniser
        token = self.jacktokensier.current_token()

        # check if any parameters present
        parameters = True
        if token["token"] == ")":
            parameters = False

        ## 1 or more parameters (function is only called if there is at least 1 parameter)
        while parameters:
            # type or classname (identifier)
            if token["token"] in ["int", "char", "boolean"]:
                xml_file.write("<keyword> " + str(token["token"]) + " </keyword>")
                token = self.jacktokensier.next_token()
            elif token["token_type"] == "identifier":
                xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
                token = self.jacktokensier.next_token()
            else:
                raise Exception("\nMissing type or class name declaration at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
           
            # var name (identifier)
            if token["token_type"] == "identifier":
                xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
                token = self.jacktokensier.next_token()
            else:
                raise Exception("\nMissing variable name declaration at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
            
            # optional comma (if present signifies another variable declaration: reloop)
            if token["token"] == ",":
                xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                token = self.jacktokensier.next_token()
            else:
                # return if no comma 
                break
                
        # close parameter list tag
        xml_file.write("</parameterList>")
        


    def compile_var_dec(self, xml_file):

        # open varDec tag
        xml_file.write("<varDec>")
        
        # point to current token
        token = self.jacktokensier.current_token()

        # varDec statement
        # 1. var
        if token["token"] == "var":
            xml_file.write("<keyword> var </keyword>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("missing keyword var at line: " + token["line_number"])

        # 2. type 
        if token["token"] in ["int", "boolean", "char"]:
            xml_file.write("<keyword> " + str(token["token"]) + " </keyword>")
            token = self.jacktokensier.next_token()
        elif token["token_type"] == "identifier":
            xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nInvalid var type at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))

        # 3. 1 or more var name(s)
        var_names = True
        while var_names:
            # var name
            if token["token_type"] == "identifier":
                xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
                token = self.jacktokensier.next_token()
            else:
                raise Exception("\nMissing var name declaration at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
        
            # comma to indicate another varname
            if token["token"] == ",":
                xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                token = self.jacktokensier.next_token()
            else:
                # break to terminate var dec
                var_names = False
        
        # var dec terminator symbol ";"
        if token["token"] == ";":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing var dec terminator ';' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
            
        
        # close varDec tag and return
        xml_file.write("</varDec>")
        return 0



    def compile_statements(self, xml_file):

        # open statements tag
        xml_file.write("<statements>")

        # point to current token
        token = self.jacktokensier.current_token()

        # check for 0 or more statements
        while True:
            # get current token (in case of reloop after returning from function)
            token = self.jacktokensier.current_token()
            if token["token"] not in ["let", "if", "while", "do", "return"]:
                # return if no more statements
                break
            elif token["token"] == "let":
                self.compile_let(xml_file)
            elif token["token"] == "if":
                self.compile_if(xml_file)
            elif token["token"] == "while":
                self.compile_while(xml_file)
            elif token["token"] == "do":
                self.compile_do(xml_file)
            elif token["token"] == "return":
                self.compile_return(xml_file)
            
        # close statements tag and return
        xml_file.write("</statements>")
        return 0
    


    def compile_let(self, xml_file):

        # open let statemnt tag
        xml_file.write("<letStatement>")

        # set pointer to current token
        token = self.jacktokensier.current_token()

        # let
        if token["token"] == "let":
            xml_file.write("<keyword> " + str(token["token"]) + " </keyword>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing keyword 'let' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))

        # var name
        if token["token_type"] == "identifier":
            xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing var name at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
        
        ## 0 or 1 expression
        # [
        if token["token"] == "[":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()

            self.compile_expression(xml_file)
            # repoint token to current value
            token = self.jacktokensier.current_token()

            # ]
            if token["token"] == "]":
                xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                token = self.jacktokensier.next_token()
        # no else statement: 0 expressions is allowed

        # (varname or expression) = 
        if token["token"] == "=":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing '=' expression at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
        
        # expression
        self.compile_expression(xml_file)

        # repoint to current token
        token = self.jacktokensier.current_token()

        # ; to terminate let statement
        if token["token"] == ';':
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing terminator ';' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))

        # close let statement tag and return
        xml_file.write("</letStatement>")



    def compile_if(self, xml_file):
        
        # open if statemnt tag
        xml_file.write("<ifStatement>")

        # set pointer to current token
        token = self.jacktokensier.current_token()

        # if
        if token["token"] == "if":
            xml_file.write("<keyword> " + str(token["token"]) + " </keyword>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing keyword 'if' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
        
        # (
        if token["token"] == "(":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing symbol '(' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))

        # expression
        self.compile_expression(xml_file)
        # repoint to current token
        token = self.jacktokensier.current_token()

        # )
        if token["token"] == ")":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing symbol ')' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
        
        # {
        if token["token"] == "{":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing symbol '{' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"])) 
        
        # statements
        self.compile_statements(xml_file)
        # repoint to current token
        token = self.jacktokensier.current_token()

        # }
        if token["token"] == "}":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing symbol '}' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
        
        # else
        if token["token"] == "else":
            xml_file.write("<keyword> " + str(token["token"]) + " </keyword>")
            token = self.jacktokensier.next_token()
        else:
            # close if statemnt tag
            xml_file.write("</ifStatement>")
            return 0
    
        # if not returned then complete else declaration:
        # {
        if token["token"] == "{":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing symbol '{' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
        
        # statements
        self.compile_statements(xml_file)
        # repoint to current token
        token = self.jacktokensier.current_token()

        # }
        if token["token"] == "}":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing symbol '}' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))

        # close if statemnet tag and return
        xml_file.write("</ifStatement>")
        return 0
        


    def compile_while(self, xml_file):
        
        # open while statemnt tag
        xml_file.write("<whileStatement>")

        # set pointer to current token
        token = self.jacktokensier.current_token()

        # while
        if token["token"] == "while":
            xml_file.write("<keyword> " + str(token["token"]) + " </keyword>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing keyword 'while' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
        
        # (
        if token["token"] == "(":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing symbol '(' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))

        # expression
        self.compile_expression(xml_file)
        # repoint to current token
        token = self.jacktokensier.current_token()

        # )
        if token["token"] == ")":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing symbol ')' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))

        # {
        if token["token"] == "{":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing symbol '{' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
        
        # statements
        self.compile_statements(xml_file)
        # repoint to current token
        token = self.jacktokensier.current_token()

        # }
        if token["token"] == "}":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing symbol '}' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))


        # close while statement tag and return
        xml_file.write("</whileStatement>")
        return 0 



    def compile_do(self, xml_file):
        
        # open do statemnt tag
        xml_file.write("<doStatement>")

        # set pointer to current token
        token = self.jacktokensier.current_token()

        # do
        if token["token"] == "do":
            xml_file.write("<keyword> " + str(token["token"]) + " </keyword>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing keyword 'do' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
        
        # subroutine call
        self.compile_subroutine_call(xml_file)
        # repoint to current token
        token = self.jacktokensier.current_token()

        # ";" to terminate do statement
        if token["token"] == ";":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing symbol ';' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))

        # close do statemnet tag and return
        xml_file.write("</doStatement>")
        return 0  



    def compile_return(self, xml_file):
        
        # open return statement tag
        xml_file.write("<returnStatement>")

        # point to current token
        token = self.jacktokensier.current_token()

        # return
        if token["token"] == "return":
            xml_file.write("<keyword> " + str(token["token"]) + " </keyword>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing keyword 'return' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
        
        # ; | expression;
        # ; 
        if token["token"] == ";":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
            # close return statement tag and return
            xml_file.write("</returnStatement>")
            return 0
        # expression;
        else:
            self.compile_expression(xml_file)
            # repoint to token
            token = self.jacktokensier.current_token()

            if token["token"] == ";":
                xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                token = self.jacktokensier.next_token()
                # close return statement tag and return
                xml_file.write("</returnStatement>")
                return 0
            else:
                raise Exception("\nMissing symbol ';' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))



 
    def compile_subroutine_call(self, xml_file):
        

        # get current token
        token = self.jacktokensier.current_token()

        ## subroutine call:
            # 1."subroutine_name(expr_list)" 
            # or
            # 2."class_name/var_name.subroutine_name(expr_list)"


        # 0. subroutine_name or class_name or var_name (all identifier)
        if token["token_type"] == "identifier":
            xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
            token = self.jacktokensier.next_token()
        else:
            raise Exception("\nMissing identifier at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
        
        # 1. assume subroutine_name written in 0.
        # 1.1 (
        if token["token"] == "(":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()

            # 1.2 expression list
            self.compile_expression_list(xml_file)
            # repoint to current token
            token = self.jacktokensier.current_token()

            # 1.3 )
            if token["token"] == ")":
                xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                token = self.jacktokensier.next_token()

        # 2. assume class_name or var_name written in 0.
        # 2.1 .
        elif token["token"] == ".":
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()
            
            # 2.2 subroutine name
            if token["token_type"] == "identifier":
                xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
                token = self.jacktokensier.next_token()
            else:
                raise Exception("\nMissing identifier at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
            
            # 2.3 (
            if token["token"] == "(":
                xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                token = self.jacktokensier.next_token()

            # 2.4 expression list
            self.compile_expression_list(xml_file)
            # repoint to current token
            token = self.jacktokensier.current_token()

            # 2.5 )
            if token["token"] == ")":
                xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                token = self.jacktokensier.next_token()
            else:
                raise Exception("\nMissing symbol ')' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))
                                
            
        else:
            raise Exception(f"\nInvalid subroutine call at line " + str(token["line_number"]) + " \nInvalid token: " + str(token["token"]))
        

        return 0




    def compile_expression(self, xml_file):
        
        # open expression tag
        xml_file.write("<expression>")

        # point to current token
        token = self.jacktokensier.current_token()

        # term
        self.compile_term(xml_file)
        # repoint
        token = self.jacktokensier.current_token()

        ## optional 0 or many: (op term)
        while True:
            # if token not in op then break and return 
            if token["token"] not in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
                break
            else:
                # op symbol
                if token["token"] not in ["<", ">", "&"]:
                    xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                elif token["token"] == "<":
                    xml_file.write("<symbol> &lt; </symbol>")
                elif token["token"] == ">":
                    xml_file.write("<symbol> &gt; </symbol>")
                elif token["token"] == "&":
                    xml_file.write("<symbol> &amp; </symbol>")
                token = self.jacktokensier.next_token()

                # term
                self.compile_term(xml_file)
                # repoint to current token after returning
                token = self.jacktokensier.current_token()


            # reloop and check for another op


        # close expression tag and return
        xml_file.write("</expression>")
        return 0




    def compile_term(self, xml_file):
        
        # open term tag
        xml_file.write("<term>")

        # point to current token
        token = self.jacktokensier.current_token()


        ##  implement compile_term
        # int constant
        if token["token_type"] == "integerConstant":
            xml_file.write("<" + str(token["token_type"]) + ">" + str(token["token"]) + "</" + str(token["token_type"]) + ">")
            token = self.jacktokensier.next_token()
        
        # string constant
        elif token["token_type"] == "stringConstant":
            xml_file.write("<" + str(token["token_type"]) + "> " + str(token["token"]).replace('"', "") + "</" + str(token["token_type"]) + ">")
            token = self.jacktokensier.next_token()

        # keyword constant
        elif token["token"] in ["true", "null", "false", "this"]:
            xml_file.write("<keyword> " + str(token["token"]) +  "</keyword>")
            token = self.jacktokensier.next_token()

        ## varname or varname[expression] or subroutine call
        # must first check if varname is addressing an array or just varname
        elif token["token_type"] == "identifier":
            ## write varname or subroutine name          

            # subroutine call
            if self.jacktokensier.preview_next_token()["token"] in ["(", "."]:
                
                self.compile_subroutine_call(xml_file)
                token = self.jacktokensier.current_token()
            
            # varname or varname[expression] 
            else:
                # varname
                xml_file.write("<identifier> " + str(token["token"]) + " </identifier>")
                token = self.jacktokensier.next_token()

                # [expression]
                if token["token"] == "[":
                    # [
                    xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                    token = self.jacktokensier.next_token()

                    # expression
                    self.compile_expression(xml_file)
                    token = self.jacktokensier.current_token()

                    # ]
                    if token["token"] == "]":
                        xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                        token = self.jacktokensier.next_token()
                    else:
                        raise Exception("\nMissing symbol ']' at line " + str(token["line_number"]) + "\ninvalid token: " + str(token["token"]))


        # (expression)
        elif token["token"] == "(":
            # (
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()

            # expression
            self.compile_expression(xml_file)
            token = self.jacktokensier.current_token()

            # )
            if token["token"] == ")":
                xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                token = self.jacktokensier.next_token()

        # unaryOp term
        elif token["token"] in ["~", "-"]:
            xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
            token = self.jacktokensier.next_token()

            self.compile_term(xml_file)
            token = self.jacktokensier.current_token()

        # raise exception if no valid input
        else:
            raise Exception(f"\nInvalid syntax at line: " + str(token["line_number"]) + \
                            "\nInvalid token: " + str(token["token"]))

        # close term tag and return
        xml_file.write("</term>")
        return 0




    def compile_expression_list(self, xml_file):
        
        # open expression list tag
        xml_file.write("<expressionList>")

        # point to current token
        token = self.jacktokensier.current_token()

        # return if empty expression list
        if token["token"] == ")":
            xml_file.write("</expressionList>")
            return 0

        # write list of expressions
        while True:
            self.compile_expression(xml_file)
            # repoint
            token = self.jacktokensier.current_token()

            # if comma, reloop and write another expression
            if token["token"] == ",":
                xml_file.write("<symbol> " + str(token["token"]) + " </symbol>")
                token = self.jacktokensier.next_token()

            # else no comma then end of expression list
            else:
                break

        # close expression list tag and return
        xml_file.write("</expressionList>")
        return 0





## Helper functions ##
def get_files(files_in: str):
    '''
    Takes input and looks for .jack files
    returns tuple containing two lists: 
        1. list ofall identified .jack files
        2. list of .xml file names for each .jack file
    '''

    # get uniform / for both windows and unix inputs
    input_argument = files_in.strip().replace("\\", "/") 

    input_jack_files = [] # store jack files from user input
    output_file_names = [] # list xml files for each corresponding jack file

    # identify input files or directories
    # directory of files
    if os.path.isdir(input_argument):
        for file in os.listdir(input_argument):
            if ".jack" in file.lower() and input_argument[-1] == "/":
                input_jack_files.append(input_argument + file)
            elif ".jack" in file.lower() and input_argument[-1] != "/":
                input_jack_files.append(input_argument + "/" + file)
    # single file
    elif os.path.isfile(input_argument):
        if ".jack" not in input_argument:
            raise Exception(f"file must be a jack file: {input_argument} is not a valid jack file")
        
        input_jack_files.append(input_argument.replace("\\", "/"))


    # write names for output files (output files are written as .xml)
    for file in input_jack_files:
        xml_name = file.replace(".jack", ".xml")
        output_file_names.append(xml_name)


    return (input_jack_files, output_file_names)



def is_comment_or_blank(line: str):
    '''
    Returns False if the line is blank or a comment line
    Returns True if line is jack code
    '''

    # remove leading and trailing whitespace and newline charcter
    line = line.strip() 

    # blank lines ignored
    if not line:
        return True
    # // comment lines ignored 
    elif line[0] == '/' and line[1] == '/':
            return True
    # /** comment lines ignores */
    elif line[0:3] == "/**" and line [-2:] == "*/":
        return True
    

    return False



def clean_line(line: str):
    '''
    Cleans each line to facilitate parsing
    Returns a string with no comments, and each word seperated by a single space:
        e.g., remove midline comment "class Main { // comment here" returns "class main {"
        e.g., remove midline comment "class Main { /* comment here */" returns "class main {"
        e.g., "this  is a    line with   spaces" becomes: "this is a line with spaces"
    '''

    # remove leading and trailing whitespace and newline charcter
    line = line.strip() 
    
    # write a cleaned version of the line 
    cleaned_line = ""
    # trash value in prev_char for first loop
    prev_char = "_"
    for char in line:

        # stop reading after // or /* , the remaining chars are comments
        if (prev_char == "/" and char == "/") or (prev_char == "/" and char == "*"):
            cleaned_line = cleaned_line[0:-1].strip() 
            break

        # if you reach */ , you have been reading a comment (/* comment here */)
        # so delete everything thus far and start copying again
        elif prev_char == "*" and char == "/":
            cleaned_line = ""
        
        # only write one space, ignore more than one space
        if not (char == " " and prev_char == " "):
            cleaned_line += char

        # store char just appended to cleaned line and loop to next char
        prev_char = char


    return cleaned_line



def is_open_comment(line: str):
    
    line = line.strip()

    if "/**" in line:
        return True
    
    return False



def is_close_comment(line: str):
    
    line = line.strip()

    if "*/" in line:
        return True
    
    return False



def write_xml_new_lines(file_name):
    '''
    write new lines for each close tag occurence
    original file was not passing nand2tetris submission tests as previous
    xml file was all written on one line
    '''
    with_new_lines = [] 
    with open(file_name, "r") as of:
        for char in of.read():
            with_new_lines.append(char)
            

    with open(file_name, "w") as of:

        xml_tag = ""
        write_new_line = False

        for i, char in enumerate(with_new_lines):
            
            xml_tag += char

            if char == "<":
                xml_tag = ""

            # only write new lines for these xml tags
            if xml_tag in ["class", "classVarDec", "subroutineDec", "parameterList", \
                            "subroutineBody", "statement", "letStatement", "expression", \
                            "term", "doStatement", "returnStatement", "expressionList", \
                            "ifStatement", "varDec", "whileStatement"] or (char == "<" and with_new_lines[i+1] == "/"):
                write_new_line = True
                xml_tag = ""

            # char
            of.write(char)

            if write_new_line == False:
                continue

            # newline
            if char == ">":
                of.write("\n")
                write_new_line = False
                xml_tag = ""


    return 0



## execute functions and classes in desired order
def main():

    # make sure input files are supplied
    if len(sys.argv) < 2:
        raise Exception("\nMust supply input file or directory as argument with JackAnalyser.py script call")
    
    # get lists of identified jack files and list of corresponding .xml file names for each jack file
    input_jack_files, output_file_names = get_files(files_in=sys.argv[1])
    
    # instanciate jackanalyser
    jackanalyser = JackAnalyser(input_jack_files, output_file_names)
    # create empty files that will be continuously appended to
    jackanalyser.create_blank_output_files()

    # call the JackTokeniser and CompilationEngine to translate the files into xml output format
    jackanalyser.translate_files()

    # all files are now translated, exit main



## call script
if __name__ == '__main__':
    main()