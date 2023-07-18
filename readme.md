# Black Oracle: GPT Hardware Generator

This tool leverages the capabilities of OpenAI's GPT model to automate hardware design based on user prompts. It's an easy-to-use tool that requires minimal inputs from the user.

## Prerequisites

Ensure you have Python 3.x installed and the pip package manager.

Before running the project, you'll need to have an OpenAI API key (purchage/get one from here: https://platform.openai.com/). Make sure to set this up, as it is a crucial part of the project.

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/sarashs/black_oracle.git
    ```

2. Navigate to the project directory:
    ```
    cd gpt-hardware-generator
    ```

3. Install the necessary requirements using pip:
    ```
    pip install -r requirements.txt
    ```

## Usage

Run the following command to start the application:
```
python main.py
```

During the execution, the program asks for two sets of user input:
- An initial prompt for the hardware design, e.g., "design a full adder in Verilog"
- Responses to clarification questions asked by the AI model

The AI will generate the hardware design based on these inputs.

## Status

Please note that this project is currently in its initial stages and under active development. Feedback and contributions are always welcome!