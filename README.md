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


