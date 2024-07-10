# Tyler Woodstock Projects for Nand2Tetris

## Project 6 - Assembly Code to Machine Code Translator
* Assembly code translator that processes Hack assembly language and translates into 16-bit machine code
* Low level architecture provided by Nand2Tetris project brief
* 16-bit instructions directly influence CPU operation
* Instructions include:
    * A-instructions (to target A-register)
    * C-instructions (to target ALU and PC)



![assembly_to_machine](https://github.com/tkwoodstock/Nand2Tetris/assets/92792893/b05f9a72-1c4f-459e-8736-ef8ca5af83b9)





## Project 7 - Virtual Machine Langauge to Assembly Code Translator Part 1 (Stack Arithmetic and Stack Processing Only)
*  Partial VM translator to translate Jack VM language (loosely based on JVM, the Java Bytecode interpretor) into target language (Hack Assembly language)
*  Achieved through stack processing (e.g., push, pop) and stack arithmetic (e.g., add)
*  This is part 1 of the VM translator, this script cannot translate:
    * Branching commands (e.g., goto, if-goto)
    * Function commands (e.g., call, return)
 

![vm_to_assembly](https://github.com/tkwoodstock/Nand2Tetris/assets/92792893/9a700d60-909a-4e46-85a3-f3c4d7eb304c)




## Project 8 - Virtual Machine Langauge to Assembly Code Translator Part 2 (Full Functionality)
* Full VM translator to translate Jack VM language (loosely based on JVM, the Java Bytecode interpretor) into target language (Hack Assembly language)
* Achieved through stack processing (e.g., push, pop) and stack arithmetic (e.g., add)
* This is part 2 of the VM translator and can handle branching commands (e.g., goto, if-goto) and function commands (e.g., call, return)



## Project 9 - Interactive Tetris Game Written in Jack Language
* Jack is a high-level object oriented language based on Java
* The game is written using three jack class files (Block.jack, TetrisGame.jack, Main.jack), in accordance with the Model, View, Controller (MVC) software design pattern
* Development time from concept to completion was approx. 15 hours
* Key features of my tetris game:
    * Semi-random shape generator
    * 3-tiers of difficulty level (increasing difficulty = faster gameplay + greater variety in shapes)
    * Live score counter display


![my_tetris_clip_x3](https://github.com/tkwoodstock/Nand2Tetris/assets/92792893/b6226984-68d9-4c52-bb15-91520e97333c)




## Project 10 - Code Compiler Part 1: Syntax Analysis
* JackAnalyser.py takes a file or directory as an argument and translates each ".jack" file into a ".xml" file in a top-down parse tree approach
* The result is acheived with three classes: JackAnalyser, JackTokeniser, and CompilationEngine
    * JackAnalyser: Defines keywords, creates blank xml files for output, instanciates JackTokeniser and Compilation Engine
    * JackTokeniser: Reads input jack file character by character, parses into grouped collections of characters that satisfy the "token" definition, stored in a list
    * CompilationEngine: Reads the list of tokens provided by the JackTokeniser and writes to xml format if tokens are in an appropriate order according to jack language syntax specification
* Class methods have been written for each of the above, to provide the required functionality
* Full compilation of jack language is completed in project 10, where the tokenised xml translation of the jack file is translated to jack virtual machine language (loosely based on java bytecode)


![jack_to_xml](https://github.com/tkwoodstock/Nand2Tetris/assets/92792893/fa883be9-20da-467d-b286-7c6bc3e59c16)




