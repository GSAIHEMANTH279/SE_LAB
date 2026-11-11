import math


def _to_number(text):
    """Convert text to a finite float, or return None if that is not possible."""
    try:
        number = float(text)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):  # rejects 'nan', 'inf' and overflow like '1e400'
        return None
    return number


def parse_declaration(text):
    """Parse 'category:value'. Returns (category, value) or None if invalid."""
    if not isinstance(text, str) or text.count(':') != 1:
        return None
    category, value = text.split(':')
    category = category.strip().lower()
    value = _to_number(value)
    if not category or value is None or value < 0:
        return None
    return category, value


def duty_amount(text):
    """Parse 'value@rate' and return the duty, or None if invalid."""
    if not isinstance(text, str) or text.count('@') != 1:
        return None
    value, rate = (_to_number(part) for part in text.split('@'))
    if value is None or rate is None or value < 0 or not 0 <= rate <= 100:
        return None
    return value * (rate / 100)  # rate / 100 <= 1, so this cannot overflow


def hs_chapter(code):
    """Return the chapter (01-97) of an HS code like '8517.12', or None if invalid."""
    if not isinstance(code, str):
        return None
    heading = code.strip().split('.')[0]
    if len(heading) < 2 or not (heading.isascii() and heading.isdigit()):
        return None
    chapter = int(heading[:2])
    if not 1 <= chapter <= 97:
        return None
    return chapter


def main():
    print("==== Running parse_declaration ====")
    user_input = input("Enter category:value (e.g. electronics:25000): ")
    result = parse_declaration(user_input)
    if result is None:
        print("Invalid declaration: use category:value with a non-negative number")
    else:
        print("Category and Value:", result)

    print("\n==== Running duty_amount ====")
    user_input = input("Enter value@rate (e.g. 25000@20): ")
    result = duty_amount(user_input)
    if result is None:
        print("Invalid input: use value@rate with value >= 0 and rate between 0 and 100")
    else:
        print("Duty Amount:", result)

    print("\n==== Running hs_chapter ====")
    user_input = input("Enter an HS code (e.g. 8517.12): ")
    result = hs_chapter(user_input)
    if result is None:
        print("Invalid HS code: it must start with a 2-digit chapter from 01 to 97")
    else:
        print("Chapter:", result)


if __name__ == "__main__":
    main()
