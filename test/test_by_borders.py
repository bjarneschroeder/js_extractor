"""
Tests:
    1:
     input :'cart = new Cart({'geetings': 'Hallo', 'id':1})'
     call  : get_by_borders(input, '{', '}')
     expected : [{'geetings': 'Hallo', 'id':1}]

    2:
     input : 'first: {'geetings': 'Hallo', 'id':1}, second: {'geetings': 'Wie gehts?', 'id':2}'
     call  : get_by_borders(input, '{', '}', True)
     expected : [{'geetings': 'Hallo', 'id':1}, {'geetings': 'Wie gehts?', 'id':2}]
"""