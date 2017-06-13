import sys, yaml
from autoyaml.propattr import PropAttr

def create(path, default):
    "Write defaults to config"
    
    with open(path, 'w') as f:
        f.write(yaml.dump(default, default_flow_style=False))


def verify(cfg, default):
    "Test `cfg` for missing keys against default"
    
    if cfg is None:
        raise KeyError("Config file empty, you should delete \"{}\" and try again".format(CONFIG_PATH))
    
    # test and report missing keys
    key_diff = set(default.keys()).difference(set(cfg.keys()))
    if len(key_diff) > 0:
        raise KeyError("Missing config keys: {}".format(", ".join(key_diff)))
    
    # test sub-dicts
    try:
        for k in default:
            if isinstance(default[k], dict):
                verify(cfg[k], default[k])
    except KeyError as e:
        e.args = ("Missing config key: {}".format(k),)
        raise e


def load(path, default):
    "Load from file, verify and return"
    
    with open(path) as f:
        cfg = yaml.load(f)
        verify(cfg, default)
        return cfg



class Config(object):
    "Cache store of the config on import"
    
    def __init__(self, config_path, default_config):
        self._config = {}
        self._default = default_config
        self._path = config_path
    
    
    def load_or_create(self):
        "Load or create config if not found"
        for _ in range(2):
            try:
                if len(self._config) == 0:
                    self._config.update(load(self._path, self._default))
                    break
            except FileNotFoundError:
                create(self._path, self._default)
        
        return self
    
    
    def hijack(self, module_name):
        "Replace calling module with config"
        sys.modules[module_name] = PropAttr(self._config)
    
    
    def add(self, **kwargs):
        "Add extra configs"
        self._config.update(kwargs)
        return self
    
    @staticmethod
    def load_hijack(module_name, path, default):
        "Shorthand for init -> load or create -> hijack"
        return Config(path, default).load_or_create().hijack(module_name)
