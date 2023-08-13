import os

SAVEDIR = 'solution'

def remove_unwanted_lines(code):
    lines = code.split('\n')
    # Keep only lines that do not start with triple backticks or "Note:"
    lines = [line for line in lines if not line.strip().startswith('```') and not line.strip().startswith('Note:')]
    return '\n'.join(lines)

def save_to_file(file_name, content):
    directory = SAVEDIR
    full_path = os.path.join(os.getcwd(), directory, file_name)
    os.makedirs(os.path.join(os.getcwd(), directory), exist_ok=True)
    with open(full_path, 'w') as file:
        file.write(content)