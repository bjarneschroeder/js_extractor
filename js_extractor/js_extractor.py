import regex 
from typing import Union

import chompjs
import re

regex.Default_VERSION = regex.VERSION0

def extract_js_content(content: Union[list, str]) -> dict[str, Union[dict, list, str]]:
    """
    Extracts from scraped JavaScript content, which is either a list of strings
    or a single string, all dictionaries and lists and parses them
    to Python lists or dictionaries.

    The result is a dictionary containing the name of the var as the key and 
    the parsed content as value.


    Args:
        content (Union[str, list[str]]): List of strings or a single string that
                                         contain JavaScript code.

    Raises:
        ValueError: If there is already a parsed object in the result dictionary with
                    the identical name. Might be handeld in a later version.

    Returns:
        dict[str, Union[dict, list]]: Dict containing the name of the var as the key and
                                      its content as value.
    """

    js_var_exp: str = r'(?:_|\$|\p{L})+[\$_\w]*'

    single_val_exp: str = fr'\s*(?:var|let|const)\s+{js_var_exp}\s*=\s*(?:".*?"|\d+(?:\.\d)*)\s*'
    dict_exp: str = fr'((?:var|let|const)\s+{js_var_exp}\s*=\s*(\{{[^\\}}\{{]*+(?:(?2)[^\}}\{{]*)*+\}}))'
    list_exp: str = fr'(\s*{js_var_exp}\s*=+\s*(\[[^\]\[]*+(?:(?2)[^\]\[]*)*+\]))'

    
    if type(content) == str:
        content = [content]

    js_objects: list[str] = []

    content = [item.replace('\n', ' ') for item in content]
    
    for item in content:
        single_values: list[str] = regex.findall(single_val_exp, item, regex.DOTALL)
        for single_value in single_values:
            eq_pos = single_value.find('=')+1
            js_objects.append(single_value[:eq_pos] + '[' + single_value[eq_pos:] + ']') #so its valid json

        for expression in [list_exp, dict_exp]:
            js_objects.extend([result[0] for result in regex.findall(expression, item, regex.DOTALL)])

        
    results: dict[str, Union[dict, list]] = {}
    for obj in js_objects:
        parsed_obj = chompjs.parse_js_object(obj)

        declar_split = obj.split('=')[0].lstrip()
        if declar_split[:4] == 'var ': #note the space so strings like "variable" are false
            obj_name = declar_split.split(' ')[1].strip()
        else:
            obj_name = declar_split.strip()

        if obj_name in results.keys():
            #todo: what to do here?
            raise ValueError('Object Name already parsed.')
        else:
            results[obj_name] = parsed_obj

    return results


def get_by_borders(string : str, start_string : str = "", end_string : str = "", remove_string : bool = False) -> list[str]:
    '''

    :param string: string to extract from
    :param start_string: the left border from the content to extract
    :param end_string: the right border from the content to extract
    :param remove_string: if true the left and right border gets removed from the result string
    :return: a list with the extracted strings
    '''

    regex : str = f"{start_string}(?:(?:\(.*?\))|(?:[^\(\)]*?)){end_string}"
    result : list = re.findall(regex, string)
    if remove_string:
        result : list = list(map(lambda x: x.replace(start_string, "").replace(end_string, ""), result))
    return result