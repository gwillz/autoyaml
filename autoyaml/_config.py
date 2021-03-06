import sys, os, types, yaml, copy
from autoyaml._propattr import PropAttr, validate_all

def create(path, default):
    "Write defaults to config"
    
    validate_all(default)
    
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


def load(path):
    "Load yaml config from file"
    
    with open(path) as f:
        cfg = yaml.load(f)
        
        if not isinstance(cfg, dict):
            raise KeyError("Config file empty, you should delete \"{}\" and try again".format(path))
        
        return cfg



class Config(object):
    "Cache store of the config on import"
    
    def __init__(self, default_config):
        self._config = copy.deepcopy(default_config)
        self._default = default_config
        self._path = None
    
    
    def load_or_create(self, config_path):
        "Load or create config if not found"
        
        if self._path:
            return self
        
        try:
            cfg = load(config_path)
            verify(cfg, self._default)
            self._config.update(cfg)
            
        except FileNotFoundError:
            create(config_path, self._default)
        
        cfg = load(config_path)
        verify(cfg, self._default)
        self._config.update(cfg)
        
        self._path = config_path
        return self
    
    
    def hijack(self, module):
        "Replace calling module with config"
        sys.modules[module['__name__']] = ModuleProps(self._config, self._path, module)
    
    
    def add(self, **kwargs):
        "Add extra configs"
        self._config.update(kwargs)
        return self


class ModuleProps(PropAttr, types.ModuleType):
    def __init__(self, config, path, module):
        self.__doc__ = "Config loaded from '{}'".format(path)
        
        self.__name__ = module['__name__']
        self.__file__ = module['__file__']
        self.__loader__ = module['__loader__']
        self.__package__ = module['__package__']
        self.__spec__ = module['__spec__']
        try:
            self.__path__ = module['__path__']
        except KeyError:
            self.__path__ = os.path.dirname(self.__file__)
        
        PropAttr.__init__(self, config)
    
