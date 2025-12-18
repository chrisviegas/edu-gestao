from enum import Enum


class SchoolType(str, Enum):
    FEDERAL = "federal"
    ESTADUAL = "estadual"
    MUNICIPAL = "municipal"
    PRIVADA = "privada"