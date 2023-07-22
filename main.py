import argparse
from modules.ai_interface import AIInterface
from modules.user_interface import UserInterface
from modules.design_generator import DesignGenerator
from modules.integration_designer import IntegrationDesigner
from modules.validator import Validator

def main(read_file, file_path):
    # Instantiate all the classes
    ai = AIInterface()
    ui = UserInterface()
    dg = DesignGenerator(ai, ui)
    #id = IntegrationDesigner(ai)
    #val = Validator()
    dg.get_design_features(read_file, file_path)
    dg.generate_architecture()
    # Validate the design
    #if val.validate_verilog(integrated_design.verilog_code):
    #    ui.show_success()
    #else:
    #    ui.show_failure()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic set up for the black oracle")
    parser.add_argument("-r", "--read_file",default=False , action="store_true", help="Whether to read the first prompt from a file or not.")
    parser.add_argument("file_path", nargs="?", default=None, help="Path to the file to be processed (optional, required if '--read_file' is specified).")
    args = parser.parse_args()
    if args.read_file:
        if args.file_path:
            pass
        else:
            raise RuntimeError("A file path must be provided when using '--read_file' option.")
    main(args.read_file, args.file_path)
