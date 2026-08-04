"""
MADED WITH CLAUDE! NOT MY OWN CODE
Modern GUI Calculator
----------------------
A clean, professional-looking calculator built with Python's built-in
tkinter library (no external dependencies required).

Features:
- Basic operations: add, subtract, multiply, divide
- Extras: percentage, square root, sign toggle (+/-), clear, backspace
- Keyboard support (numbers, + - * / . Enter Backspace Esc)
- Modern flat dark theme with hover effects
- Error handling (e.g. divide by zero, invalid expressions)
- Expression preview (shows the running calculation above the result)
- Optional Scientific mode (toggle button): sin/cos/tan, log/ln, x^y,
  x^2, x^3, 1/x, n!, pi, e, parentheses, and a DEG/RAD switch — the
  basic calculator underneath is unchanged and works exactly as before

Run with:
    python calculator.py
"""

import re
import math
import tkinter as tk
from tkinter import font


# ---------------------------------------------------------------------------
# Color / style constants (modern dark theme)
# ---------------------------------------------------------------------------
BG_MAIN = "#1e1f26"
BG_DISPLAY = "#1e1f26"
COLOR_EXPR = "#9a9bb0"
COLOR_RESULT = "#ffffff"

BTN_NUM_BG = "#2b2d3a"
BTN_NUM_HOVER = "#383b4d"
BTN_NUM_FG = "#ffffff"

BTN_OP_BG = "#ff9f43"
BTN_OP_HOVER = "#ffb266"
BTN_OP_FG = "#1e1f26"

BTN_FUNC_BG = "#3a3d52"
BTN_FUNC_HOVER = "#4a4e68"
BTN_FUNC_FG = "#ffffff"

BTN_EQ_BG = "#4cd964"
BTN_EQ_HOVER = "#6ee582"
BTN_EQ_FG = "#1e1f26"

BTN_SCI_BG = "#2b2f4a"
BTN_SCI_HOVER = "#3a4066"
BTN_SCI_FG = "#c9cdff"

BTN_MODE_BG = "#3a3d52"
BTN_MODE_HOVER = "#4a4e68"
BTN_MODE_ACTIVE_BG = "#7c5cff"
BTN_MODE_ACTIVE_HOVER = "#9478ff"
BTN_MODE_FG = "#ffffff"


class RoundedButton(tk.Canvas):
    """A flat, modern-looking button drawn on a Canvas so we get rounded
    corners and smooth hover effects (plain tk.Button looks dated)."""

    def __init__(self, parent, text, command, bg, hover_bg, fg,
                 font_obj, width=70, height=60, radius=16, **kwargs):
        super().__init__(parent, width=width, height=height,
                          bg=parent["bg"], highlightthickness=0, **kwargs)
        self.command = command
        self.bg = bg
        self.hover_bg = hover_bg
        self.fg = fg
        self.font_obj = font_obj
        self.width = width
        self.height = height
        self.radius = radius
        self.text = text

        self._draw(bg)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
            x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
            x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _draw(self, fill_color):
        self.delete("all")
        self._round_rect(2, 2, self.width - 2, self.height - 2,
                          self.radius, fill=fill_color, outline="")
        self.create_text(self.width / 2, self.height / 2, text=self.text,
                          fill=self.fg, font=self.font_obj)

    def _on_enter(self, _event):
        self._draw(self.hover_bg)

    def _on_leave(self, _event):
        self._draw(self.bg)

    def _on_click(self, _event):
        self._draw(self.hover_bg)

    def _on_release(self, _event):
        self._draw(self.hover_bg)
        if self.command:
            self.command()
        self.after(120, lambda: self._draw(self.bg))

    def update_text(self, new_text):
        self.text = new_text
        self._draw(self.bg)

    def set_colors(self, bg, hover_bg, fg=None):
        self.bg = bg
        self.hover_bg = hover_bg
        if fg is not None:
            self.fg = fg
        self._draw(self.bg)


