from ai_interface import AIInterface

class IntegrationDesigner:
    def __init__(self, ai_interface):
        self.ai_interface = ai_interface

    def design_integration(self, module_names):
        # Translates the module names into an AI prompt
        ai_prompt = f"Generate Verilog code for integrating the following hardware modules: {', '.join(module_names)}"

        # Sends the AI prompt to the AI
        self.ai_interface.send_prompt(ai_prompt)

        # Receives the AI response
        ai_response = self.ai_interface.receive_response()

        # Translates the AI response into a user-friendly design
        integration_code = f"Based on your modules, here's the proposed Verilog code for integrating them:\n{ai_response}"

        return integration_code