import regex 
from typing import Union

import chompjs

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