import flet as ft
import math


class Calculator:
    def __init__(self):
        self.result = ft.Text("0", size=40, color=ft.Colors.WHITE)
        self.operator = ""
        self.first_operand = None
        self.new_operand = True
        self.memory = 0

    def view(self):
        return ft.Container(
            width=400,
            padding=20,
            bgcolor=ft.Colors.BLACK,   # ← 背景黒
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row([self.result], alignment="end"),

                    # --- Memory buttons ---
                    ft.Row([
                        self.btn("MC", color=ft.Colors.BLACK, bg=ft.Colors.BLUE_GREY_200),
                        self.btn("MR", color=ft.Colors.BLACK, bg=ft.Colors.BLUE_GREY_200),
                        self.btn("M+", color=ft.Colors.BLACK, bg=ft.Colors.BLUE_GREY_200),
                        self.btn("M-", color=ft.Colors.BLACK, bg=ft.Colors.BLUE_GREY_200),
                    ]),

                    # --- Scientific buttons ---
                    ft.Row([
                        self.btn("sin", bg=ft.Colors.BLUE_GREY_300, color=ft.Colors.BLACK),
                        self.btn("cos", bg=ft.Colors.BLUE_GREY_300, color=ft.Colors.BLACK),
                        self.btn("tan", bg=ft.Colors.BLUE_GREY_300, color=ft.Colors.BLACK),
                        self.btn("ln", bg=ft.Colors.BLUE_GREY_300, color=ft.Colors.BLACK),
                    ]),
                    ft.Row([
                        self.btn("log", bg=ft.Colors.BLUE_GREY_300, color=ft.Colors.BLACK),
                        self.btn("x!", bg=ft.Colors.BLUE_GREY_300, color=ft.Colors.BLACK),
                        self.btn("10^x", bg=ft.Colors.BLUE_GREY_300, color=ft.Colors.BLACK),
                        self.btn("√", bg=ft.Colors.BLUE_GREY_300, color=ft.Colors.BLACK),
                    ]),

                    # --- Standard calculator buttons ---
                    ft.Row([
                        self.btn("7"), self.btn("8"), self.btn("9"),
                        self.btn("/", bg=ft.Colors.ORANGE, color=ft.Colors.WHITE),
                    ]),
                    ft.Row([
                        self.btn("4"), self.btn("5"), self.btn("6"),
                        self.btn("*", bg=ft.Colors.ORANGE, color=ft.Colors.WHITE),
                    ]),
                    ft.Row([
                        self.btn("1"), self.btn("2"), self.btn("3"),
                        self.btn("-", bg=ft.Colors.ORANGE, color=ft.Colors.WHITE),
                    ]),
                    ft.Row([
                        self.btn("0", expand=2),
                        self.btn("."),
                        self.btn("+", bg=ft.Colors.ORANGE, color=ft.Colors.WHITE),
                    ]),
                    ft.Row([
                        self.btn("=", expand=4, bg=ft.Colors.ORANGE, color=ft.Colors.WHITE),
                    ]),
                ]
            ),
        )

    # ===== ボタン作成 =====
    def btn(self, text, expand=1, bg=ft.Colors.WHITE24, color=ft.Colors.WHITE):
        return ft.ElevatedButton(
            text,
            expand=expand,
            data=text,
            bgcolor=bg,
            color=color,
            on_click=self.on_click
        )

    # ===== ボタンが押されたときの処理 =====
    def on_click(self, e):
        data = e.control.data

        # ---- Memory ----
        if data == "MC":
            self.memory = 0
        elif data == "MR":
            self.result.value = str(self.format(self.memory))
            self.new_operand = True
        elif data == "M+":
            self.memory += float(self.result.value)
            self.new_operand = True
        elif data == "M-":
            self.memory -= float(self.result.value)
            self.new_operand = True

        # ---- Numbers / Decimal ----
        elif data.isdigit() or data == ".":
            if self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                if data == "." and "." in self.result.value:
                    pass
                else:
                    self.result.value += data

        # ---- Scientific: sin, cos, tan ----
        elif data in ["sin", "cos", "tan"]:
            x = float(self.result.value)
            rad = math.radians(x)

            if data == "sin":
                v = math.sin(rad)
            elif data == "cos":
                v = math.cos(rad)
            elif data == "tan":
                v = math.tan(rad)

            self.result.value = str(v)
            self.new_operand = True

        # ---- ln ----
        elif data == "ln":
            x = float(self.result.value)
            self.result.value = "Error" if x <= 0 else str(math.log(x))
            self.new_operand = True

        # ---- log10 ----
        elif data == "log":
            x = float(self.result.value)
            self.result.value = "Error" if x <= 0 else str(math.log10(x))
            self.new_operand = True

        # ---- factorial ----
        elif data == "x!":
            x = float(self.result.value)
            if x < 0 or not x.is_integer():
                self.result.value = "Error"
            else:
                self.result.value = str(math.factorial(int(x)))
            self.new_operand = True

        # ---- 10^x ----
        elif data == "10^x":
            x = float(self.result.value)
            self.result.value = str(10 ** x)
            self.new_operand = True

        # ---- sqrt ----
        elif data == "√":
            x = float(self.result.value)
            self.result.value = "Error" if x < 0 else str(math.sqrt(x))
            self.new_operand = True

        # ---- Operators ----
        elif data in ["+", "-", "*", "/"]:
            self.first_operand = float(self.result.value)
            self.operator = data
            self.new_operand = True

        # ---- Equal ----
        elif data == "=":
            if self.operator:
                second = float(self.result.value)

                if self.operator == "+":
                    v = self.first_operand + second
                elif self.operator == "-":
                    v = self.first_operand - second
                elif self.operator == "*":
                    v = self.first_operand * second
                elif self.operator == "/":
                    v = "Error" if second == 0 else self.first_operand / second

                self.result.value = str(v)
            self.new_operand = True

        self.result.update()

    # ---- Format number ----
    def format(self, n):
        return int(n) if n == int(n) else n


def main(page: ft.Page):
    page.title = "Scientific Calculator"
    page.bgcolor = ft.Colors.BLACK
    calc = Calculator()
    page.add(calc.view())


ft.app(target=main)
