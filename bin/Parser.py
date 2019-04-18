"""
Parses input .asm file and creates simplified object to be
decoded by Code module.
"""

class Parser(object):
    """Class representing an object to parse an input .asm file."""

    def __init__(self, input_file):
        self.input_file = input_file

        # initiate mapping of symbols to their mem locations
        # variable mappings will be added to this list as they're encountered.
        self.symbols = {"SP": 0, "LCL": 1, "ARG": 2,
                        "THIS": 3, "THAT": 4, "R0": 0, "R1": 1, "R2": 2,
                        "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7, "R8": 8,
                        "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13,
                        "R14": 14, "R15": 15, "SCREEN": 16384, "KDB": 24576}

        # loop through and index jump labels into dictionary.
        with open(input_file, 'r') as raw_file:
            self.jump_labels = {}
            line_num = 0
            AC_only_list = []

            for line in raw_file:
                no_comments_line = line.split("//")[0]
                stripped_line = no_comments_line.strip()

                if stripped_line == '':
                    # weed out empty lines and comment lines
                    # don't increment counter or transcribe to new list.
                    pass
                elif stripped_line[0] == "(":
                    # read in all characters until close parenthesis.
                    # don't increment counter or transcribe to new list.
                    symbol = stripped_line[1:].split(")")[0]
                    self.jump_labels[symbol] = line_num + 1
                else:
                    print("\t%d - %s" % (line_num, stripped_line))
                    line_num += 1
                    AC_only_list.append(stripped_line)

        self.stripped_file = AC_only_list

    def jump_map(self):
        return self.jump_labels

    def variable_mem_map(self):
        return self.variables

    def write_parsed_file(self):
        pass
