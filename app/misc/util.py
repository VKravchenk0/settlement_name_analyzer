import io
import time
import zipfile
from functools import wraps

import jsonpickle
import numpy as np

jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', ensure_ascii=False)

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


def split_into_chunks_and_compress_into_archive(result_dtos, number_of_chunks):
    splitted_list = np.array_split(result_dtos, number_of_chunks)
    inmemory_zip_file = io.BytesIO()
    with zipfile.ZipFile(inmemory_zip_file, 'w') as zf:
        i = 1
        for chunk in splitted_list:
            string_json = jsonpickle.encode(chunk.tolist(), unpicklable=False, indent=2)
            data = zipfile.ZipInfo(str(i) + '.json')
            data.date_time = time.localtime(time.time())[:6]
            data.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data, str.encode(string_json))
            i = i + 1

    inmemory_zip_file.seek(0)
    return inmemory_zip_file


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def split_list(input_list, number_of_parts):
    k, m = divmod(len(input_list), number_of_parts)
    return (input_list[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(number_of_parts))
