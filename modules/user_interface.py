class UserInterface:
    def __init__(self):
        pass

    def get_initial_prompt(self):
        # Gets an initial prompt from the user
        print("Please enter your initial design prompt. Make sure to include your desired hardware description language (verilog, system verilog, vhdl):")
        prompt = input()
        language = None
        if ("verilog" in prompt): 
            language = ("veilog", ".v")
        elif ("vhdl" in prompt):
            language = ("vhdl", ".vhdl")
        elif ("system verilog" in prompt):
            language = ("system verilog", ".sv")
        else:
            self.get_initial_prompt()
        return prompt, language

    def show_design(self, design):
        # Shows a design to the user
        print("Here's the proposed design:")
        print(design)

    def get_feedback(self):
        # Gets feedback from the user
        print("Do you accept this design? (yes/no)")
        feedback = input()
        return feedback.lower() == 'yes'

if __name__ == "__main__":
    ui = UserInterface()
    ui.get_initial_prompt()
