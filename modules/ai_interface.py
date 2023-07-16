import openai
import os
from prompts import Prompts

class AIInterface:
    def __init__(self, model='gpt-4'):
        try:
            self.api_key = os.getenv("OPENAI_API_KEY")
        except:
            print("OPENAI_API_KEY environment variable is likely not set!")
        openai.api_key = self.api_key
        self.model = self.set_model(model)
        self.prompts = Prompts(self.model)

    def send_prompt(self):
        # Sends a prompt to the OpenAI API
        self.response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.prompts.message,
            temperature=0.0
            )

    def receive_response(self):
        # Retrieves the generated response from the OpenAI API
        self.prompts.add_AI_response(self.response.choices[0].message["content"])
        return self.response.choices[0].message["content"]
    
    def set_model(self, model):
        try:
            openai.Model.retrieve(model)
        except openai.InvalidRequestError:
            model_alt = "gpt-3.5-turbo-16k"
            print(f'Model is set to {model_alt}. It seems that your API does not support {model}.')
            model = model_alt
        return model

if __name__ == "__main__":
    test_interface = AIInterface()
    test_interface.prompts.generate_initial_prompt("Desing a risc-jj cpu in system verilog")
    test_interface.send_prompt()
    response = test_interface.receive_response()
    try:
        assert response != None, "Test: Failed"
        print(f"Test: OK, response: {response}")
    except AssertionError as e:
        print(e)