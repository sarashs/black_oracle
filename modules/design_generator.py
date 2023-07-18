from modules.ai_interface import AIInterface
from modules.user_interface import UserInterface
import json
import os

class DesignGenerator:
    def __init__(self, ai_interface, u_interface):
        self.ai_interface = ai_interface
        self.u_interface = u_interface
        self.language = None
        self.module_name_dict = {}

    def get_design_features(self):
        prompt, self.language = self.u_interface.get_initial_prompt()
        _ = self.ai_interface.prompts.generate_initial_prompt(prompt)
        self.ai_interface.send_prompt()
        response = self.ai_interface.receive_response()
        human_response = None
        # Assess the response
        if "design ok" in response.lower():
            self.ai_interface.prompts.generate_module_names(self.language)
        else:
            self.ai_interface.prompts.generate_followup()
            self.ai_interface.send_prompt()
            response = self.ai_interface.receive_response()
            print(response)
            human_response = self.u_interface.get_respone_to_questions()
# TODO: I could probably improve how I handle this
            self.ai_interface.prompts.generate_response_to_followup(human_response)
            self.ai_interface.send_prompt()
            self.ai_interface.prompts.generate_module_names(self.language)
        self.ai_interface.send_prompt()
        response = self.ai_interface.receive_response()
        try:
            self.module_name_dict = json.loads(response)
        except json.JSONDecodeError:
            print("AI response is not as expected (JSON dict). Please try another prompt.")
        print(f'Your design will be implemented as follows: \n\n {response}')

    def generate_architecture(self) -> list:
        for module in self.module_name_dict.keys():
            self.ai_interface.prompts.generate_module(module)
            self.ai_interface.send_prompt()
            response = self.ai_interface.receive_response()
            directory = 'solution'
            full_path = os.path.join(os.getcwd(), directory, module)
            os.makedirs(os.path.join(os.getcwd(), directory), exist_ok=True)
            with open(full_path, 'w') as file:
                file.write(response)

if __name__ == "__main__":
    ai = AIInterface()
    ui = UserInterface()
    dg = DesignGenerator(ai, ui)
    dg.get_design_features()
    dg.generate_architecture()
    #print(dg.ai_interface.prompts.message)
