class Emitter:

    # full_path - the name that was passed to the Emitter in main
    def __init__(self, full_path):
        self.full_path = full_path
        self.header = ''
        self.code = ''

    # function for adding C code
    # code is a string containing the C code that is generated
    def emit(self, code):
        self.code += code

    # function for adding a fragment that ends a line
    # for example exit("while(") and the emit_line function will return emit_line("){")
    def emit_line(self, code):
        self.code += code + '\n'

    def header_line(self, code):
        self.header += code + '\n'

    # writeFile writes the C code to a file
    def write_file(self):
        with open(self.full_path, 'w') as output_file:
            output_file.write(self.header + self.code)

    
