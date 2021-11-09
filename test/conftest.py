import pytest
from typing import Union


@pytest.fixture
def content_list() -> dict[str, Union[list, dict]]:
    contents: list[str] = [
        'adsf var content = {"key1": "value1"};asdf',
        'asdfe content2=["ele1", "ele2"];asdfasf',
        'content3 = [{"n1_key1": ["n1_ele1", "n1_ele2"]}, ["ele1", "ele2"]]',
        'var content4 = {"nest1": {"n1_nest1": {"n1_n1_key1": "n1_n1_value1", "n1_n1_key2": ["n1_n1_ele1", "n1_n1_ele2"]}}}'
        'var content5 = ["ele1"]'
    ]

    result: dict['str', Union[dict, list, str]] = {
        'content': {
            'key1': 'value1'
        },
        'content2': [
            'ele1', 
            'ele2'
        ],
        'content3': [
            {'n1_key1': ['n1_ele1', 'n1_ele2']}, 
            ['ele1', 'ele2']
        ],
        'content4': {
            'nest1': {
                'n1_nest1': {
                    'n1_n1_key1': 'n1_n1_value1',
                    'n1_n1_key2': ["n1_n1_ele1", "n1_n1_ele2"]
                }
            }
        },
        'content5': ['ele1']
    }

    return {'content': contents, 'result': result}