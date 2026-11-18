import ast
import math
import operator

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex


Window.size = (360, 640)
Window.clearcolor = get_color_from_hex("#151515")


# آلة حساب آمنة
def calculate(expression):
    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def solve(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            left = solve(node.left)
            right = solve(node.right)
            return operations[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in operations:
            return operations[type(node.op)](solve(node.operand))

        raise ValueError("عملية غير مسموحة")

    tree = ast.parse(expression, mode="eval")
    result = solve(tree.body)

    if not math.isfinite(result) or abs(result) > 1e100:
        raise ValueError("النتيجة خارج النطاق")

    return result


class OmarCalculator(App):

    def build(self):
        self.expression = ""

        root = BoxLayout(
            orientation="vertical",
            padding=12,
            spacing=10
        )

        # عنوان التطبيق
        title = Label(
            text="OMAR CALCULATOR",
            font_size=20,
            color=get_color_from_hex("#FF9800"),
            size_hint_y=0.10
        )
        root.add_widget(title)

        # شاشة الحاسبة
        self.display = Label(
            text="0",
            font_size=42,
            halign="right",
            valign="middle",
            color=(1, 1, 1, 1),
            size_hint_y=0.25
        )
        self.display.bind(size=self.update_text_size)
        root.add_widget(self.display)

        # الأزرار
        grid = GridLayout(
            cols=4,
            spacing=8,
            padding=5
        )

        buttons = [
            "AC", "DEL", "%", "÷",
            "7", "8", "9", "×",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "√", "0", ".", "="
        ]

        for item in buttons:
            color = "#333333"

            if item in ["÷", "×", "-", "+", "="]:
                color = "#FF9800"
            elif item in ["AC", "DEL", "%", "√"]:
                color = "#555555"

            btn = Button(
                text=item,
                font_size=25,
                background_normal="",
                background_color=get_color_from_hex(color),
                color=(1, 1, 1, 1)
            )

            btn.bind(on_press=lambda instance, value=item:
                     self.button_click(value))

            grid.add_widget(btn)

        root.add_widget(grid)
        return root

    def update_text_size(self, instance, size):
        instance.text_size = size

    def button_click(self, value):

        if value == "AC":
            self.expression = ""
            self.display.text = "0"

        elif value == "DEL":
            self.expression = self.expression[:-1]
            self.display.text = self.expression or "0"

        elif value == "=":
            try:
                result = calculate(self.expression)
                self.expression = str(result)
                self.display.text = self.expression
            except Exception:
                self.display.text = "خطأ"
                self.expression = ""

        elif value == "√":
            try:
                result = math.sqrt(calculate(self.expression))
                self.expression = str(result)
                self.display.text = self.expression
            except Exception:
                self.display.text = "خطأ"
                self.expression = ""

        else:
            symbols = {
                "÷": "/",
                "×": "*"
            }

            self.expression += symbols.get(value, value)
            self.display.text = self.expression


if __name__ == "__main__":
    OmarCalculator().run()