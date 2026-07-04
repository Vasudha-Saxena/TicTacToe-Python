"""
==================================================
   TIC TAC TOE - GUI EDITION (Tkinter)
   INTERNSHIP PROJECT
==================================================

Description:
    A visually polished, standalone desktop Tic Tac Toe game built
    with Python's Tkinter library.

Features included:
    1. Modern dark-themed aesthetic with a curated color palette
    2. Fixed, perfectly square window (auto-sized, non-stretched)
    3. Custom pill-style clickable buttons for mode selection
       (2 Players / Vs Computer Easy / Vs Computer Unbeatable)
    4. Two AI difficulty levels: Easy (random) & Unbeatable (Minimax)
    5. Dedicated "Score" button that opens a popup with the live
       tally (X wins / O wins / Draws) — also auto-pops after every match
    6. Animated-style hover effects on board cells
    7. Winning line highlight in a distinct color
    8. Status bar showing whose turn it is / round result
    9. "New Round" and "Reset Match" controls
    10. Icons via unicode symbols (✕ / ○)

Author: <Vasudha Saxena>
==================================================
"""

import tkinter as tk
from tkinter import font as tkfont
import random


# ---------------------------------------------------------
# COLOR PALETTE (Aesthetic dark theme with soft accents)
# ---------------------------------------------------------

COLORS = {
    "bg":            "#1b1f3b",   # deep navy background
    "panel":         "#252a4a",   # slightly lighter panel
    "cell":          "#2f345c",   # board cell default
    "cell_hover":    "#3a4074",   # board cell hover
    "cell_win":      "#4ade80",   # winning line highlight (green)
    "text_light":    "#f5f5f7",   # main light text
    "text_muted":    "#9ca3c9",   # secondary muted text
    "x_color":       "#ff6b6b",   # X symbol color (coral red)
    "o_color":       "#4ea8ff",   # O symbol color (sky blue)
    "accent":        "#ffd166",   # accent (buttons / highlights)
    "accent_hover":  "#ffe08a",
    "button_text":   "#1b1f3b",
    "draw_color":    "#b98cff",   # draw highlight (soft purple)
}


# ---------------------------------------------------------
# GAME LOGIC (Board + Minimax AI) - same rules as console version
# ---------------------------------------------------------

class GameLogic:
    WINNING_COMBOS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    def __init__(self):
        self.reset()

    def reset(self):
        self.cells = [None] * 9  # None = empty, 'X' or 'O' otherwise

    def available_moves(self):
        return [i for i, v in enumerate(self.cells) if v is None]

    def make_move(self, idx, symbol):
        self.cells[idx] = symbol

    def undo_move(self, idx):
        self.cells[idx] = None

    def check_winner(self, symbol):
        for combo in self.WINNING_COMBOS:
            if all(self.cells[i] == symbol for i in combo):
                return combo
        return None

    def is_full(self):
        return all(v is not None for v in self.cells)

    def minimax(self, depth, is_max, ai, human):
        if self.check_winner(ai):
            return 10 - depth
        if self.check_winner(human):
            return depth - 10
        if self.is_full():
            return 0

        if is_max:
            best = -float('inf')
            for move in self.available_moves():
                self.make_move(move, ai)
                score = self.minimax(depth + 1, False, ai, human)
                self.undo_move(move)
                best = max(best, score)
            return best
        else:
            best = float('inf')
            for move in self.available_moves():
                self.make_move(move, human)
                score = self.minimax(depth + 1, True, ai, human)
                self.undo_move(move)
                best = min(best, score)
            return best

    def best_move(self, ai, human):
        best_score = -float('inf')
        move_choice = None
        for move in self.available_moves():
            self.make_move(move, ai)
            score = self.minimax(0, False, ai, human)
            self.undo_move(move)
            if score > best_score:
                best_score = score
                move_choice = move
        return move_choice

    def random_move(self):
        return random.choice(self.available_moves())


