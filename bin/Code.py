

def binary_convert(dec_val, bin_digits):
    """ Function to convert a decimal number into a binary number, formatted
    to fill 'bin_digits' digits. Returns binary number as string
    """
    return format(dec_val, '0%db' % bin_digits)

class ConversionTable(object):
    def __init__(self):
        self.comp_dict = {"0": "101010",
                         "1": "111111",
                         "-1": "111010",
                         "D": "001100",
                         "A": "110000",
                         "M": "110000",
                         "!D": "001101",
                         "!A": "110001",
                         "!M": "110001",
                         "-D": "001111",
                         "-A": "110011",
                         "-M": "110011",
                         "D+1": "011111",
                         "A+1": "110111",
                         "M+1": "110111",
                         "D-1": "001110",
                         "A-1": "110010",
                         "M-1": "110010",
                         "D+A": "000010",
                         "D+M": "000010",
                         "D-A": "010011",
                         "D-M": "010011",
                         "A-D": "000111",
                         "M-D": "000111",
                         "D&A": "000000",
                         "D&M": "000000",
                         "D|A": "010101",
                         "D|M": "010101"}

        self.dest_dict = {"0": "000",
                          "M": "001",
                          "D": "010",
                          "MD": "011",
                          "A": "100",
                          "AM": "101",
                          "AD": "110",
                          "AMD": "111"}

        self.jump_dict = {"0": "000",
                          "JGT": "001",
                          "JEQ": "010",
                          "JGE": "011",
                          "JLT": "100",
                          "JNE": "101",
                          "JLE": "110",
                          "JMP": "111"}

    def comp_convert(self, command):
        return self.comp_dict[command]

    def dest_convert(self, command):
        return self.dest_dict[command]

    def jump_convert(self, command):
        return self.jump_dict[command]


class HackLine(object):
    """Class representing a line of Hack code"""

    def __init__(self, command):
        self.type = command.command_type()
        self.converter = ConversionTable()

        if self.type == "A":
            dec_value = command.value()
            lower_15 = binary_convert(dec_value, 15)
            top_1 = "0"
            self.full_bin_val = top_1 + lower_15
        elif self.type == "C":
            top_3 = "111"

            if "m" in command.value()[0].lower():
                a_bit = "1"
            else:
                a_bit = "0"

            comp_command = command.value()[0]
            dest_command = command.value()[1]
            jump_command = command.value()[2]

            comp_bits = self.converter.comp_convert(comp_command)
            dest_bits = self.converter.dest_convert(dest_command)
            jump_bits = self.converter.jump_convert(jump_command)

            self.full_bin_val = top_3 + a_bit + comp_bits + dest_bits + jump_bits
        else:
            raise ValueError("Unexpected command type: %d: %s" % (line, self.type))

    def binary_line(self):
        return self.full_bin_val


class HackGroup(object):
    """Class representing a block of Hack code"""

    def __init__(self):
        self.hack_dict = {}

    def add_hack_command(self, line, comm):
        self.hack_dict[line] = comm

    def get_hack_command(self, line):
        return self.hack_dict[line]

    def line_list(self):
        lines = []
        for key in self.hack_dict.keys():
            lines.append(key)
        lines.sort()
        return lines


class Code(object):
    """Class representing an object for converting parsed .asm code (from Parser
    module) into Hack code."""

    def __init__(self, parser):
        commands = parser.parsed_commands()

        self.converted_code = HackGroup()

        for line in commands.line_list():
            command = commands.get_command(line)

            current_hack_line = HackLine(command)

            self.converted_code.add_hack_command(line, current_hack_line)


    def write_hack_file(self, filepath):
        # write .hack file by transcribing from self.commands
        with open(filepath, 'w') as new_file:
            for line in self.converted_code.line_list():
                current_command = self.converted_code.get_hack_command(line)
                binary_string = current_command.binary_line()

                new_file.write(binary_string + "\n")
                # write binary_string to line in new file.
