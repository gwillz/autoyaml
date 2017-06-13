import sys, yaml
from autoyaml.propattr import PropAttr

def create(path, default):
    "Write defaults to config"
    
    with open(path, 'w') as f:
        f.write(yaml.dump(default, default_flow_style=False))


def verify(cfg, default, name="root"):
    "Test `cfg` for missing keys against default"
    
    if not isinstance(cfg, dict):
        if isinstance(default, dict):
            raise KeyError("Missing nested config: {}".format(name))
        else:
            return
    
    # test and report missing keys
    key_diff = set(default.keys()).difference(set(cfg.keys()))
    if len(key_diff) > 0:
        raise KeyError("Missing config keys: {}".format(", ".join(key_diff)))
    
    # test sub-dicts
    for k in default:
        verify(cfg[k], default[k], k)


def load(path, default):
    "Load from file, verify and return"
    
    with open(path) as f:
        cfg = yaml.load(f)
        
        if not isinstance(cfg, dict):
            raise KeyError("Config file empty, you should delete \"{}\" and try again".format(path))
        
        verify(cfg, default)
        return cfg



class Config(object):
    "Cache store of the config on import"
    
    def __init__(self, config_path, default_config):
        self._config = {}
        self._default = default_config
        self._path = config_path
        self._additional = 0
    
    
    def load_or_create(self):
        "Load or create config if not found"
        for _ in range(2):
            try:
                if len(self._config) == self._additional:
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
        self._additional += 1
        return self
    
    @staticmethod
    def load_hijack(module_name, path, default):
        "Shorthand for init -> load or create -> hijack"
        return Config(path, default).load_or_create().hijack(module_name)
