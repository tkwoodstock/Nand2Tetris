from .to_binary import to_binary

def translate_a_instruction(instruction):
    # if number address (variables not allowed to start with a number)
    if ord(instruction[1]) <= 57 and ord(instruction[1]) >= 48:
        # iterate over each address character and ensure it's a number
        for char in instruction[1:]:
            if ord(char) > 57 or ord(char) < 48:
                raise Exception("explicit address calls can only contain numbers") 
            

        # convert decimal address to binary
        address_string = to_binary(instruction[1:], to_16=True)

        # # pad with zeros so instruction length is 16
        # zero_padding = 16 - len(address_string)
        # for zero in range(zero_padding):
        #     address_string = "0" + address_string

        # append to translated
        #translated.append(address_string)
        return address_string

