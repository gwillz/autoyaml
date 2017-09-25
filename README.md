AutoYAML
============================

![build status](https://git.mk2es.com.au/gwillz/autoyaml/badges/master/build.svg)
![coverage report](https://git.mk2es.com.au/gwillz/autoyaml/badges/master/coverage.svg)

A thing that neatly loads config files as nested modules.

- creates the default config file if needed
- throws `KeyError` on variations from the default config
- hides away ugly dicts and excessive configuration
- read-only access to config properties

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

# shorthand
Config.load_hijack(__name__, PATH, DEFAULTS)

# OR

# the .add() call is useful for inserting configs that are dynamic
Config(DEFAULTS).load_or_create(PATH).add(extra=(1+3)).hijack(globals())

# OR

# to not save/load a config file, useful for testing
Config(DEFAULTS).hijack(globals())

```


Then use it in your project like so:

```py
from project import config

config.something.etc # => 1234
config.more          # => 'and more'
config.settings      # => True
config.extra         # => 4

```
