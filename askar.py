import tkinter as tk
from tkinter import messagebox
import random
import string
import secrets
import threading

class ModernPasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("CipherGen Pro")
        self.root.geometry("450x650")
        self.root.configure(bg="#121212")  # Deep dark background
        self.root.resizable(False, False)

        # Theme Colors
        self.primary = "#88FF00"    # Purple
        self.secondary = "#E5FF00"  # Teal
        self.bg_light = "#12F0F0"   # Surface color
        self.text_main = "#89A5B6"
        self.text_dim = "#AD9E9E"

        # State Variables
        self.password_var = tk.StringVar(value="Click Generate")
        self.length_var = tk.IntVar(value=16)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        self._build_ui()

    def _build_ui(self):
        """Constructs a modern, centered GUI layout."""
        
        # Header Section
        header = tk.Frame(self.root, bg="#121212", pady=30)
        header.pack(fill="x")
        
        tk.Label(
            header, text="CIPHERGEN", font=("Helvetica", 24, "bold"),
            bg="#121212", fg=self.primary
        ).pack()
        
        tk.Label(
            header, text="Secure Password Architect", font=("Helvetica", 10),
            bg="#121212", fg=self.text_dim
        ).pack()

        # Output Display Box
        display_frame = tk.Frame(self.root, bg=self.bg_light, padx=20, pady=20, highlightthickness=1, highlightbackground="#333333")
        display_frame.pack(padx=30, fill="x")

        self.pass_entry = tk.Entry(
            display_frame, textvariable=self.password_var, font=("Consolas", 16),
            bg=self.bg_light, fg=self.secondary, borderwidth=0, justify="center"
        )
        self.pass_entry.pack(fill="x")

        # Strength Indicator Bar (Canvas)
        self.strength_canvas = tk.Canvas(self.root, height=4, bg="#333333", highlightthickness=0)
        self.strength_canvas.pack(padx=30, pady=(0, 20), fill="x")
        self.strength_bar = self.strength_canvas.create_rectangle(0, 0, 0, 4, fill=self.secondary, outline="")

        # Controls Section
        controls = tk.Frame(self.root, bg="#121212", padx=30)
        controls.pack(fill="both", expand=True)

        # Length Slider
        tk.Label(controls, text="PASSWORD  LENGTH", font=("Arial ", 9, "bold"), bg="#121212", fg=self.text_dim).pack(anchor="w")
        
        slider_frame = tk.Frame(controls, bg="#121212")
        slider_frame.pack(fill="x", pady=(5, 20))
        
        self.len_slider = tk.Scale(
            slider_frame, from_=8, to=64, variable=self.length_var, orient="horizontal",
            bg="#121212", fg=self.text_main, highlightthickness=0, troughcolor="#333333",
            activebackground=self.primary, font=("Helvetica", 10)
        )
        self.len_slider.pack(fill="x")

        # Toggle Switches (Checkbuttons)
        options = [
            ("Uppercase Letters (A-Z)", self.use_upper),
            ("Lowercase Letters (a-z)", self.use_lower),
            ("Include Numbers (0-9)", self.use_digits),
            ("Special Symbols (!@#$)", self.use_symbols),
        ]

        for text, var in options:
            cb = tk.Checkbutton(
                controls, text=text, variable=var, bg="#121212", fg=self.text_main,
                selectcolor="#121212", activebackground="#121212", activeforeground=self.primary,
                font=("Helvetica", 11), pady=8, borderwidth=0
            )
            cb.pack(anchor="w")

        # Action Buttons
        btn_frame = tk.Frame(self.root, bg="#121212", pady=40)
        btn_frame.pack(fill="x")

        # Generate Button
        gen_btn = tk.Button(
            btn_frame, text="GENERATE PASSWORD", command=self.generate_password,
            bg=self.primary, fg="#000000", font=("Helvetica", 12, "bold"),
            padx=20, pady=12, borderwidth=0, cursor="hand2", activebackground="#9965f4"
        )
        gen_btn.pack(pady=10, padx=30, fill="x")

        # Copy Button
        copy_btn = tk.Button(
            btn_frame, text="Copy to Clipboard", command=self.copy_password,
            bg="#121212", fg=self.text_dim, font=("Helvetica", 10),
            padx=10, pady=5, borderwidth=1, relief="flat", cursor="hand2"
        )
        copy_btn.pack()

    def update_strength_ui(self, score):
        """Animates the strength bar based on password entropy."""
        colors = ["#f44336", "#ff9800", "#ffeb3b", "#4caf50"] # Red, Orange, Yellow, Green
        width = self.strength_canvas.winfo_width()
        
        # Calculate width based on score (0-4)
        target_width = (width / 4) * score
        color = colors[min(score - 1, 3)] if score > 0 else "#333333"
        
        self.strength_canvas.coords(self.strength_bar, 0, 0, target_width, 4)
        self.strength_canvas.itemconfig(self.strength_bar, fill=color)

    def generate_password(self):
        """Uses secrets module for cryptographically secure generation."""
        char_pool = ""
        if self.use_upper.get(): char_pool += string.ascii_uppercase
        if self.use_lower.get(): char_pool += string.ascii_lowercase
        if self.use_digits.get(): char_pool += string.digits
        if self.use_symbols.get(): char_pool += string.punctuation

        if not char_pool:
            messagebox.showwarning("Selection Error", "Please select at least one character type.")
            return

        length = self.length_var.get()
        # Using 'secrets' instead of 'random' for security-critical apps
        password = "".join(secrets.choice(char_pool) for _ in range(length))
        
        self.password_var.set(password)
        
        # Simple strength logic
        score = 1
        if length >= 12: score += 1
        if sum([self.use_upper.get(), self.use_digits.get(), self.use_symbols.get()]) >= 2: score += 1
        if length >= 20 and self.use_symbols.get(): score += 1
        
        self.update_strength_ui(score)

    def copy_password(self):
        """Copies text to clipboard safely."""
        password = self.password_var.get()
        if password in ["", "Click Generate"]:
            return
            
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        
        # Temporary visual feedback on the button
        messagebox.showinfo("Success", "Password copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernPasswordGenerator(root)
    root.mainloop()