"""
Parses input .asm file and creates simplified object to be
decoded by Code module.
"""

def try_num(string_in):
    try:
        int(string_in)
        return True
    except ValueError:
        return False


class SymbolTable(object):
    """Class representing the mapping of symbols to values."""
    def __init__(self):
        self.symbol_map = {}

    def add_entry(self, key, val):
        if key in self.symbol_map:
            "Error: trying to update existing SymbolTable entry."
        else:
            self.symbol_map[key] = val

    def symbol_val(self, key):
        return self.symbol_map[key]

    def symbol_list(self):
        return self.symbol_map.keys()

    def val_list(self):
        return self.symbol_map.values()


class RAMTable(SymbolTable):
    """Subclass of SymbolTable representing the more-specific
    mapping of symbols to RAM values.
    Already includes system predefined and I/O pointers."""

    def __init__(self):
        self.symbol_map = {"SP": 0, "LCL": 1, "ARG": 2,
                        "THIS": 3, "THAT": 4, "R0": 0, "R1": 1, "R2": 2,
                        "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7, "R8": 8,
                        "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13,
                        "R14": 14, "R15": 15, "SCREEN": 16384, "KDB": 24576}
        self.next_avail_val = 16

    def add_entry(self, symbol):
        # differs from parent class in auto-assignment of value
        if self.next_avail_val >= 16384:
            raise ValueError("Max RAM allotment reached. Cannot continue.")
        else:
            self.symbol_map[symbol] = self.next_avail_val
            self.next_avail_val += 1


class CommandSet(object):
    """Class representing multiple command objects parsed from a .asm file."""
    def __init__(self):
        self.command_dict = {}

    def add_command(self, line, comm):
        self.command_dict[line] = comm


class Command(object):
    """Class representing a single parsed command from .asm file."""

    def __init__(self, command_line, jumps, variables):
        self.raw_command = command_line
        self.jump_map = jumps
        self.variable_map = variables

        # code to determine what type of command the object is
        # code to parse the specific command into its parts (dest, jump, etc.)
        if self.raw_command[0] == "@":
            self.type = "A"
            raw_A = self.raw_command[1:]

            # look for symbol in variable dictionary or interpret as raw number
            # if not either one, then add variable to variable dictionary,
            # linking it to the next available mem slot.

            if try_num(raw_A):
                self.A_value = int(raw_A)
            elif raw_A in self.jump_map.symbol_list():
                self.A_value = self.jump_map.symbol_val(raw_A)
            elif raw_A in self.variable_map.symbol_list():
                self.A_value = self.variable_map.symbol_val(raw_A)
            else:
                self.variable_map.add_entry(raw_A)
                self.A_value = self.variable_map.symbol_val(raw_A)

        else:
            self.type = "C"

            if "=" in self.raw_command:
                self.comp = self.raw_command.split("=")[1]
                self.dest = self.raw_command.split("=")[0]
                self.jump = 0;
            elif ";" in self.raw_command:
                self.comp = self.raw_command.split(";")[0]
                self.dest = 0;
                self.jump = self.raw_command.split(";")[1]
            else:
                raise ValueError("C-command identified with invalid value:\n\t%s"
                                % self.raw_command)

            self.C_value = [self.comp, self.dest, self.jump]

    def command_type(self):
        return self.type

    def value(self):
        if self.type == "A":
            return self.A_value
        elif self.type == "C":
            return self.C_value
        else:
            return None

    def asm_text(self):
        return self.raw_command

    def __repr__(self):
        return self.raw_command


class Parser(object):
    """Class representing an object to parse an input .asm file."""

    def __init__(self, input_file):
        self.input_file = input_file

        # initiate mapping of symbols to their mem locations
        # variable mappings will be added to this list as they're encountered.
        self.jumps = SymbolTable()
        self.variables = RAMTable()

        # loop through and index jump labels into dictionary.

        with open(input_file, 'r') as raw_file:
            self.stripped_file = []
            line_num = 0

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
                    self.jumps.add_entry(symbol, line_num)
                else:
                    line_num += 1
                    self.stripped_file.append(stripped_line)

        self.commands = CommandSet()
        line = 0
        for command_line in self.stripped_file:
            current_command = Command(command_line, self.jumps, self.variables)
            self.commands.add_command(line, current_command)
#             if current_command.command_type() == "A":
#                 print("\t%d - %s (%d)" % (line, current_command.asm_text(),
#                                                 current_command.value()))
# #                print("\t%d - %s (%d)" (line, command_line, current_command.value()))
#             else:
#                 print("\t%d - %s " % (line, current_command.asm_text()), end="")
#                 print(current_command.value())
            line += 1

    def jump_map(self):
        return self.jumps

    def variable_map(self):
        return self.variables

    def parsed_commands(self):
        return self.commands

    def write_parsed_file(self):
        # write .hack file by transcribing from self.commands
        pass
