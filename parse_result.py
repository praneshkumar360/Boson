########################
##### PARSE RESULT #####
########################

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            res.error = None
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error, register_count=0):
        if not self.error and register_count == 0:
            self.error = error
        return self