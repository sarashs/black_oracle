import argparse
from modules.ai_interface import AIInterface
from modules.user_interface import UserInterface
from modules.design_generator import DesignGenerator

def main(args):
    # Your main terminal-based function remains the same
    ai = AIInterface(model=args.model)
    ui = UserInterface(args.gui)
    dg = DesignGenerator(ai, ui)
    dg.get_design_features(args.no_follow_up, args.read_file, args.file_path)
    dg.generate_architecture()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic set up for the black oracle")
    parser.add_argument("-m", "--model", 
                        choices=["gpt-3.5-turbo-16k", "gpt-4"], 
                        default="gpt-3.5-turbo-16k",
                        help="Pick one of the available models.")
    parser.add_argument("-n", "--no_follow_up",
                        default=False, action="store_true",
                        help="Do not ask followup questions and just design based on the prompt.")
    parser.add_argument("-r", "--read_file",
                        default=False, action="store_true",
                        help="Whether to read the first prompt from a file or not.")
    parser.add_argument("-f", "--file_path",
                        nargs="?", default=None,
                        help="Path to the file to be processed (optional, required if '--read_file' is specified).")
    parser.add_argument("--gui",
                        action="store_true",
                        help="Launch the GUI interface.")
    
    args = parser.parse_args()

    if args.read_file and not args.file_path:
        raise RuntimeError("A file path must be provided when using '--read_file' option.")
    main(args)
