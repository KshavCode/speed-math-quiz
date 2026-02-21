import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

from question_maker import question_maker

class MathGameApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("750x450")
        self.root.title("Quick Math Challenge")
        self.root.configure(bg="#1E293B") # Slate dark background
        self.root.resizable(False, False)

        # --- Game State ---
        self.score = 0
        self.total_seconds = 30
        self.timer = self.total_seconds
        self.current_question_data = []
        
        # Ensure CSV exists
        if not os.path.exists("scores.csv"):
            pd.DataFrame(columns=["username", "score"]).to_csv("scores.csv", index=False)

        self.build_main_ui()
        self.start_game()

    def build_main_ui(self):
        """Constructs a modular, centered UI using Frames."""
        # --- Top Bar (Timer & Score) ---
        self.header_frame = tk.Frame(self.root, bg="#1E293B", pady=20, padx=30)
        self.header_frame.pack(fill="x")

        self.timer_label = tk.Label(self.header_frame, text=f"Time: {self.timer}s", 
                                    font=("Verdana", 16, "bold"), bg="#1E293B", fg="#F87171")
        self.timer_label.pack(side="left")

        self.score_label = tk.Label(self.header_frame, text=f"Score: {self.score}", 
                                    font=("Verdana", 16, "bold"), bg="#1E293B", fg="#4ADE80")
        self.score_label.pack(side="right")

        # --- Question Area ---
        self.q_frame = tk.Frame(self.root, bg="#1E293B", pady=40)
        self.q_frame.pack(fill="x")

        self.question_label = tk.Label(self.q_frame, text="Loading...", 
                                       font=("Helvetica", 48, "bold"), bg="#1E293B", fg="white")
        self.question_label.pack(expand=True)

        # --- Options Area ---
        self.options_frame = tk.Frame(self.root, bg="#1E293B")
        self.options_frame.pack(pady=20)

        # We will store the button objects in a list so we can update them dynamically
        self.option_buttons = []
        for i in range(3):
            btn = tk.Button(self.options_frame, text="", font=("Verdana", 20, "bold"), 
                            width=8, bg="#3B82F6", fg="white", activebackground="#2563EB", 
                            activeforeground="white", relief="flat", cursor="hand2")
            btn.grid(row=0, column=i, padx=15)
            self.option_buttons.append(btn)

    def start_game(self):
        self.load_new_question()
        self.update_timer()

    def load_new_question(self):
        """Fetches a new question and updates the buttons."""
        self.current_question_data = question_maker()
        
        # current_question_data format: [Question String, [Opt1, Opt2, Opt3], Correct Answer]
        self.question_label.config(text=self.current_question_data[0])
        options = self.current_question_data[1]

        for i in range(3):
            # Update button text and assign the specific option to the command dynamically
            opt_value = options[i]
            self.option_buttons[i].config(
                text=opt_value, 
                command=lambda opt=opt_value: self.check_answer(opt)
            )

    def check_answer(self, selected_option):
        """Validates the answer and updates the score (DRY principle applied)."""
        correct_answer = self.current_question_data[2]
        
        if str(selected_option) == str(correct_answer):
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            
        self.load_new_question()

    def update_timer(self):
        """Handles the countdown loop natively."""
        if self.timer > 0:
            self.timer -= 1
            self.timer_label.config(text=f"Time: {self.timer}s")
            self.root.after(1000, self.update_timer)
        else:
            self.finish_game()

    def finish_game(self):
        """Disables buttons and triggers the save screen."""
        for btn in self.option_buttons:
            btn.config(state="disabled", bg="#64748B") # Gray out buttons
        self.open_input_window()

    def open_input_window(self):
        """Modal window to capture the username."""
        win = tk.Toplevel(self.root)
        win.geometry("350x150")
        win.title("Time's Up!")
        win.configure(bg="#F1F5F9")
        win.resizable(False, False)
        
        # Grab focus so user can't click main window
        win.grab_set() 

        tk.Label(win, text=f"Final Score: {self.score}", font=("Helvetica", 14, "bold"), 
                 bg="#F1F5F9", fg="#0F172A").pack(pady=(15, 5))

        input_frame = tk.Frame(win, bg="#F1F5F9")
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Username:", font=("Helvetica", 12), bg="#F1F5F9").pack(side="left", padx=5)
        entry1 = tk.Entry(input_frame, font=("Helvetica", 12), width=15)
        entry1.pack(side="left", padx=5)
        entry1.focus() # Auto-focus the cursor in the entry box

        def submit():
            username = entry1.get().strip()
            if not username:
                messagebox.showwarning("Required", "Please enter a username.", parent=win)
                return
            
            # Save to Pandas
            df = pd.read_csv("scores.csv")
            newdf = pd.DataFrame({"username": [username], "score": [self.score]})
            df = pd.concat([df, newdf], ignore_index=True)
            df.to_csv("scores.csv", index=False)
            
            win.destroy()
            self.show_scoreboard(username)

        tk.Button(win, text="Save Score", font=("Helvetica", 11, "bold"), bg="#10B981", fg="white", 
                  relief="flat", command=submit, cursor="hand2").pack(pady=10)

    def show_scoreboard(self, current_user):
        """Displays the top scores using a modern Treeview table."""
        board = tk.Toplevel(self.root)
        board.title("Global Leaderboard")
        board.geometry("450x500")
        board.configure(bg="#F8FAFC")
        
        tk.Label(board, text="Top 10 High Scores", font=("Helvetica", 18, "bold"), 
                 bg="#F8FAFC", fg="#1E293B").pack(pady=20)

        # Style the Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'), background="#E2E8F0")
        style.configure("Treeview", font=('Helvetica', 11), rowheight=30)

        # Create Table
        columns = ("rank", "username", "score")
        tree = ttk.Treeview(board, columns=columns, show="headings", height=10)
        tree.heading("rank", text="Rank")
        tree.heading("username", text="Username")
        tree.heading("score", text="Score")
        
        tree.column("rank", width=80, anchor="center")
        tree.column("username", width=200, anchor="center")
        tree.column("score", width=100, anchor="center")
        tree.pack(pady=10, padx=20, fill="both", expand=True)

        # Load and sort data
        df = pd.read_csv("scores.csv")
        df = df.sort_values(by=["score"], ascending=False).reset_index(drop=True)

        # Insert Top 10 into table
        for idx, row in df.head(10).iterrows():
            tree.insert("", "end", values=(idx + 1, row['username'], row['score']))

        # Highlight current user's performance at the bottom
        user_rank = df.index[(df['username'] == current_user) & (df['score'] == self.score)].tolist()[0] + 1
        
        summary_text = f"Your Rank: {user_rank}  |  Your Score: {self.score}"
        tk.Label(board, text=summary_text, font=("Helvetica", 13, "bold"), 
                 bg="#1E293B", fg="#F8FAFC", pady=10).pack(fill="x", side="bottom")

if __name__ == "__main__":
    root = tk.Tk()
    app = MathGameApp(root)
    root.mainloop()