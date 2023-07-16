from ai_interface import AIInterface
from user_interface import UserInterface

class DesignGenerator:
    def __init__(self, ai_interface, u_interface):
        self.ai_interface = ai_interface
        self.u_interface = u_interface
        self.language = None

    def get_design_features(self):
        prompt, self.language = self.u_interface.get_initial_prompt()
        _ = self.ai_interface.prompts.generate_initial_prompt(prompt)
        self.ai_interface.send_prompt()
        response = self.ai_interface.receive_response()
        # Assess the response
        if "design ok" in response.lower():
            self.ai_interface.prompts.generate_module_names(self.language)
        else:
            self.ai_interface.prompts.generate_followup()
            self.ai_interface.send_prompt()
            response = self.ai_interface.receive_response()
            #self.ai_interface.prompts.generate_module_names(self.language)
        self.ai_interface.send_prompt()
        response = self.ai_interface.receive_response()
        return response

    def generate_architecture(self) -> list:
        pass

    def generate_design(self, user_prompt):
        # Translates the user prompt into an AI prompt
        ai_prompt = f"Generate a high-level hardware design based on the following user prompt: {user_prompt}"

        # Sends the AI prompt to the AI
        self.ai_interface.send_prompt(ai_prompt)

        # Receives the AI response
        ai_response = self.ai_interface.receive_response()

        # Translates the AI response into a user-friendly design
        design = f"Based on your prompt, here's a proposed high-level hardware design:\n{ai_response}"

        return design

if __name__ == "__main__":
    ai = AIInterface()
    ui = UserInterface()
    dg = DesignGenerator(ai, ui)
    response = dg.get_design_features()
    print(response)
    #print(dg.ai_interface.prompts.message)