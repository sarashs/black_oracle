from ai_interface import AIInterface

class DesignGenerator:
    def __init__(self, ai_interface):
        self.ai_interface = ai_interface

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
