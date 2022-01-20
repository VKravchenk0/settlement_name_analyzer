latin_replacement_dict = {
    'a': 'а',
    'o': 'о',
    'e': 'е',
    'i': 'і',
    'y': 'у',
    'c': 'с',
    'k': 'к',
    'p': 'р',
    'x': 'х',
    'A': 'А',
    'O': 'О',
    'E': 'Е',
    'I': 'І',
    'Y': 'У',
    'C': 'С',
    'K': 'К',
    'P': 'Р',
    'X': 'Х',
    'M': 'М',
    'H': 'Н',
    'T': 'Т',
    'B': 'В'
}


def replace_latin_letters_with_cyrillic(string):
    result = string
    for latin_letter, cyrillic_letter in latin_replacement_dict.items():
        result = result.replace(latin_letter, cyrillic_letter)
    return result


def replace_apostrophe(string):
    return string.replace('’', "'")
