import tkinter as tk
from tkinter import messagebox
import argparse
from modules.ai_interface import AIInterface
from modules.user_interface import UserInterface
from modules.design_generator import DesignGenerator
from tkinter import filedialog, font

class GenericWindow(tk.Tk):
    def __init__(self, window_type="main", results=None):
        super().__init__()
        self.customFont = font.Font(family="Helvetica", size=14)
        if window_type == "main":
            self.init_main_window()
        elif window_type == "secondary":
            self.init_secondary_window(results)
        elif window_type == "tertiary":
            self.init_tertiary_window()

    def init_main_window(self):
        self.title("Black Oracle UI")
        self.iconbitmap('Images\logo.ico')
        self.my_image = tk.PhotoImage(file="Images\logo.png")
        self.my_image = self.my_image.subsample(8, 8)
        image_label = tk.Label(self, image=self.my_image)
        image_label.pack(side="left", padx=(0,0))

        #self.read_file_var = tk.BooleanVar(value=False)
        self.file_path = tk.StringVar()
        self.option_var = tk.IntVar()

        #tk.Checkbutton(self, text="Read file", variable=self.read_file_var).pack(pady=10)

        # Button for file dialog
        tk.Button(self, text="Choose File", command=self._choose_file, font=self.customFont).pack(pady=10)
        self.file_path_label = tk.Label(self, text="", font=self.customFont)
        self.file_path_label.pack(pady=10)

        # New prompt entry
        tk.Label(self, text="Prompt:", font=self.customFont).pack(pady=5)
        self.prompt_text = tk.Text(self, width=150, height=30)
        self.prompt_text.pack(pady=5)

        options = ["Verilog", "System Verilog", "VHDL", "HLS C/C++"]

        for val, option in enumerate(options):
            tk.Radiobutton(self, text=option, variable=self.option_var, value=val, font=self.customFont).pack(anchor='w')

        tk.Button(self, text="Submit", command=self.on_submit_main, font=self.customFont).pack(pady=20)

    def on_submit_main(self):
        # This function would send the data from the main window
        # to your backend, and collect the results to show them in
        # the secondary window.
        # Sample code:
        #read_file = self.read_file_var.get()
        file_path = self.file_path.get()
        prompt_value = self.prompt_text.get("1.0", tk.END).strip()

        # Mock results:
        results = "The results from your backend logic."

        self.destroy()
        app = GenericWindow("secondary", results)
        app.mainloop()

    def init_secondary_window(self, results):
        self.title("Results")

        result_label = tk.Label(self, text=results)
        result_label.pack(pady=10)

        tk.Button(self, text="Proceed", command=self.on_proceed).pack(pady=20)

    def on_proceed(self):
        # Destroy current window and launch tertiary window
        self.destroy()
        app = GenericWindow("tertiary")
        app.mainloop()

    def init_tertiary_window(self):
        self.title("Additional Inputs")

        tk.Label(self, text="Enter more details:").pack(pady=5)
        self.additional_input = tk.Text(self, width=50, height=10)
        self.additional_input.pack(pady=5)

        tk.Button(self, text="Submit", command=self.on_submit_tertiary).pack(pady=20)

    def on_submit_tertiary(self):
        additional_info = self.additional_input.get("1.0", tk.END).strip()
        # Do something with the additional_info
        self.destroy()
    
    def _choose_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.file_path.set(filepath)
            self.file_path_label.config(text=filepath)
            # Read the file content and update the prompt
            with open(filepath, 'r') as file:
                file_content = file.read()
            self.prompt_text.delete(1.0, tk.END)  # Clear existing content
            self.prompt_text.insert(tk.END, file_content)

def main(read_file, file_path):
    # Your main terminal-based function remains the same
    ai = AIInterface()
    ui = UserInterface()
    dg = DesignGenerator(ai, ui)
    dg.get_design_features(read_file, file_path)
    dg.generate_architecture()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic set up for the black oracle")
    parser.add_argument("-r", "--read_file", default=False, action="store_true", help="Whether to read the first prompt from a file or not.")
    parser.add_argument("-f", "--file_path", nargs="?", default=None, help="Path to the file to be processed (optional, required if '--read_file' is specified).")
    parser.add_argument("--gui", action="store_true", help="Launch the GUI interface.")
    
    args = parser.parse_args()

    if args.gui:
        app = GenericWindow("main")
        app.mainloop()
    else:
        if args.read_file and not args.file_path:
            raise RuntimeError("A file path must be provided when using '--read_file' option.")
        main(args.read_file, args.file_path)
