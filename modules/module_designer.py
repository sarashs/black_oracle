from ai_interface import AIInterface

class ModuleDesigner:
    def __init__(self, ai_interface):
        self.ai_interface = ai_interface

    def design_module(self, module_spec):
        # Translates the module specification into an AI prompt
        ai_prompt = f"Generate Verilog code for a hardware module based on the following specification: {module_spec}"

        # Sends the AI prompt to the AI
        self.ai_interface.send_prompt(ai_prompt)

        # Receives the AI response
        ai_response = self.ai_interface.receive_response()

        # Translates the AI response into a user-friendly design
        module_code = f"Based on your specification, here's the proposed Verilog code for your module:\n{ai_response}"

        return module_code