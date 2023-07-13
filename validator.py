import subprocess
import os

class Validator:
    def __init__(self):
        pass

    def validate_verilog(self, verilog_code, testbench_file):
        # Write the code to a temporary file
        with open("temp.v", "w") as f:
            f.write(verilog_code)

        # Run the Verilog simulator on the temporary file and the testbench
        result = subprocess.run(["iverilog", "-o", "temp.out", "temp.v", testbench_file], capture_output=True)

        # If the compilation failed, the code is not valid
        if result.returncode != 0:
            return False

        # Run the compiled output and capture the result
        result = subprocess.run(["vvp", "temp.out"], capture_output=True)

        # Check the output of the simulator
        # For simplicity, we'll just check if the simulation completed successfully.
        # In a real application, you would probably want to parse the output to check if the testbench passed.
        return result.returncode == 0
