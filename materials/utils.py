from string import punctuation, whitespace

def transliterate(string):
    text = string.lower()  # приводим все к нижнему регистру



    # Убираем все знаки пунктуации и "невидимые" символы (табы, пробелы и т.д.)
    for c in punctuation + whitespace:
        text = text.replace(c, '')

    # Дальше словарь только для транслитерации
    # (он ровно в 3 раза меньше чем ваш исходный словарь)
    alph = {
        "й": "j", "ц": "c", "у": "u", "к": "k", "е": "e", "н": "n",
        "г": "g", "ш": "sh", "щ": "shch", "з": "z", "х": "h", "ъ": "",
        "ф": "f", "ы": "y", "в": "v", "а": "a", "п": "p", "р": "r",
        "о": "o", "л": "l", "д": "d", "ж": "zh", "э": "e",
        "я": "ya", "ч": "ch", "с": "s", "м": "m", "и": "i",
        "т": "t", "ь": "", "б": "b", "ю": "yu"
    }

    for c, r in alph.items():
        text = text.replace(c, r)

    return text

