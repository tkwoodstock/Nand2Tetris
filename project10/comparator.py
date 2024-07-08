import sys


'''
Takes 2 xml files and compares their content token for token
'''


# file1
f1 = []
with open(sys.argv[1]) as file:
    for char in file.read():
        f1.append(char)

# file2
f2 = []
with open(sys.argv[2]) as file:
    for char in file.read():
        f2.append(char)

# line numbers
line_f1 = 1
line_f2 = 1

# character indexes
f1i = 0
f2i = 0


# compare
while True:

    # break if end of chars
    if f1i == len(f1) or f2i == len(f2):
        print("end of file, files exactly the same")
        break

    # assign chars
    char1 = f1[f1i]
    char2 = f2[f2i]

    # increment line number
    if char1 == "\n":
        line_f1 += 1
    if char2 == "\n":
        line_f2 += 1

    # ignore spaces 
    if char1 == " ":
        f1i += 1
        continue
    if char2 == " ":
        f2i += 1
        continue

    # compare chars
    if char1 == char2:
        #print(f"MATCH char1 '{char1}' = char2 '{char2}'")
        f1i += 1
        f2i += 1

    if char1 != char2:
        print("\nMISTMATCH CHARS:")
        print(f"{sys.argv[1]} char: {char1} | {sys.argv[2]} char: {char2}")
        print(f"\nMISMATCH AT LINES:")
        print(f"{sys.argv[1]}: line {line_f1}")
        print(f"{sys.argv[2]}: line {line_f2}")
        raise Exception("\nEXITING DUE TO MISMATCH")
