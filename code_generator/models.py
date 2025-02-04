from enum import Enum
from typing import List
from semantic_analyse.models import Record
from collections import OrderedDict
from typing import Dict


class Opcode(Enum):
    ADD = "ADD"                 # t = a + b
    SUB = "SUB"                 # t = a - b
    MUL = "MUL"                 # t = a * b
    DIV = "DIV"                 # t = a / b
    ASSIGN = "ASSIGN"           # t = a
    LT = "LT"                   # t = (a < b) ? 1 : 0
    EQ = "EQ"                   # t = (a == b) ? 1 : 0
    AND = "AND"                 # t = a && b
    OR = "OR"                   # t = a || b
    NOT = "NOT"                 # t = !a
    GOTO = "GOTO"               # goto label
    IF_TRUE = "IF_TRUE"         # if (a) goto label
    IF_FALSE = "IF_FALSE"       # if (!a) goto label
    PARAM = "PARAM"             # param a (pass parameter for function call)
    CALL = "CALL"               # t = call func, nargs
    RETURN = "RETURN"           # return t
    PRINT = "PRINT"             # print t
    LABEL = "LABEL"             # label: (define a label)


class Instruction:
    def __init__(self, opcode: Opcode, operand1=None, operand2=None, operand3=None):
        self.opcode = opcode
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3

    def process_opcode(self, ):
        match self.opcode:
            case Opcode.ADD:
                return f"{self.operand1} = {self.operand2} + {self.operand3}"
            case Opcode.SUB:
                return f"{self.operand1} = {self.operand2} - {self.operand3}"
            case Opcode.MUL:
                return f"{self.operand1} = {self.operand2} * {self.operand3}"
            case Opcode.DIV:
                return f"{self.operand1} = {self.operand2} / {self.operand3}"
            case Opcode.ASSIGN:
                return f"{self.operand1} = {self.operand2}"
            case Opcode.LT:
                return f"{self.operand1} = ({self.operand2} < {self.operand3})"
            case Opcode.EQ:
                return f"{self.operand1} = ({self.operand2} == {self.operand3})"
            case Opcode.AND:
                return f"{self.operand1} = {self.operand2} and {self.operand3}"
            case Opcode.OR:
                return f"{self.operand1} = {self.operand2} or {self.operand3}"
            case Opcode.NOT:
                return f"{self.operand1} = not {self.operand2}"
            case Opcode.GOTO:
                return f"goto {self.operand1}"
            case Opcode.IF_TRUE:
                return f"if {self.operand1} goto {self.operand2}"
            case Opcode.IF_FALSE:
                return f"if not {self.operand1} goto {self.operand2}"
            case Opcode.PARAM:
                return f"param {self.operand1}"
            case Opcode.CALL:
                return f"{self.operand1} = call {self.operand2}, {self.operand3}"
            case Opcode.RETURN:
                return f"return {self.operand1}"
            case Opcode.PRINT:
                return f"print {self.operand1}"
            case Opcode.LABEL:
                return f"label {self.operand1}:"
            case _:
                return "Unknown Opcode"


class Method:
    def __init__(self):
        self.param_list: List[Record] = []
        self.var_list: List[Record] = []  # List of parameters and variables together
        self.instruction_list: List[Instruction] = []  # Instructions List
        self.list_: List[Record] = []
        self.var_values: List[int] = []
        self.pc: int = 0  # Program Counter

    def print_instructions(self):
        for i, inst in enumerate(self.instruction_list):
            print(f"{i}  {inst.process_opcode()}")


class ClassFile:
    def __init__(self):
        self.methods: Dict[str, Method] = OrderedDict()
        self.main_method: Method = Method()

    def print(self):
        for name, method in self.methods.items():
            print(f"\nMETHOD {name}")
            # for j, var in enumerate(method.get_list()):
            #     print(f" #{j}={var.get_id()} ", end="")
            print()
            method.print_instructions()
