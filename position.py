######################
####   POSITION   ####
######################

class Position:
    def __init__(self, index, line, col, file_name, file_txt):
        self.index = index
        self.line = line
        self.col = col
        self.file_name = file_name
        self.file_txt = file_txt
    
    def increment(self, curr_char=None):
        self.index += 1
        self.col += 1

        if curr_char == '\n':
            self.line += 1
            self.col = 0

    def copy(self):
        return Position(self.index, self.line, self.col, self.file_name, self.file_txt)