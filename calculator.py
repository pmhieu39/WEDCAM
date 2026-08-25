import ast
import operator

class SafeCalculator:
    def __init__(self):
        # Định nghĩa các phép toán được phép
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg
        }

    def evaluate(self, expression_str):
        if not expression_str:
            return "Empty"
        try:
            # Parse biểu thức thành cây cú pháp (AST) để an toàn
            node = ast.parse(expression_str, mode='eval').body
            result = self._eval_node(node)
            # Làm tròn 2 chữ số thập phân nếu là số thực
            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            elif isinstance(result, float):
                return str(round(result, 2))
            return str(result)
        except ZeroDivisionError:
            return "Div by Zero"
        except Exception:
            return "Invalid"

    def _eval_node(self, node):
        if isinstance(node, ast.Num): # Dành cho Python cũ
            return node.n
        elif isinstance(node, ast.Constant): # Python 3.8+
            return node.value
        elif isinstance(node, ast.BinOp): 
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return self.operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            return self.operators[type(node.op)](operand)
        else:
            raise TypeError("Unsupported operator")