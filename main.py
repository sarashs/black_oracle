from modules.ai_interface import AIInterface
from modules.user_interface import UserInterface
from modules.design_generator import DesignGenerator
from modules.module_designer import ModuleDesigner
from modules.integration_designer import IntegrationDesigner
from modules.validator import Validator

def main():
    # Instantiate all the classes
    ai = AIInterface()
    ui = UserInterface()
    dg = DesignGenerator(ai, ui)
    md = ModuleDesigner(ai)
    id = IntegrationDesigner(ai)
    val = Validator()

    # Initial prompt
    dg.get_design_features()

    # initial_prompt = ui.get_initial_prompt()
    #ai.prompts.generate_initial_prompt(initial_prompt)

    # Generate a high-level design
    #design = dg.generate_design(initial_prompt)

    while not ui.confirm_design(design):
        # If the user doesn't accept the design, refine it
        design = dg.refine_design(design)

    # Design accepted, generate modules
    modules = []
    for module in design.modules:
        modules.append(md.design_module(module))

    # Generate integration
    integrated_design = id.integrate_design(modules)

    # Validate the design
    if val.validate_verilog(integrated_design.verilog_code):
        ui.show_success()
    else:
        ui.show_failure()

if __name__ == "__main__":
    main()
