import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, font
try:
    from modules.utils import SAVEDIR
except ModuleNotFoundError:
    from utils import SAVEDIR

class UserInterface:
    def __init__(self, gui=False):
        self.gui = gui

    def get_initial_prompt(self):
        # Gets an initial prompt from the user
        if self.gui:
            app = GenericWindow("main")
            app.mainloop()
            prompt, option = app.get_user_input()
            prompt = prompt + f'\n The code must be written in {option}'
        else:
            print("Please enter your initial design prompt. Make sure to include your desired hardware description language (verilog, system verilog, vhdl, HLS):")
            prompt = input()
        return prompt
    
    def get_respone_to_questions(self):
        """This function obtains the users response to AI's questions via a file"""
        if self.gui:
            # If GUI mode is active, launch the secondary window
            app = GenericWindow("secondary")
            app.mainloop()
        else:
            print("Please input the relative path to your responses to the AI questions. Note that your responses should be an itemized list of replies to the AI questions with no extra text.")
            response_path = input()
            #try:
            with open(response_path, 'r') as file:
                content = file.read()
        return content

    def show_design(self, design):
        # Shows a design to the user
        print("Here's the proposed design:")
        print(design)

    def get_feedback(self):
        # Gets feedback from the user
        print("Do you accept this design? (yes/no)")
        feedback = input()
        return feedback.lower() == 'yes'
    

class GenericWindow(tk.Tk):
    def __init__(self, window_type="main", results=None):
        super().__init__()
        self.customFont = font.Font(family="Helvetica", size=14)
        self.user_prompt = ""
        self.user_options = ""
        self.options = ["Verilog", "System Verilog", "VHDL", "HLS C/C++"]
        self.file_path = tk.StringVar()
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

        for val, option in enumerate(self.options):
            tk.Radiobutton(self, text=option, variable=self.option_var, value=val, font=self.customFont).pack(anchor='w')

        tk.Button(self, text="Submit", command=self.on_submit_main, font=self.customFont).pack(pady=20)

    def on_submit_main(self):
        # This function would send the data from the main window
        # to the backend
        # Sample code:
        #read_file = self.read_file_var.get()
        file_path = self.file_path.get()
        self.user_prompt = self.prompt_text.get("1.0", tk.END).strip()
        self.user_option = self.options[self.option_var.get()]

        self.destroy()

    def init_secondary_window(self, results):
        self.title("Follow up questions")
        self.iconbitmap('Images\logo.ico')

        result_label = tk.Label(self, text=results)
        result_label.pack(pady=10)

        text_widget = tk.Text(self, height=2, width=50, font=self.customFont)
        text_widget.pack()
        text_widget.insert(tk.END, f"Check the {SAVEDIR} folder for follow-up questions.")

        # If you only want to display text and prevent user input:
        text_widget.config(state=tk.DISABLED)

        # New prompt entry
        tk.Label(self, text="Response to questions:", font=self.customFont).pack(pady=5)
        self.prompt_text = tk.Text(self, width=150, height=30)
        self.prompt_text.pack(pady=5)

        # Button for file dialog
        tk.Button(self, text="Choose File", command=self._choose_file, font=self.customFont).pack(pady=10)
        self.file_path_label = tk.Label(self, text="", font=self.customFont)
        self.file_path_label.pack(pady=10)

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

    def get_user_input(self):
        """This function returns the collected values from the GUI."""
        return self.user_prompt, self.user_option

if __name__ == "__main__":
    ui = UserInterface(True)
    ui.get_initial_prompt()
