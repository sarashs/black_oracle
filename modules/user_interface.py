class UserInterface:
    def __init__(self):
        pass

    def get_initial_prompt(self):
        # Gets an initial prompt from the user
        print("Please enter your initial design prompt:")
        prompt = input()
        return prompt

    def show_design(self, design):
        # Shows a design to the user
        print("Here's the proposed design:")
        print(design)

    def get_feedback(self):
        # Gets feedback from the user
        print("Do you accept this design? (yes/no)")
        feedback = input()
        return feedback.lower() == 'yes'
