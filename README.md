# Introduction
This package enables you to extract JavaScript Variables, Arrays and Dictionaries 
from a given String containing JavaScript code with one method call.
The result is a Python Dictionary which contains the variable names as keys and 
the stored content as the value.
This is useful for obtaining information stored in the JavaScript content of websites 
one is maybe scraping.
The package uses [chompjs](https://github.com/Nykakin/chompjs) for parsing the extracted content into Python.
I recommend reading the documentation of [chompjs](https://github.com/Nykakin/chompjs) since this
package underlies the same limitations.
The search for JavaScript Dictionaries, Arrays and Variables is done with regex. 

## Usage
### Extracting Dictionaries:
```python
from js_extractor import extract_js_content

content: str = 'random jscode.... var variable = {"name": "court", "age": "24"} ....random js code'

result: dict = extract_js_content(content)
print(result)
{'variable': {'name': 'court', 'age': '24'}}

print(result['variable']['name'])
court 
```

### Extracting Arrays:
```python
from js_extractor import extract_js_content

content: str = 'random jscode... array = [{"key1": "value1"}, {"key2": "value2"}]...'

result: dict = extract_js_content(content)
print(result)
{'array': [
    {'key1': 'value1'},
    {'key2': 'value2'}
]}
```

### Extracting single values:
Because [chompjs](https://github.com/Nykakin/chompjs) needs valid JSON to succesfully parse a string, single values will be wrapped in a list.
```python
from js_extractor import extract_js_content

content: str = 'random jscode.... var variable = "hallo" ....random js code'

result: dict = extract_js_content(content)
print(result)
{'variable': ["hallo"]}

print(result['variable'][0])
hallo
```

### Using a list of JavaScript content strings as input:
Often JavaScript content is all over the place in scraped websites and appears in multiple tags.
You don't have to concat all the content into one string.
**extract_js_content** can also take a list of strings and generate one result dictionary.
Note that currently a ValueError is thrown when a variable name apperas twice.
```python
from js_extractor import extract_js_content

content: list[str] = [
    'random jscode.... var variable = "hallo" ....random js code',
    'random jscode.... let dictionary = {"key1": "value1"} ....random js code',
    'random jscode.... let list_value = ["this", "is", "cool"] ....random js code',
]

result: dict = extract_js_content(content)
print(result)
{ 'variable': [
        "hallo"
  ],
  'dictionary': {
        'key1': 'value1'
  },
  'list_values': [
        'this',
        'is',
        'cool'
  ]
}
```


# Installation
Installation via PyPi is recommended. You can install the package in your environment via:
```
pip install js_extractor
```

# Notes
This is the first time I distribute code, so please forgive me the rookie mistakes.  
¯\\_(ツ)_/¯