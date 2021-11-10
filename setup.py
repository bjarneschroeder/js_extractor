from distutils.core import setup
setup(
  name = 'js_extractor',         
  packages = ['js_extractor'],   
  version = '0.1',      
  license='MIT',        
  description = 'Find JavaScript Variables, Dicts and Lists in a String and parse them with their content into a Python Dictionary',   # Give a short description about your library
  author = 'Bjarne Schroeder',                   
  author_email = 'schroeder.bjarne97@gmail.com',      
  url = 'https://github.com/bjarneschroeder/js_extractor',   
  download_url = 'https://github.com/bjarneschroeder/js_extractor/archive/refs/tags/v_01.tar.gz',    # I explain this later on
  keywords = ['scraping', 'parsing', 'python', 'extracting', 'javascript'],   # Keywords that define your package best
  install_requires=[
        'atomicwrites',
        'attrs',
        'chompjs',
        'colorama',
        'iniconfig',
        'packaging',
        'pluggy',
        'py',
        'pyparsing',
        'pytest',
        'regex',
        'toml'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Scraping',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)