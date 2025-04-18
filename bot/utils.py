import ast


def extract_elements(value: str) -> tuple[str, int]:
    parsed_tuple = ast.literal_eval(value)
    name = parsed_tuple[0]
    number = int(parsed_tuple[1])
    return name, number


def title_check(text: str) -> str:
    if len(text) <= 50:
        return text
    raise ValueError
