try:
    from modules.ai_interface import AIInterface
    from modules.user_interface import UserInterface
    from modules.utils import remove_unwanted_lines, save_to_file
except ModuleNotFoundError:
    from ai_interface import AIInterface
    from user_interface import UserInterface
    from utils import remove_unwanted_lines, save_to_file
import json
import os

class DesignGenerator:
    def __init__(self, ai_interface, u_interface):
        self.ai_interface = ai_interface
        self.u_interface = u_interface
        self.language = None
        self.module_name_dict = {}

    def get_design_features(self, no_follow_up=False, read_file=False, file_path=None):
        if read_file:
            print("Reading the prompt file...")
            if file_path:
                try:
                    with open(file_path) as file:
                        prompt = file.read()
                except:
                    raise FileNotFoundError(f"No file was found in the provided path: {file_path}")
            else:
                raise RuntimeError("A file path must be provided.")
        else:
            prompt = self.u_interface.get_initial_prompt()
        if ("system verilog" in prompt.lower() or "systemverilog" in prompt.lower()): 
            self.language = ("system verilog", ".sv")
        elif ("vhdl" in prompt.lower()):
            self.language = ("vhdl", ".vhdl")
        elif ("verilog" in prompt.lower()):
            self.language = ("verilog", ".v")
        elif ("hls" in prompt.lower()):
            self.language = ("HLS (cpp)", ".cpp")
        else:
            raise NameError("No language name was found in the prompt.")
        print(f"The solution will be generated in {self.language[0]}")
        _ = self.ai_interface.prompts.generate_initial_prompt(prompt, self.language)
        self.ai_interface.send_prompt()
        response = self.ai_interface.receive_response()
        human_response = None
        # Assess the response
        if ("design ok" in response.lower()) or no_follow_up:
            self.ai_interface.prompts.generate_module_names()
        else:
            self.ai_interface.prompts.generate_followup()
            self.ai_interface.send_prompt()
            response = self.ai_interface.receive_response()
            save_to_file("follow_up_questions.doc", remove_unwanted_lines(response))

# TODO: Replace these prints with logs
            print(response)

            human_response = self.u_interface.get_respone_to_questions()
# TODO: I could probably improve how I handle this
            self.ai_interface.prompts.generate_response_to_followup(human_response)
            self.ai_interface.send_prompt()
            self.ai_interface.prompts.generate_module_names()
        self.ai_interface.send_prompt()
        response = self.ai_interface.receive_response()
        try:
            self.module_name_dict = json.loads(response)
        except json.JSONDecodeError:
            print("AI response is not as expected (JSON dict). Please try another prompt.")
        self.u_interface.show_design(response)
        save_to_file("high_level_design.json", remove_unwanted_lines(response))

    def generate_architecture(self):
        for module in self.module_name_dict.keys():
            self.ai_interface.prompts.generate_module(module, self.module_name_dict[module])
            self.ai_interface.send_prompt()
            response = self.ai_interface.receive_response()
            save_to_file(module, remove_unwanted_lines(response))
        # Generate test bench
            self.ai_interface.prompts.generate_testbench_module(module, response)
            self.ai_interface.send_prompt()
            response = self.ai_interface.receive_response()
            save_to_file(module.replace(self.language[1], "_tb" + self.language[1]), remove_unwanted_lines(response))
        self.u_interface.get_feedback()

if __name__ == "__main__":
    ai = AIInterface()
    ui = UserInterface()
    dg = DesignGenerator(ai, ui)
    dg.get_design_features()
    dg.generate_architecture()
    #print(dg.ai_interface.prompts.message)
