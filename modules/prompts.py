import tiktoken

# Maximum number of available tokens
MAX_TOKEN = 16000
MAX_MESSAGE_TOKEN = 8000

class Prompts:
    def __init__(self, model):
        self.module_name_prompt = {"role": "user", "content": "Create a JSON dictionary that represents the modules for a hardware design project. Each module should be represented as a key-value pair in the dictionary. The key should be the module name followed by its extension (.v). The value should be another dictionary. This inner dictionary should have two keys: \"connected_to\" and \"description\". The value for \"connected_to\" should be a list of names of modules that are connected to the current module. The value for \"description\" should be a brief sentence explaining the module's function. Do not add any additional text, just output the final JSON dictionary."}
        self.user_prompt_not_ok = {"role": "user", "content": "ask a set of at most 20 questions that will enable you to complete the design"}
        self.user_response_to_questions = {"role": "user", "content": ''}
        self.pre_prompts = [{"role" : "system", "content": "You are a seasoned AI FPGA engineer. Your goal is to write working logic code in VHDL, Verilog and System verilog as well as test benches on your own."},
                            {"role" : "user", "content": "As a hardware engineer, you are given the following Instructions to design a hardware. There are two ways you are allowed to respond to this prompt.\
                    If everything is clear and you know exactly how to write the HDL code, then respond by: <<<Desing OK>>>.\
                    If you need more information before you can write the HDL code, then respond by: <<<Design NOT OK>>>. \
                    Remember, you are only allowed to respond in these two ways. Do not inlcude anything other than the what is instructed in your response. \
                    Instructions: \n\n Design a simple cpu in verilog"},
                            {"role" : "assistant", "content": "<<<Design NOT OK>>>"},
                            self.user_prompt_not_ok,
                            {"role" : "assistant", "content": "1. What type of CPU architecture is required: Von Neumann or Harvard, or another type?\n \
                             2. How many bits should the CPU be? \n \
                             3. What is the required instruction set for this CPU? Is it MIPS, ARM, x86 or a custom one? \n \
                             4. How many general-purpose registers are required? \n \
                             5. Are there any requirements for specific types of registers like stack pointer, program counter, instruction register, etc? \n\
                             6. Does the CPU need to support interrupts? \n \
                             7. What type of memory architecture should be implemented? Does it need cache memory?\n\
                             8. What is the targeted clock speed for the CPU?\n\
                             9. What kind of pipelining is required, if any?\n\
                             10. How should exceptions and error handling be implemented?\n\
                             11. Are there specific requirements for power consumption or heat dissipation?\n\
                             12. Is there a need for any specific I/O interfaces?\n\
                             13. Are there any requirements for instruction decoding and execution? \n \
                             14. What kind of ALU design is needed? \n \
                             15. Is there a requirement for a Floating Point Unit (FPU)?\n \
                             16. Does the CPU need to support multithreading or multiprocessing? \n \
                             17. What type of instruction fetching mechanism should be implemented?\n \
                             18. What will be the bus architecture? Is it to be synchronous or asynchronous?\n \
                             19. What are the physical size limitations for the CPU? \n \
                             20. Are there any specific testing or verification protocols to be followed in the design process?"},
                            {"role" : "user", "content": "The following enumerated list is the answers to your questions: \
                                1. simple custom design \
                                2. 8 bits \
                                3. a simple custom instruction set that you decide upon \
                                4. 8\
                                5. no specific requirements\
                                6. no\
                                7. it does not require cache memory\
                                8. 100 Mhz\
                                9. no pipelining\
                                10. no need for error handling\
                                11. no\
                                12. AXI-lite interface to connect to the PS on a zynq 7000 device \
                                13. no \
                                14. simple alu design that can handle bitwise operations, addition, subtraction, multiplication and division \
                                15. no only signed integer\
                                16. no\
                                17. you decide\
                                18. you decide\
                                19. this should fit a lower end zynq 7000 device \
                                20. no but you will be writing custom test benches for each module that you develop. \n\
                                Your next task is to come up with a description of your design where you describe your solution in detail and lay down the logic and reasoing behind your design choices."},
                            {"role" : "assistant", "content": "Design Overview:\
                                The CPU will be based on an 8-bit custom architecture, operating at a clock frequency of 100 MHz. This design will be tailored for a lower-end Zynq 7000 device, focusing on simplicity and efficiency. \n \
                                Components and Functionality: \n \
                                1. Register File: The CPU will feature 8 general-purpose 8-bit registers for computations and data manipulation. \
                                2. ALU (Arithmetic Logic Unit): A simple ALU will be designed to perform bitwise operations, addition, subtraction, multiplication, and division. These operations will cover a wide array of typical processing tasks.\
                                3. Instruction Set: The custom instruction set will include basic load/store operations, arithmetic operations (ADD, SUB, MUL, DIV), bitwise operations (AND, OR, XOR, NOT), and control flow instructions (JMP, JZ, JNZ). This simplicity will help to reduce complexity and overhead.\
                                4. Control Unit: This unit will decode instructions fetched from memory and generate appropriate control signals to coordinate operations among the CPU components.\
                                5. Memory: Since cache memory isn't required, we'll interface directly with the main memory for simplicity. A Memory Management Unit (MMU) is not necessary given the custom, simple design. Instructions and data will be fetched using separate buses to maximize throughput.\
                                6. I/O: The CPU will use the AXI-lite interface to connect to the PS on the Zynq 7000 device, a standard and widely used interface for such devices.\
                                Reasoning:\n\n \
                                The lack of pipelining, interrupts, and error handling simplifies the design significantly and allows us to focus on basic CPU operations. The custom instruction set ensures that the CPU has the essential functionality without the overhead of unused instructions. This keeps the design efficient, both in terms of performance and resource usage. This design approach also allows for greater control over how instructions are executed and avoids potential hardware compatibility issues. \
                                In terms of memory access, a direct interface with the main memory without cache simplifies the design and is consistent with the goal of minimizing complexity. However, this might lead to a slight decrease in performance, which can be acceptable considering the simplicity it brings.\
                                The ALU is kept simple by only handling essential operations, reducing the number of components and the complexity of the design. Using 8-bit registers is consistent with the 8-bit architecture of the CPU and provides enough capacity for many applications while keeping hardware requirements low.\
                                The selection of the AXI-lite interface for I/O operations is based on its widespread use and compatibility with the Zynq 7000 device. This ensures smooth integration with the PS.\
                                Design decisions for instruction fetching and bus architecture will be driven by an aim for simplicity and efficiency. Likely, a synchronous bus architecture will be used, given its relative simplicity and predictability compared to an asynchronous one. For instruction fetching, a simple fetch-decode-execute cycle will be implemented.\
                                Each module will be tested individually with custom test benches to ensure their correctness and reliability. Despite not having a specific protocol, this method is widely accepted and effective in hardware verification."},
                            self.module_name_prompt,
                            {"role" : "assistant", "content": "\n\
                             {\n\
                                \"register_file.v\": {\n \
                                    \"connected_to\": [\"control_unit.v\", \"ALU.v\"],\n \
                                    \"description\": \"Holds the 8 general-purpose registers and manages data transfer between registers.\"\n \
                                },\n \
                                \"ALU.v\": {\n \
                                    \"connected_to\": [\"register_file.v\", \"control_unit.v\"],\n \
                                    \"description\": \"Performs arithmetic and bitwise operations on data from the registers.\"\n \
                                },\n \
                                \"control_unit.v\": {\n \
                                    \"connected_to\": [\"register_file.v\", \"ALU.v\", \"instruction_memory.v\", \"data_memory.v\"],\n \
                                    \"description\": \"Decodes instructions and generates control signals for the other components.\"\n \
                                },\n \
                                \"instruction_memory.v\": {\n \
                                    \"connected_to\": [\"control_unit.v\"],\n \
                                    \"description\": \"Holds the instructions to be executed by the CPU and sends them to the control unit.\"\n \
                                },\n \
                                \"data_memory.v\": {\n \
                                    \"connected_to\": [\"control_unit.v\", \"register_file.v\"],\n \
                                    \"description\": \"Stores and retrieves data for the CPU, managed by the control unit.\"\n \
                                },\n \
                                \"AXI_lite_interface.v\": {\n \
                                    \"connected_to\": [\"control_unit.v\"],\n \
                                    \"description\": \"Manages I/O operations between the CPU and the PS on the Zynq 7000 device.\"\n \
                                }"
                            }                       ]
        self.model = model
        try:
            self.tokenizer = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.prompt_history = []
        self.num_tokens = sum([self.count_tokens(item["content"]) for item in self.pre_prompts])
        self.message = self.pre_prompts

    def generate_initial_prompt(self, message: str) -> str:
        """This prompt is the first description of the system we want to build."""
        added_tokens = self.count_tokens(message)
        self.num_tokens += added_tokens
        print(f'Total number of tokens at intial prompt: {self.num_tokens}')
        if (self.num_tokens) < MAX_MESSAGE_TOKEN:
            text = f"As a hardware engineer, you are given the following Instructions to design a hardware. There are two ways you are allowed to respond to this prompt.\
                    If everything is clear and you know exactly how to write the HDL code, then respond by: <<<Desing OK>>>.\
                    If you need more information before you can write the HDL code, then respond by: <<<Design NOT OK>>>. \
                    Remember, you are only allowed to respond in these two ways. Do not inlcude anything other than the what is instructed in your response. \
                    Instructions: \n\n {message}"
            self.message.append({"role": "user", "content": text})
            return "success"
        else:
            print("The initial instruction is too large")
            return "failed"

    def generate_module_names(self, language):
        """Thie prompt generates a set of module names and descriptions"""
        self.module_name_prompt['content'].replace(".v", language[1])
        added_tokens = self.count_tokens(self.module_name_prompt['content'])
        self.num_tokens += added_tokens
        print(f'Total number of tokens at generating module names: {self.num_tokens}')
        self.message.append(self.module_name_prompt)

    def generate_followup(self):
        """This prompt asks the followup questions"""
        added_tokens = self.count_tokens(self.user_prompt_not_ok['content'])
        self.num_tokens += added_tokens
        print(f'Total number of tokens at getting the followup questions: {self.num_tokens}')
        self.message.append(self.user_prompt_not_ok)

    def generate_response_to_followup(self, human_response):
        """This prompt gives the user response to the followup questions"""
        self.user_response_to_questions['content'] = human_response
        added_tokens = self.count_tokens(human_response)
        self.num_tokens += added_tokens
        print(f'Total number of tokens at answering the followup questions: {self.num_tokens}')
        self.message.append(self.user_response_to_questions)

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
            num_tokens = len(self.tokenizer.encode(message)) + 4
        except TypeError:
            num_tokens = 4
        return num_tokens
    
    def add_AI_response(self, text):
        """Add AIs response to the trail of messages"""
        self.num_tokens += self.count_tokens(text)
        self.message.append({"role": "user", "content": text})

if __name__ == "__main__":
    p = Prompts('gpt-4')
    p.generate_initial_prompt('')