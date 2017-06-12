AutoYAML
============================

![build status](https://git.mk2es.com.au/gwillz/autoyaml/badges/master/build.svg)
![coverage report](https://git.mk2es.com.au/gwillz/autoyaml/badges/master/coverage.svg)

A thing that neatly loads config files as nested modules. No dicts or nothing.

- creates the default config file if needed
- throws `IOError`s on variations from the default config
- hides away ugly dicts and excessive configuration


## Usage

First create a `config.py` or whatever in your project.

```py
from autoyaml import Config

PATH = 'config/anywhere.yml'
DEFAULTS = {
    'something': {
        'etc': 1234,
        'thing': False
    },
    'more': 'and more',
    'settings': True
}

Config.load_hijack(__name__, PATH, DEFAULTS)

# OR

Config(PATH, DEFAULTS)\
.load_or_create()\
.add(extra=(1+3))\
.hijack(__name__)
# the .add() call is useful for inserting configs that are dynamic
```


Then use it in your project like so:

```py
from project import config

config.something.etc # => 1234
config.more          # => 'and more'
config.settings      # => True
config.extra         # => 4
```
