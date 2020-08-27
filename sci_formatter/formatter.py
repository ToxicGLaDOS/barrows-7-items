import re

def is_sci_form(s):
    pattern = re.compile(r'(-?\d+\.?\d*)(E|e)(-?\d+)')
    matches = re.match(pattern, s)

    if matches:
        return True
    else:
        return False

def build_number_string_from_sci_form(sci_form):
    pattern = re.compile(r'(-?\d+\.?\d*)(E|e)(-?\d+)')
    matches = re.match(pattern, sci_form)
    if matches:
        digits = matches.group(1)
        exponent = int(matches.group(3))
        for x in range(int(abs(exponent))):
            digits = shift(digits, exponent)

        return digits
    else:
        raise Exception("String not in valid scientific notation")

def shift(number, direction):
    if direction > 0:
        number = shift_right(number)
    elif direction < 0:
        number = shift_left(number)
    else:
        raise Exception("Hey don't do that.")

    return number

def cleanup_number(number):
    split = number.split('.')
    lhs = split[0]
    sign = ''
    if lhs and lhs[0] == '-':
        sign = '-'
        lhs = lhs[1:]
    # If lhs is empty string then we had something like .01
    # so we just set lhs to 0 which will result in 0.01 after combining at the end
    if lhs == '':
        lhs = '0'
    lhs = cleanup_left(lhs)
    rhs = ''

    # Make sure there is a second element and the second element isn't empty string
    if len(split) == 2 and split[1]:
        rhs = cleanup_right(split[1])

    # If rhs isn't empty than return the cleaned up lhs with the '.' and rhs
    if rhs:
        return sign + lhs + '.' + rhs
    # If rhs is empty than the value is an int so we don't need to reintroduce the '.'
    else:
        return sign + lhs

def cleanup_left(lhs):
    # We need length of a to be greater than 1 because
    # if the last digit is 0 then the result should be 0
    # for example '0000000' should cleanup into '0' not ''
    while len(lhs) > 1 and lhs[0] == '0':
        lhs = lhs[1:]

    return lhs

def cleanup_right(rhs):
    # We allow the rhs to be trimmed all the way down to ''
    # because 1.00000 should become 1
    while len(rhs) > 0 and rhs[-1] == '0':
        rhs = rhs[:-1]

    return rhs

def shift_right(number):
    split_number = list(number)
    # We're dealing with a float
    if '.' in split_number:
        dot_index = split_number.index('.')
        # If the . is on the very right side already
        if dot_index == len(split_number) - 1:
            split_number[dot_index] = '0'
        else:
            # Set the . to be the number after the dot
            # then set the number after the dot to be the dot
            split_number[dot_index] = split_number[dot_index + 1]
            split_number[dot_index + 1] = '.'
    else:
        split_number.append('0')

    return cleanup_number(''.join(split_number))

def shift_left(number):
    split_number = list(number)

    if '.' in split_number:
        dot_index = split_number.index('.')
        # If the dot is right at the beginning
        if dot_index == 0:
            # Replace the dot with a 0 and put a dot before it
            # Effectively add a 0
            split_number[dot_index] = '0'
            split_number.insert(0, '.')
        else:
            # Switch the dot and the number before it
            split_number[dot_index] = split_number[dot_index - 1]
            split_number[dot_index - 1] = '.'

    else:
        # Add a dot second from last
        # Example: 10001 -> 1000.1
        split_number.insert(-1, '.')

        # This happens when the number is only one character long.
        # For instance: shift_left(0) becomes '.0' after the insert from the previous line
        # So we want to add a 0 before that to make it '0.0'
        if split_number[0] == '.':
            split_number.insert(0, '0')

    return cleanup_number(''.join(split_number))

if __name__ == "__main__":
    tests = {
        "0E9": "0",
        "0E-44": "0",
        "1E-3": "0.001",
        "3.14159E7": "31415900",
        "1000E2": "100000",
        "-0E-2": "-0",
        "-4.0E-5": "-0.00004",
        "-7E8": "-700000000",
        "3.48589471521581E6": "3485894.71521581",
        "4.253410648674087E8": "425341064.8674087",
        "-0.5837697425993881E-18": "-0.0000000000000000005837697425993881",
        "11.869394714721945E4": "118693.94714721945",
        "50.713381783697855E4": "507133.81783697855",
        "-37.051413707432545E-15": "-0.000000000000037051413707432545",
        "-0.9918169178691116E7": "-9918169.178691116",
        "1.7324838038078278E-10": "0.00000000017324838038078278",
        "15.45516245820167E-10": "0.000000001545516245820167",
        "-0.4510893237335487E15": "-451089323733548.7"
    }

    for k, v in tests.items():
        if build_number_string_from_sci_form(k) != v:
            print(k, v, build_number_string_from_sci_form(k))
            assert False

