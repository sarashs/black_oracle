from modules.ai_interface import AIInterface
from modules.user_interface import UserInterface
from modules.design_generator import DesignGenerator
from modules.integration_designer import IntegrationDesigner
from modules.validator import Validator

def main():
    # Instantiate all the classes
    ai = AIInterface()
    ui = UserInterface()
    dg = DesignGenerator(ai, ui)
    #id = IntegrationDesigner(ai)
    #val = Validator()
    dg.get_design_features()
    dg.generate_architecture()
    # Validate the design
    #if val.validate_verilog(integrated_design.verilog_code):
    #    ui.show_success()
    #else:
    #    ui.show_failure()

if __name__ == "__main__":
    main()
