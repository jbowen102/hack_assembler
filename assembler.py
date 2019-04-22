from bin import Parser, Code

while True:
    assy_file = input("Enter file path (rel to asm_code) for assembly code: ")
    if assy_file:
        break

assy_path = "./asm_code/" + assy_file

parse = Parser.Parser(assy_path)
mach_code = Code.Code(parse)

hack_file = input("Enter file path for new Hack file "
                        "or Enter to use same name: ")
if not hack_file:
    hack_file = assy_file.split("/")[-1][:-4] + ".hack"
hack_path = "./hack_code_output/" + hack_file

mach_code.write_hack_file(hack_path)
