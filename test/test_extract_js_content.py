from typing import Union
import pytest
from src.js_extractor import extract_js_content


@pytest.mark.parametrize('content, expected_result', [
    ('var content = "value1"',                      {'content': ['value1']}),
    ('var content="value1";',                       {'content': ['value1']}),
    ('asdf var content = "value1"\\n sde1sfd',      {'content': ['value1']}),
    ('var content = "value1"',                      {'content': ['value1']}),
    ('var content = "8.0";',                          {'content': ['8.0']}),
    ('asdf var content = "8.0" ;asdf',                {'content': ['8.0']}),
])
def test_single_value_extraction(content: str, expected_result: dict[str, str]):
    assert extract_js_content(content) == expected_result


@pytest.mark.parametrize('content, expected_result', [
    ('var content = {"key1": "value1"}', {'content': {'key1': 'value1'}}),
    ('var CONTENT = {"key1": "value1"}', {'CONTENT': {'key1': 'value1'}}),
    ('var c0nt3nt = {"key1": "value1"}', {'c0nt3nt': {'key1': 'value1'}}),
    ('var con_tent = {"key_1": "value_1"}', {'con_tent': {'key_1': 'value_1'}}),
    ('\nvar content = {"key1": "value1"}',   {'content': {'key1': 'value1'}})
])
def test_all_name_kinds(content: str, expected_result: dict[str, str]):
    assert extract_js_content(content) == expected_result

@pytest.mark.parametrize('content',[
    ('var con-tent= {"key1": "value1"}'),
    ('let 1content = {"key1": "value1"}'),
    ('asdfvar = {"key1": "value1"}')
])
def test_false_positive_names(content: str):
    assert extract_js_content(content) == {}

@pytest.mark.parametrize('content, expected_result', [
    ('var content = {"key1": "value1"}',            {'content': {'key1': 'value1'}}),
    ('var content = {"key1": "value1"};',           {'content': {'key1': 'value1'}}),
    ('var content={"key1":"value1"}',               {'content': {'key1': 'value1'}}),
    ('var content={"key1":"value1"};',              {'content': {'key1': 'value1'}}),
    ('adsf var content = {"key1": "value1"};asdf',  {'content': {'key1': 'value1'}})
])
def test_dict_extraction(content: str, expected_result: dict[str, str]):
    assert extract_js_content(content) == expected_result

@pytest.mark.parametrize('content, expected_result', [
    ('var content = {"nest1": {"n1_key1": "n1_value1"}}',                                                   {'content': {'nest1': {'n1_key1': 'n1_value1'}}}),
    ('var content = {"nest1": {"n1_key1": "n1_value1"}, "key1": "value1"}',                                 {'content': {'nest1': {'n1_key1': 'n1_value1'}, 'key1': 'value1'}}),
    ('var content = {"nest1": {"n1_key1": "n1_value1", "n1_key2": "n1_value2"}}',                           {'content': {'nest1': {'n1_key1': 'n1_value1', 'n1_key2': 'n1_value2'}}}),
    ('var content = {"nest1": {"n1_key1": "n1_value1", "n1_key2": "n1_value2"}, "key1": "value1"}',         {'content': {'nest1': {'n1_key1': 'n1_value1', 'n1_key2': 'n1_value2'}, 'key1': 'value1'}}),
    ('var content = {"nest1": {"n1_nest1": {"n1_n1_key1": "n1_n1_value1"}}}',                               {'content': {'nest1': {'n1_nest1': {'n1_n1_key1': 'n1_n1_value1'}}}}),
    ('var content = {"nest1": {"n1_nest1": {"n1_n1_nest1": {"n1_n1_n1_key1": "n1_n1_n1_value1"}}}, "nest2": {"n2_nest1":{"n2_n1_key1": "n2_n2_value1"}}}', 
        {'content': {'nest1': {'n1_nest1': {'n1_n1_nest1': {'n1_n1_n1_key1': 'n1_n1_n1_value1'}}}, 'nest2': {'n2_nest1': {'n2_n1_key1': 'n2_n2_value1'}}}})
])
def test_nested_dict_extraction(content, expected_result: dict[str, str]):
    assert extract_js_content(content) == expected_result


@pytest.mark.parametrize('content, expected_result', [
    ('content = ["ele1", "ele2"]',              {'content': ['ele1', 'ele2']}),
    ('content = ["ele1", "ele2"];',             {'content': ['ele1', 'ele2']}),
    ('content=["ele1", "ele2"]',                {'content': ['ele1', 'ele2']}),
    ('content=["ele1", "ele2"];',               {'content': ['ele1', 'ele2']}),
    ('asdfe content=["ele1", "ele2"];asdfasf',  {'content': ['ele1', 'ele2']}),
])
def test_list_extraction(content: str, expected_result: dict[str, list[str]]):
    assert extract_js_content(content) == expected_result


@pytest.mark.parametrize('content, expected_result', [
    ('content = [["n1_ele1", "n1_ele2"], "ele1"]',                          {'content': [['n1_ele1', 'n1_ele2'], 'ele1']}),
    ('content = [{"n1_key1": "n1_value1"}, "ele1"]',                        {'content': [{'n1_key1': 'n1_value1'}, 'ele1']}),
    ('content = [{"n1_key1": ["n1_ele1", "n1_ele2"]}, ["ele1", "ele2"]]',   {'content': [{'n1_key1': ['n1_ele1', 'n1_ele2']}, ['ele1', 'ele2']]}),
])
def test_nested_list_extraction(content: str, expected_result: list[Union[dict[list[str]], list[str]]]):
    assert extract_js_content(content) == expected_result


@pytest.mark.usefixtures('content_list')
def test_multiple_js_contents(content_list):
    assert extract_js_content(content_list['content']) == content_list['result']

@pytest.mark.usefixtures('content_list')
def test_multiple_parameters(content_list):
    contents_as_list: list[str] = content_list['content']
    content: str = '\n'.join(contents_as_list)
    assert  extract_js_content(content) == content_list['result']