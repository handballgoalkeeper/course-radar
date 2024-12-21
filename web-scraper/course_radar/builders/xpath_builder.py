from enum import Enum

class XPathBuilder:
    RECURSIVE_SEPARATOR = '//'
    SINGLE_DEPTH_SEPARATOR = '/'
    RELATIVE_TO_NODE_START_SEPARATOR = '.'
    CONSTRAINTS_OPENING ='['
    CONSTRAINTS_CLOSING =']'

    class Element(Enum):
        DIV = 'div'
        TABLE = 'table'
        MAIN = 'main'
        BODY = 'body'
        SECTION = 'section'
        H4 = 'h4'
        A = 'a'
        P = 'p'
        ASIDE = 'aside'
        NAV = 'nav'
        TBODY = 'tbody'
        TR = 'tr'
        TD = 'td'
        TH = 'th'
        SPAN = 'span'

    class Attribute(Enum):
        HREF = 'href'

    class Constraint:
        def __init__(self, constraint_part: str, logical_operator: str = 'and'):
            self.constraint_part = constraint_part
            self.logical_operator = logical_operator

    def __init__(self, start_relative_to_current_node = False):
        self.start_relative_to_current_node = start_relative_to_current_node
        self.parts = []

        if start_relative_to_current_node:
            self.parts.append(XPathBuilder.RELATIVE_TO_NODE_START_SEPARATOR)

    def with_recursive(self, element: Element, constraints: list[Constraint] = None) -> 'XPathBuilder':

        if constraints is None or len(constraints) == 0:
            self.parts.append(f"{ XPathBuilder.RECURSIVE_SEPARATOR }{element.value}")
            return self

        if constraints is not None:
            part = f"{ XPathBuilder.RECURSIVE_SEPARATOR }{ element.value }"

            part += XPathBuilder.CONSTRAINTS_OPENING
            for i, constraint in enumerate(constraints):
                if i == len(constraints) - 1:
                    part += f"{ constraint.constraint_part }{ XPathBuilder.CONSTRAINTS_CLOSING }"
                else:
                    part += f"{ constraint.constraint_part } { constraint.logical_operator } "

            self.parts.append(part)
            return self

    def single_depth(self, element: Element) -> 'XPathBuilder':
        self.parts.append(f"{ XPathBuilder.SINGLE_DEPTH_SEPARATOR }{ element.value }")
        return self

    def inner_text(self, recursive: bool = False) -> 'XPathBuilder':
        separator = XPathBuilder.RECURSIVE_SEPARATOR if recursive else XPathBuilder.SINGLE_DEPTH_SEPARATOR

        self.parts.append(f"{ separator }text()")
        return self

    def get_attribute_content(self, attribute: 'XPathBuilder.Attribute' , recursive: bool = False) -> 'XPathBuilder':
        separator = XPathBuilder.RECURSIVE_SEPARATOR if recursive else XPathBuilder.SINGLE_DEPTH_SEPARATOR

        self.parts.append(f"{ separator}@{ attribute.value }")
        return self



    def build(self) -> str:
        return "".join(self.parts)

    def __str__(self):
        return self.build()