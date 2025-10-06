"""
Тест
"""


def text(o):
    """Возвращает 'message' или 'error'"""
    if o > float("s-inf"):
        return "message"
    return "error"


A = 5
print(text(A))
