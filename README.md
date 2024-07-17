# Tyler Woodstock Projects for Nand2Tetris

## Overview
Nand2Tetris is a free online course delivered by Noam Nisan and Shimon Schocken at the Hebrew University of Jerusalem. 

The course covers lower level computing concepts to give a better understanding of what happens "underneath the hood" of a modern computer and how higher-level programming languages are designed and developed. 
The structure of the course follows a trajectory of increasing computing complexity from low level logic gates up to a high-level programming language and full operating system, covering concepts such as:
boolean logic, logic gates, memory, computer architecture, machine langauge, assembly code, virtual machines, code compilation, and high-level object oriented programming.

This repository contains my solutions to some of the projects in the course.
* Projects 1-5 are omitted as the solutions will have low degrees of variability between course participants. These projects (1-5) cover logic gates and boolean logic, building registers and RAM, machine language, assembly code, and computer architecture.
* Projects 6-12 allow for more flexbility in implementation between course participants and as such are a better reflection of my own individual work as a result of completing this course; details for each of these projects can be seen below. Taken together, projects 6-12 demonstrate the entire process of:
  1. Writing high-level language 
  2. Compiling to platform-independent virtual machine code (stack processing, branching, and flow control)
  3. Translating virtual machine code to assembly code (addressing registers and CPU arithmetic)
  4. Translating assembly code into machine code (16-bit instructions for ROM, CPU, and RAM)


## Project 6 - Assembly Code to Machine Code Translator
* Assembly code translator that processes Hack assembly language and translates into 16-bit machine code
* Low level architecture provided by Nand2Tetris project brief
* 16-bit instructions directly influence CPU operation
* Instructions include:
    * A-instructions (to target A-register)
    * C-instructions (to target ALU and PC)


![assembly_to_machine](https://github.com/tkwoodstock/Nand2Tetris/assets/92792893/922061c1-c216-4136-8862-0d4bc93a9f7d)




## Project 7 - Virtual Machine Langauge to Assembly Code Translator Part 1 (Stack Arithmetic and Stack Processing Only)
*  Partial VM translator to translate Jack VM language (loosely based on JVM, the Java Bytecode interpretor) into target language (Hack Assembly language)
*  Achieved through stack processing (e.g., push, pop) and stack arithmetic (e.g., add)
*  This is part 1 of the VM translator, this script cannot translate:
    * Branching commands (e.g., goto, if-goto)
    * Function commands (e.g., call, return)
 

![vm_to_assembly1](https://github.com/tkwoodstock/Nand2Tetris/assets/92792893/597cbb9f-310f-4479-af96-bc6699313f8a)




## Project 8 - Virtual Machine Langauge to Assembly Code Translator Part 2 (Full Functionality)
* Full VM translator to translate Jack VM language (loosely based on JVM, the Java Bytecode interpretor) into target language (Hack Assembly language)
* Achieved through stack processing (e.g., push, pop) and stack arithmetic (e.g., add)
* This is part 2 of the VM translator and can handle branching commands (e.g., goto, if-goto) and function commands (e.g., call, return)


![vm_to_assembly2](https://github.com/tkwoodstock/Nand2Tetris/assets/92792893/d8e45de9-fa89-416f-a501-c48ede76b482)




## Project 9 - Interactive Tetris Game Written in Jack Language
* Jack is a high-level object oriented language based on Java
* The game is written using three jack class files (Block.jack, TetrisGame.jack, Main.jack), in accordance with the Model, View, Controller (MVC) software design pattern
* Development time from concept to completion was approx. 15 hours
* Key features of my tetris game:
    * Semi-random shape generator
    * 3-tiers of difficulty level (increasing difficulty = faster gameplay + greater variety in shapes)
    * Live score counter display


![my_tetris_clip_x2](https://github.com/tkwoodstock/Nand2Tetris/assets/92792893/a98f52e1-0afc-4fd2-b8ae-2ccce0c9db17)



## Project 10 - Code Compiler Part 1: Syntax Analysis
* JackAnalyser.py takes a file or directory as an argument and translates each ".jack" file into a ".xml" file in a top-down parse tree approach
* The result is acheived with three classes: JackAnalyser, JackTokeniser, and CompilationEngine
    * JackAnalyser: Defines keywords, creates blank xml files for output, instanciates JackTokeniser and Compilation Engine
    * JackTokeniser: Reads input jack file character by character, parses into grouped collections of characters that satisfy the "token" definition, stored in a list
    * CompilationEngine: Reads the list of tokens provided by the JackTokeniser and writes to xml format if tokens are in an appropriate order according to jack language syntax specification
* Class methods have been written for each of the above, to provide the required functionality
* Full compilation of jack language is completed in project 10, where the jack file is translated directly to jack virtual machine language (loosely based on java bytecode)


![jack_to_xml](https://github.com/tkwoodstock/Nand2Tetris/assets/92792893/0134bd55-15e2-4903-bb29-f2fe3572de0a)




