FORMATTER = {
    "italic": "_",
    "bold": "*",
    "strike": "~",
    "mono": "`",
    "spoiler": "||",
    "lineBreak": "\n"
}


def text_formatter(text):
    all_special_chars = ["\\", '+', '-', "'", '"', "^", ".", ",", "!", "*", "_", "~", "`", "/", ";", "?", "<", ">", "]", "[", ":", "@", "#", "$", "%", "&", "(", ")"]
    try:
        for sc in all_special_chars:
            text = text.replace(sc, f'\\{sc}')

        for f in FORMATTER:
            current_format = '{' + f + '}'

            if current_format in text:
                text = text.replace(current_format, FORMATTER[f])

        text = text.replace('{', '\\{')
        text = text.replace('}', '\\}')

        return text
    except Exception:
        return text


def money_formatter(value : float):
    try:
        value = f"{value:.2f}"
        return value
    except ValueError as ve:
        formatted_value = f"{float(value):.2f}"
        return formatted_value
