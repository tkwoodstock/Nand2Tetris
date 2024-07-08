# Tyler Woodstock Projects for Nand2Tetris

## Project 6 - Assembly Code to Machine Code Translator
* Assembly code translator that processes Hack assembly language and translates into 16-bit machine code
* Low level architecture provided by Nand2Tetris project brief
* 16-bit instructions directly influence CPU operation
* Instructions include:
    * A-instructions (to target A-register)
    * C-instructions (to target ALU and PC)



## Project 7 - Virtual Machine Langauge to Assembly Code Translator Part 1 (Stack Arithmetic and Stack Processing Only)
*  Partial VM translator to translate Jack VM language (loosely based on JVM, the Java Bytecode interpretor) into target language (Hack Assembly language)
*  Achieved through stack processing (e.g., push, pop) and stack arithmetic (e.g., add)
*  This is part 1 of the VM translator, this script cannot translate:
    * Branching commands (e.g., goto, if-goto)
    * Function commands (e.g., call, return)



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


![Tylers_Tetris_gif_demo](https://github.com/tkwoodstock/Nand2Tetris/assets/92792893/e0f6bff8-a962-4a47-91ac-8286c2eb3a84)



## Project 10 - Code Compiler Part 1: Syntax Analysis
* JackAnalyser.py takes a file or directory as an argument and translates each ".jack" file into a ".xml" file
* The output xml file(s) is
* The result is acheived with three classes: JackAnalyser, JackTokeniser, and CompilationEngine
    * JackAnalyser: Defines keywords, creates blank xml files for output, instanciates JackTokeniser and Compilation Engine
    * JackTokeniser: Reads input jack file character by character, groups collections of characters that satisfy the "token" definition, and stores in a list
    * CompilationEngine: Reads the list of tokens provided by the JackTokeniser and writes to xml format if tokens are in an appropriate order according to jack language syntax
* Class methods have been written for each of the above, to provide the required functionality
* Full compilation of jack language is completed in project 10, where the tokenised xml translation of the jack file is translated to jack virtual machine language (loosely based on java bytecode)



