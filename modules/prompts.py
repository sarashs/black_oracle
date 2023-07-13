import tiktoken

# Maximum number of available tokens
MAX_TOKEN = 16000
MAX_MESSAGE_TOKEN = MAX_TOKEN / 2

class Prompts:
    def __init__(self, model):
        self.pre_prompts = [{"role" : "system", "content": "You are a seasoned FPGA engineer. You are capable of writing logic code in VHDL, Verilog and System verilog as well as test benches on your own."},
               ]
        self.model = model
        try:
            self.tokenizer = tiktoken.encoding_for_model(model)
        except KeyError:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.prompt_history = []
        self.num_tokens = sum([self.count_tokens(item["content"]) for item in self.pre_prompts])
        self.message = self.pre_prompts

    def generate_initial_prompt(self, message: str):
        """This prompt is the first description of the system we want to build."""
        added_tokens = self.count_tokens(message)
        if (self.num_tokens + added_tokens) < MAX_MESSAGE_TOKEN:
            self.message.append({"role": "user", "content": message})
            return "success"
        else:
            print("The initial instruction is too large")
            return "failed"

    def generate_followup(self):
        """This prompt responds to the followup questions"""
        pass

    def generate_module(self):
        """Prompt that tells GPT to generate modules"""
        pass    

    def generate_wrapper(self):
        """Prompt that tells GPT to generate modules"""
        pass

    def count_tokens(self, message):
        """Counts the number of tokens"""

        # we add an extra 4 tokens for role system/user/assisstance content and \n
        try:
            num_tokens = len(self.tokenizer(message)) + 4
        except TypeError:
            num_tokens = 4
        return num_tokens