# ---------------------------------------------------------
# GUI APPLICATION
# ---------------------------------------------------------

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg=COLORS["bg"])

        # Let the window center itself within a square footprint
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # ---- Fonts ----
        self.title_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=11)
        self.cell_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.status_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")
        self.button_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.score_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")

        # ---- Game state ----
        self.logic = GameLogic()
        self.current_symbol = "X"
        self.mode = tk.StringVar(value="pvc_hard")   # pvp | pvc_easy | pvc_hard
        self.game_over = False
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self.buttons = []
        self.mode_buttons = {}

        self._build_layout()
        self._make_window_square()
        self.root.resizable(False, False)

    def _make_window_square(self):
        """Sizes the window into a perfect square that fits all content."""
        self.root.update_idletasks()
        size = max(self.root.winfo_reqwidth(), self.root.winfo_reqheight())
        size = min(size, 700)
        self.root.geometry(f"{size}x{size}")

        # Center the window on the screen
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - size) // 2
        y = (screen_h - size) // 2
        self.root.geometry(f"{size}x{size}+{x}+{y}")

    # -------------------------------------------------
    # LAYOUT
    # -------------------------------------------------
    def _build_layout(self):
        outer = tk.Frame(self.root, bg=COLORS["bg"], padx=15, pady=12)
        outer.grid(row=0, column=0)

        # Title
        tk.Label(
            outer, text="TIC · TAC · TOE", font=self.title_font,
            bg=COLORS["bg"], fg=COLORS["text_light"]
        ).grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Mode selector - custom clickable pill buttons (stacked, full width)
        mode_panel = tk.Frame(outer, bg=COLORS["bg"])
        mode_panel.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        mode_panel.grid_columnconfigure(0, weight=1)

        modes = [
            ("2 Players", "pvp"),
            ("Vs Computer · Easy", "pvc_easy"),
            ("Vs Computer · Unbeatable", "pvc_hard"),
        ]
        for i, (label, value) in enumerate(modes):
            btn = tk.Button(
                mode_panel, text=label, font=self.button_font,
                bd=0, relief="flat", cursor="hand2", pady=5,
                command=lambda v=value: self.set_mode(v)
            )
            btn.grid(row=0, column=i, sticky="ew", padx=4)
            mode_panel.grid_columnconfigure(i, weight=1)
            self.mode_buttons[value] = btn
        self._refresh_mode_buttons()

        # Board frame
        board_frame = tk.Frame(outer, bg=COLORS["bg"])
        board_frame.grid(row=2, column=0, columnspan=3, pady=6)

        for i in range(9):
            btn = tk.Button(
                board_frame, text="", font=self.cell_font,
                width=3, height=1, bg=COLORS["cell"], fg=COLORS["text_light"],
                activebackground=COLORS["cell_hover"], bd=0,
                relief="flat", cursor="hand2",
                command=lambda idx=i: self.on_cell_click(idx)
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, ipady=18)
            btn.bind("<Enter>", lambda e, b=btn: self._on_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self._on_hover(b, False))
            self.buttons.append(btn)

        # Status label
        self.status_label = tk.Label(
            outer, text="Player X's turn", font=self.status_font,
            bg=COLORS["bg"], fg=COLORS["accent"], pady=10
        )
        self.status_label.grid(row=3, column=0, columnspan=3)

        # Control buttons (New Round / Reset / Score)
        controls = tk.Frame(outer, bg=COLORS["bg"])
        controls.grid(row=4, column=0, columnspan=3, pady=(6, 0))

        self._make_action_button(controls, "⟳ New Round", self.new_round).grid(
            row=0, column=0, padx=4
        )
        self._make_action_button(controls, "🏆 Score", lambda: self.show_score_popup()).grid(
            row=0, column=1, padx=4
        )
        self._make_action_button(controls, "✕ Reset Match", self.reset_match).grid(
            row=0, column=2, padx=4
        )

    def set_mode(self, value):
        self.mode.set(value)
        self._refresh_mode_buttons()
        self.new_round()

    def _refresh_mode_buttons(self):
        for value, btn in self.mode_buttons.items():
            if value == self.mode.get():
                btn.config(bg=COLORS["accent"], fg=COLORS["button_text"],
                           activebackground=COLORS["accent_hover"])
            else:
                btn.config(bg=COLORS["panel"], fg=COLORS["text_light"],
                           activebackground=COLORS["cell_hover"])

    def _make_action_button(self, parent, text, command):
        btn = tk.Button(
            parent, text=text, font=self.button_font,
            bg=COLORS["accent"], fg=COLORS["button_text"],
            activebackground=COLORS["accent_hover"], activeforeground=COLORS["button_text"],
            bd=0, relief="flat", padx=10, pady=5, cursor="hand2",
            command=command
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["accent_hover"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLORS["accent"]))
        return btn

    def show_score_popup(self, result_text=None):
        """Opens a small styled popup window showing the current match score."""
        popup = tk.Toplevel(self.root)
        popup.title("Score")
        popup.configure(bg=COLORS["panel"])
        popup.resizable(False, False)
        popup.transient(self.root)

        content = tk.Frame(popup, bg=COLORS["panel"], padx=28, pady=22)
        content.pack()

        if result_text:
            tk.Label(
                content, text=result_text, font=self.status_font,
                bg=COLORS["panel"], fg=COLORS["accent"], wraplength=220,
                justify="center"
            ).pack(pady=(0, 14))

        tk.Label(
            content, text="🏆 MATCH SCORE", font=self.button_font,
            bg=COLORS["panel"], fg=COLORS["text_muted"]
        ).pack(pady=(0, 10))

        tk.Label(
            content, text=f"Player X   —   {self.scores['X']}",
            font=self.score_font, bg=COLORS["panel"], fg=COLORS["x_color"]
        ).pack(pady=3)
        tk.Label(
            content, text=f"Player O   —   {self.scores['O']}",
            font=self.score_font, bg=COLORS["panel"], fg=COLORS["o_color"]
        ).pack(pady=3)
        tk.Label(
            content, text=f"Draws        —   {self.scores['Draws']}",
            font=self.score_font, bg=COLORS["panel"], fg=COLORS["draw_color"]
        ).pack(pady=3)

        self._make_action_button(content, "Close", popup.destroy).pack(pady=(16, 0))

        # Center popup over the main window
        popup.update_idletasks()
        w, h = popup.winfo_reqwidth(), popup.winfo_reqheight()
        x = self.root.winfo_x() + (self.root.winfo_width() - w) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - h) // 2
        popup.geometry(f"{w}x{h}+{x}+{y}")
        popup.grab_set()

    def _on_hover(self, btn, entering):
        # Only apply hover effect to empty, still-playable cells
        idx = self.buttons.index(btn)
        if self.logic.cells[idx] is None and not self.game_over:
            btn.config(bg=COLORS["cell_hover"] if entering else COLORS["cell"])

    # -------------------------------------------------
    # GAME FLOW
    # -------------------------------------------------
    def on_cell_click(self, idx):
        if self.game_over or self.logic.cells[idx] is not None:
            return

        # Human move
        self._place(idx, self.current_symbol)
        if self._check_end_conditions():
            return

        self._switch_turn()

        # If playing vs computer and it's now O's turn, let AI respond
        if self.mode.get() in ("pvc_easy", "pvc_hard") and self.current_symbol == "O":
            self.root.after(400, self._computer_move)

    def _computer_move(self):
        if self.game_over:
            return
        if self.mode.get() == "pvc_easy":
            move = self.logic.random_move()
        else:
            move = self.logic.best_move(ai="O", human="X")

        self._place(move, "O")
        if self._check_end_conditions():
            return
        self._switch_turn()

    def _place(self, idx, symbol):
        self.logic.make_move(idx, symbol)
        color = COLORS["x_color"] if symbol == "X" else COLORS["o_color"]
        display_symbol = "✕" if symbol == "X" else "○"
        self.buttons[idx].config(
            text=display_symbol, fg=color, bg=COLORS["cell"],
            disabledforeground=color
        )

    def _switch_turn(self):
        self.current_symbol = "O" if self.current_symbol == "X" else "X"
        self.status_label.config(
            text=f"Player {self.current_symbol}'s turn",
            fg=COLORS["o_color"] if self.current_symbol == "O" else COLORS["x_color"]
        )

    def _check_end_conditions(self):
        win_combo = self.logic.check_winner(self.current_symbol)
        if win_combo:
            self._end_round(winner=self.current_symbol, combo=win_combo)
            return True

        if self.logic.is_full():
            self._end_round(winner=None, combo=None)
            return True

        return False

    def _end_round(self, winner, combo):
        self.game_over = True

        if winner:
            for idx in combo:
                self.buttons[idx].config(bg=COLORS["cell_win"])
            self.scores[winner] += 1
            result_text = f"🎉 Player {winner} wins this round!"
            self.status_label.config(text=result_text, fg=COLORS["cell_win"])
        else:
            self.scores["Draws"] += 1
            result_text = "🤝 It's a draw!"
            self.status_label.config(text=result_text, fg=COLORS["draw_color"])

        self._disable_board()

        # Automatically display the updated score after every match
        self.root.after(350, lambda: self.show_score_popup(result_text))

    def _disable_board(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def new_round(self):
        """Clears the board but keeps the running score."""
        self.logic.reset()
        self.current_symbol = "X"
        self.game_over = False
        for btn in self.buttons:
            btn.config(
                text="", bg=COLORS["cell"], state="normal",
                fg=COLORS["text_light"]
            )
        self.status_label.config(text="Player X's turn", fg=COLORS["accent"])

    def reset_match(self):
        """Resets both the board and the scoreboard."""
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self.new_round()


# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------

def main():
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()