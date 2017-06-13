from autoyaml._config import Config, verify
from autoyaml._propattr import PropAttr, validate_key, validate_all

def load_hijack(module_name, path, default):
    "Shorthand for init -> load or create -> hijack"
    return Config(path, default).load_or_create().hijack(module_name)
