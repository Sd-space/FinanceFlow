from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    analyst = "analyst"
    viewer = "viewer"


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"