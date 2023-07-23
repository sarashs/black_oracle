def remove_unwanted_lines(code):
    lines = code.split('\n')
    # Keep only lines that do not start with triple backticks or "Note:"
    lines = [line for line in lines if not line.strip().startswith('```') and not line.strip().startswith('Note:')]
    return '\n'.join(lines)