from autoyaml._config import Config, verify
from autoyaml._propattr import PropAttr, validate_key, validate_all

def load_hijack(module, path, default):
    "Shorthand for init -> load or create -> hijack"
    return Config(default).load_or_create(path).hijack(module)
