import tkinter as tk
from tkinter import messagebox
import random

class StickGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stick Game")

        # Set default window size
        window_width = 600
        window_height = 600
        self.root.geometry(f"{window_width}x{window_height}")

        # Center the window on screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Initial game setup UI
        self.setup_frame = tk.Frame(root)
        tk.Label(self.setup_frame, text="Total number of sticks:", font=("Helvetica", 20)).pack()
        self.total_entry = tk.Entry(self.setup_frame, font=("Helvetica", 16), width=10)
        self.total_entry.pack()

        tk.Label(self.setup_frame, text="Max sticks per turn:", font=("Helvetica", 20)).pack()
        self.max_entry = tk.Entry(self.setup_frame, font=("Helvetica", 16), width=10)
        self.max_entry.pack()

        self.start_button = tk.Button(self.setup_frame, text="Start Game", font=("Helvetica", 16), width=10, height=2, command=self.start_game)
        self.start_button.pack()

        self.setup_frame.pack()

        # Gameplay UI
        self.game_frame = tk.Frame(root)

        self.status_label = tk.Label(self.game_frame, text="", font=("Helvetica", 20))
        self.status_label.pack()

        self.input_label = tk.Label(self.game_frame, text="Your turn: Take how many sticks?", font=("Helvetica", 20))
        self.input_label.pack()

        self.user_input = tk.Entry(self.game_frame, font=("Helvetica", 16), width=15)
        self.user_input.pack()

        self.take_button = tk.Button(self.game_frame, text="Take", font=("Helvetica", 16), width=10, height=2, command=self.user_move)
        self.take_button.pack()

        self.back_button = tk.Button(self.game_frame, text="Restart", font=("Helvetica", 16), width=10, height=2, command=self.restart)
        self.back_button.pack(pady=10)

    def start_game(self):
        try:
            self.total_sticks = int(self.total_entry.get())
            self.max_per_turn = int(self.max_entry.get())

            if self.total_sticks <= 0 or self.max_per_turn <= 0:
                raise ValueError
            self.allowing = list(range(1,self.max_per_turn + 1))
            
            
            self.remaining_sticks = self.total_sticks
            self.setup_frame.pack_forget()
            self.game_frame.pack()
            self.update_status(f"Game started with {self.total_sticks} sticks.\nBot will go first...")
        
            # Let bot make the first move after a short delay so UI updates
            self.root.after(1000, self.bot_move)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter positive integers.")

    def update_status(self, message):
        self.status_label.config(text=message)

    def user_move(self):
        try:
            taken = int(self.user_input.get())
            if taken <= 0 or taken > self.max_per_turn or taken > self.remaining_sticks:
                raise ValueError

            self.remaining_sticks -= taken
            if self.remaining_sticks == 0:
                self.update_status("You took the last stick. You win!")
                self.take_button.config(state="disabled")
                return

            self.update_status(f"You took {taken} stick(s). {self.remaining_sticks} remaining.")
            self.root.after(10, self.bot_move)

        except ValueError:
            messagebox.showerror("Invalid Move", f"Enter a number between 1 and {min(self.max_per_turn, self.remaining_sticks)}.")

    def bot_move(self):
        taken = self.AB(self.remaining_sticks)
        self.remaining_sticks -= taken

        if self.remaining_sticks == 0:
            self.update_status(f"Bot took {taken} stick(s). No sticks left. Bot win!")
            self.take_button.config(state="disabled")
            return

        self.update_status(f"Bot took {taken} stick(s). {self.remaining_sticks} remaining.")
        self.user_input.delete(0, tk.END)

    def AB(self, current):
        global a
        a = -1
        b = 1
        value = -2
        # If doesn't found favor state, choose random (Since it keeps landed on None if choice = None)
        choice = self.Thinking()
        for way in self.allowing:
            if current-way >= 0:
                v = self.MINV(current-way, a, b)
                if v > value:
                    value = v
                if v > a:
                    a = v
                    choice = way
                    # switch choice to get to that state
        return choice 

    # Support functions for Alphe-beta
    def MINV(self,state,a,b):
        if state == 0:
            return 1
        value = 2
        for way in self.allowing:
            if state-way >= 0:
                v = self.MAXV(state-way,a,b)
                if v < value:
                    value = v
                if value <= a:
                    return value
                if value < b:
                    b = value
        return value

    def MAXV(self,state, a, b):
        if state == 0:
            return -1
        value = -2
        for way in self.allowing:
            if state-way >= 0:
                v = self.MINV(state-way,a,b)
                if v > value:
                    value = v
                if value >= b:
                    return value
                if value > a:
                    a = value
        return value

    # Intelligence COM
    def Thinking(self):
        return int(random.choice(self.allowing))

    def restart(self):
        self.game_frame.pack_forget()
        self.take_button.config(state="normal")
        self.total_entry.delete(0, tk.END)
        self.max_entry.delete(0, tk.END)
        self.user_input.delete(0, tk.END)
        self.setup_frame.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = StickGameUI(root)
    root.mainloop()
