from assembler import assembler


test_base = "nand2tetris_project6/test_files/"
test_tail = ".asm"

files = ["Add", "Max", "Pong", "Rect"]
#files = ["Pong"]

outbase = "nand2tetris_project6/output/"
out_tail = ".hack"

for file in files:
    assembler(test_base+file+test_tail, outbase+file+out_tail)