class Calculator(tk.Tk):
    MAX_DIGITS = 14  # keeps the display readable and avoids overflow bugs

    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.configure(bg=BG_MAIN)
        self.resizable(False, False)

        # Internal state
        self.expression = ""      # e.g. "12+7"
        self.reset_next_input = False
        self.scientific_mode = False
        self.angle_mode = "DEG"   # "DEG" or "RAD" — only affects sin/cos/tan

        # Fonts
        self.expr_font = font.Font(family="Segoe UI", size=14)
        self.result_font = font.Font(family="Segoe UI", size=36, weight="bold")
        self.btn_font = font.Font(family="Segoe UI", size=16)
        self.btn_font_small = font.Font(family="Segoe UI", size=14)
        self.btn_font_tiny = font.Font(family="Segoe UI", size=12)

        self._build_display()
        self._build_mode_toggle()
        self._build_buttons()
        self._build_sci_panel()
        self._bind_keys()

        self.update_display()

    # ------------------------------------------------------------------
    # Scientific mode toggle
    # ------------------------------------------------------------------
    def _build_mode_toggle(self):
        bar = tk.Frame(self, bg=BG_MAIN, padx=16, pady=(0, 4))
        bar.pack(fill="x")

        self.mode_btn = RoundedButton(
            bar, text="Scientific mode: OFF", command=self.toggle_scientific_mode,
            bg=BTN_MODE_BG, hover_bg=BTN_MODE_HOVER, fg=BTN_MODE_FG,
            font_obj=self.btn_font_tiny, width=248, height=36, radius=12,
        )
        self.mode_btn.pack(side="right")

    def toggle_scientific_mode(self):
        self.scientific_mode = not self.scientific_mode
        if self.scientific_mode:
            self.sci_frame.pack(fill="x")
            self.mode_btn.update_text("Scientific mode: ON")
            self.mode_btn.set_colors(BTN_MODE_ACTIVE_BG, BTN_MODE_ACTIVE_HOVER)
        else:
            self.sci_frame.pack_forget()
            self.mode_btn.update_text("Scientific mode: OFF")
            self.mode_btn.set_colors(BTN_MODE_BG, BTN_MODE_HOVER)
        self.update_idletasks()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_display(self):
        display_frame = tk.Frame(self, bg=BG_DISPLAY, padx=20, pady=20)
        display_frame.pack(fill="x")

        self.expr_label = tk.Label(
            display_frame, text="", anchor="e",
            bg=BG_DISPLAY, fg=COLOR_EXPR, font=self.expr_font
        )
        self.expr_label.pack(fill="x")

        self.result_label = tk.Label(
            display_frame, text="0", anchor="e",
            bg=BG_DISPLAY, fg=COLOR_RESULT, font=self.result_font
        )
        self.result_label.pack(fill="x")

    def _build_buttons(self):
        pad_frame = tk.Frame(self, bg=BG_MAIN, padx=16, pady=16)
        pad_frame.pack()

        # (label, action, style)
        rows = [
            [("C", self.clear_all, "func"), ("⌫", self.backspace, "func"),
             ("%", lambda: self.add_operator("%"), "func"), ("÷", lambda: self.add_operator("/"), "op")],
            [("7", lambda: self.add_digit("7"), "num"), ("8", lambda: self.add_digit("8"), "num"),
             ("9", lambda: self.add_digit("9"), "num"), ("×", lambda: self.add_operator("*"), "op")],
            [("4", lambda: self.add_digit("4"), "num"), ("5", lambda: self.add_digit("5"), "num"),
             ("6", lambda: self.add_digit("6"), "num"), ("−", lambda: self.add_operator("-"), "op")],
            [("1", lambda: self.add_digit("1"), "num"), ("2", lambda: self.add_digit("2"), "num"),
             ("3", lambda: self.add_digit("3"), "num"), ("+", lambda: self.add_operator("+"), "op")],
            [("√", self.square_root, "func"), ("0", lambda: self.add_digit("0"), "num"),
             (".", self.add_decimal, "num"), ("=", self.calculate, "eq")],
        ]

        style_map = {
            "num": (BTN_NUM_BG, BTN_NUM_HOVER, BTN_NUM_FG, self.btn_font),
            "op": (BTN_OP_BG, BTN_OP_HOVER, BTN_OP_FG, self.btn_font),
            "func": (BTN_FUNC_BG, BTN_FUNC_HOVER, BTN_FUNC_FG, self.btn_font_small),
            "eq": (BTN_EQ_BG, BTN_EQ_HOVER, BTN_EQ_FG, self.btn_font),
        }

        for r, row in enumerate(rows):
            for c, (label, action, style) in enumerate(row):
                bg, hover, fg, fnt = style_map[style]
                btn = RoundedButton(
                    pad_frame, text=label, command=action,
                    bg=bg, hover_bg=hover, fg=fg, font_obj=fnt,
                    width=76, height=64,
                )
                btn.grid(row=r, column=c, padx=6, pady=6)

    def _build_sci_panel(self):
        """Extra panel of scientific-mode buttons. Hidden by default; the
        basic calculator above is fully functional without it."""
        self.sci_frame = tk.Frame(self, bg=BG_MAIN, padx=16, pady=(0, 16))
        # Not packed yet — toggle_scientific_mode() shows/hides it.

        rows = [
            [("sin", lambda: self.apply_function("sin")),
             ("cos", lambda: self.apply_function("cos")),
             ("tan", lambda: self.apply_function("tan")),
             ("π", lambda: self.insert_constant("pi"))],
            [("log", lambda: self.apply_function("log")),
             ("ln", lambda: self.apply_function("ln")),
             ("e", lambda: self.insert_constant("e")),
             ("xʸ", self.add_power)],
            [("x²", lambda: self.apply_function("sqr")),
             ("x³", lambda: self.apply_function("cube")),
             ("1/x", lambda: self.apply_function("inv")),
             ("n!", lambda: self.apply_function("fact"))],
            [("(", lambda: self.add_paren("(")),
             (")", lambda: self.add_paren(")")),
             (self.angle_mode, self.toggle_angle_mode),
             ("√", self.square_root)],
        ]

        for r, row in enumerate(rows):
            for c, (label, action) in enumerate(row):
                btn = RoundedButton(
                    self.sci_frame, text=label, command=action,
                    bg=BTN_SCI_BG, hover_bg=BTN_SCI_HOVER, fg=BTN_SCI_FG,
                    font_obj=self.btn_font_small, width=76, height=52, radius=12,
                )
                btn.grid(row=r, column=c, padx=6, pady=6)
                if label in ("DEG", "RAD"):
                    self.angle_btn = btn

    def _bind_keys(self):
        for digit in "0123456789":
            self.bind(digit, lambda e, d=digit: self.add_digit(d))
        self.bind(".", lambda e: self.add_decimal())
        self.bind("+", lambda e: self.add_operator("+"))
        self.bind("-", lambda e: self.add_operator("-"))
        self.bind("*", lambda e: self.add_operator("*"))
        self.bind("/", lambda e: self.add_operator("/"))
        self.bind("%", lambda e: self.add_operator("%"))
        self.bind("<Return>", lambda e: self.calculate())
        self.bind("<KP_Enter>", lambda e: self.calculate())
        self.bind("<BackSpace>", lambda e: self.backspace())
        self.bind("<Escape>", lambda e: self.clear_all())

    # ------------------------------------------------------------------
    # Calculator logic
    # ------------------------------------------------------------------
    def update_display(self, result=None):
        self.expr_label.config(text=self._pretty(self.expression))
        if result is not None:
            self.result_label.config(text=result)
        else:
            # Live preview: show last number being typed, or 0
            tail = self._current_number_segment()
            self.result_label.config(text=tail if tail else "0")

    @staticmethod
    def _pretty(expr):
        return (expr.replace("*", " × ")
                    .replace("/", " ÷ ")
                    .replace("-", " − ")
                    .replace("+", " + "))

    def _current_number_segment(self):
        """Return the number currently being typed (after the last operator
        or opening/closing parenthesis)."""
        parts = re.split(r"[+\-*/%()]", self.expression)
        return parts[-1] if parts else ""

    def add_digit(self, digit):
        if self.reset_next_input:
            self.expression = ""
            self.reset_next_input = False
        if len(self._current_number_segment()) >= self.MAX_DIGITS:
            return
        # Avoid multiple leading zeros like "00"
        if self._current_number_segment() == "0" and digit == "0":
            return
        if self._current_number_segment() == "0" and digit != "0":
            self.expression = self.expression[:-1] + digit
        else:
            self.expression += digit
        self.update_display()

    def add_decimal(self):
        if self.reset_next_input:
            self.expression = ""
            self.reset_next_input = False
        segment = self._current_number_segment()
        if segment == "":
            self.expression += "0."
        elif "." not in segment:
            self.expression += "."
        self.update_display()

    def add_operator(self, op):
        if not self.expression:
            if op == "-":
                self.expression = "-"
                self.update_display()
            return
        self.reset_next_input = False
        last_char = self.expression[-1]
        if last_char in "+-*/%":
            self.expression = self.expression[:-1] + op
        else:
            self.expression += op
        self.update_display()

    def backspace(self):
        if self.reset_next_input:
            self.clear_all()
            return
        self.expression = self.expression[:-1]
        self.update_display()

    def clear_all(self):
        self.expression = ""
        self.reset_next_input = False
        self.update_display(result="0")

    def square_root(self):
        segment = self._current_number_segment()
        try:
            value = float(segment) if segment not in ("", "-") else 0.0
            if value < 0:
                raise ValueError("negative")
            root = value ** 0.5
            new_segment = self._format_number(root)
            self.expression = self.expression[: len(self.expression) - len(segment)] + new_segment
            self.update_display()
        except ValueError:
            self.update_display(result="Error")
            self.expression = ""

    @staticmethod
    def _format_number(value):
        if value == int(value) and abs(value) < 1e15:
            return str(int(value))
        return f"{value:.10g}"

    def _replace_current_segment(self, new_text):
        """Swap out the number currently being typed for new_text, keeping
        whatever operators/parentheses came before it."""
        segment = self._current_number_segment()
        if segment:
            self.expression = self.expression[: len(self.expression) - len(segment)] + new_text
        else:
            self.expression += new_text
        self.reset_next_input = False
        self.update_display()

    # -- Scientific-mode operations ------------------------------------
    def apply_function(self, kind):
        """Apply a unary scientific function to the number currently being
        typed (e.g. sin, log, x², 1/x, n!)."""
        segment = self._current_number_segment()
        try:
            value = float(segment) if segment not in ("", "-") else 0.0

            if kind in ("sin", "cos", "tan"):
                angle = math.radians(value) if self.angle_mode == "DEG" else value
                result = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[kind](angle)
            elif kind == "log":
                if value <= 0:
                    raise ValueError("log of non-positive number")
                result = math.log10(value)
            elif kind == "ln":
                if value <= 0:
                    raise ValueError("ln of non-positive number")
                result = math.log(value)
            elif kind == "sqr":
                result = value ** 2
            elif kind == "cube":
                result = value ** 3
            elif kind == "inv":
                if value == 0:
                    raise ZeroDivisionError
                result = 1 / value
            elif kind == "fact":
                if value < 0 or value != int(value):
                    raise ValueError("factorial needs a non-negative integer")
                result = math.factorial(int(value))
            else:
                return

            self._replace_current_segment(self._format_number(result))
        except ZeroDivisionError:
            self.update_display(result="Cannot divide by 0")
            self.expression = ""
            self.reset_next_input = True
        except (ValueError, OverflowError):
            self.update_display(result="Error")
            self.expression = ""
            self.reset_next_input = True

    def insert_constant(self, name):
        if self.reset_next_input:
            self.expression = ""
            self.reset_next_input = False
        value = math.pi if name == "pi" else math.e
        formatted = self._format_number(value)
        segment = self._current_number_segment()
        if segment:
            # A number was already being typed — insert as multiplication,
            # e.g. "2" then π becomes "2*3.141592654".
            self.expression += "*" + formatted
        else:
            self.expression += formatted
        self.update_display()

    def add_power(self):
        """Append the ** (power) operator, replacing any trailing operator."""
        if not self.expression:
            return
        self.reset_next_input = False
        stripped = self.expression
        for op in ("**", "+", "-", "*", "/", "%"):
            if stripped.endswith(op):
                stripped = stripped[: -len(op)]
                break
        self.expression = stripped + "**"
        self.update_display()

    def add_paren(self, paren):
        if self.reset_next_input:
            self.expression = ""
            self.reset_next_input = False
        self.expression += paren
        self.update_display()

    def toggle_angle_mode(self):
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        self.angle_btn.update_text(self.angle_mode)

    def calculate(self):
        if not self.expression:
            return
        expr = self.expression.rstrip("+-*/%")
        # Convert percentage: turn "a%" into "(a/100)" style handling.
        try:
            safe_expr = self._convert_percent(expr)
            # Only allow safe characters before eval
            if not all(ch in "0123456789.+-*/() " for ch in safe_expr):
                raise ValueError("invalid characters")
            result = eval(safe_expr, {"__builtins__": {}}, {})
            if isinstance(result, float) and (result != result or result in (float("inf"), float("-inf"))):
                raise ZeroDivisionError
            formatted = self._format_number(result)
            self.expression = formatted
            self.reset_next_input = True
            self.update_display(result=formatted)
        except ZeroDivisionError:
            self.update_display(result="Cannot divide by 0")
            self.expression = ""
            self.reset_next_input = True
        except Exception:
            self.update_display(result="Error")
            self.expression = ""
            self.reset_next_input = True

    @staticmethod
    def _convert_percent(expr):
        """Turn each standalone number followed by % into (number/100)."""
        return re.sub(r"(\d+(\.\d+)?)%", r"(\1/100)", expr)


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
