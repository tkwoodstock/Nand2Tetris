
def clean_line(ln):
    # remove outer whitespace
    ln = ln.strip()
    # remove inner whitespace and ?? ignore break line character at end of line ??
    temp_line = ""
    prev_char = ""
    for char in ln:
        # ignore spaces
        if char != " " and char != "/":
            temp_line += char

        # ignore any text after comment syntax: (comment = // commented text here)
        if prev_char == "/" and char == "/":
            break
   
        prev_char = char # remember previous character to check for comments

    ln = temp_line

    return ln

