from dataclasses import field


class Record:
    def __init__(self, identifier: str, record_type: str):
        self.id = identifier
        self.type = record_type

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def set_id(self, identifier: str):
        self.id = identifier

    def set_type(self, record_type: str):
        self.type = record_type


class MethodRecord(Record):
    def __init__(self, identifier: str, record_type: str):
        super().__init__(identifier, record_type)
        self.parameter_list = []
        self.variable_list = []
        self.instruction_list = []


class ClassRecord(Record):
    def __init__(self, name: str, record_type: str):
        super().__init__(name, record_type)
        self.method_list = {}
        self.field_list = {}


class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.records = {}
        self.containing_class = None
        self.next = 0

    def next_child(self):
        if self.next >= len(self.children):
            new_scope = Scope(self)
            self.children.append(new_scope)
        else:
            new_scope = self.children[self.next]
        self.next += 1
        return new_scope

    def lookup(self, key: str):
        if key in self.records:
            return self.records[key]
        return self.parent.lookup(key) if self.parent else None

    def reset_scope(self):
        self.next = 0
        for child in self.children:
            child.reset_scope()

    def print_scope(self):
        left_align_format = "| %-29s | %-19s | %-27s|"
        print("+-------------------------------+---------------------+----------------------------+")
        for key, value in self.records.items():
            record_class = type(value).__name__
            print(left_align_format % (key, value.get_type(), record_class))
            print("+-------------------------------+---------------------+----------------------------+")
        for child in self.children:
            child.print_scope()


class SymbolTable:
    def __init__(self):
        self.root = Scope()
        self.current = self.root

    def enter_scope(self):
        self.current = self.current.next_child()

    def exit_scope(self):
        self.current = self.current.parent

    def lookup(self, key: str):
        return self.current.lookup(key)

    def reset_table(self):
        self.current = self.root
        self.root.reset_scope()

    def print_table(self):
        print("\n\n\t\tPrinting the Symbol Table:\n")
        print("+-------------------------------+---------------------+----------------------------+")
        print("|             ID                |         TYPE        |        SCOPE/RECORD        |")
        print("+-------------------------------+---------------------+----------------------------+")
        self.root.print_scope()
        print("+-------------------------------+---------------------+----------------------------+")