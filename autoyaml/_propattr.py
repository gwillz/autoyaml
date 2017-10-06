import re

def validate_key(key):
    "Ensure a key can be used as an .attr - ie. matches [a-zA-Z_]"
    
    if not isinstance(key, str):
        raise KeyError("Invalid key '{}', only accepts string types".format(key))
    
    elif not re.match(r'^[^0-9\-_][a-zA-Z0-9\-_]+$', key):
        raise KeyError("Invalid key '{}', only accepts alphanumeric and must not start with (0-9,-,_)".format(key))


def validate_all(cfg):
    "validate all keys in cfg, matching [a-zA-Z_]"
    
    for k in cfg:
        validate_key(k)
        if isinstance(cfg[k], dict):
            validate_all(cfg[k])


class PropAttr(object):
    "Recursively convert dictionaries, so [attr] becomes .attr"
    
    def __init__(self, props, name="root"):
        self._name = name
        self._props = props
        
        for k in props:
            validate_key(k)
            
            if isinstance(props[k], dict):
                self._props[k] = PropAttr(props[k], k)
    
    def __getattr__(self, item):
        "Get config by key"
        return self._props[item]
    __getitem__ = __getattr__
    
    def __iter__(self):
        for k in self._props:
            yield k, self._props[k]
    
    def __eq__(self, other):
        return self._props == other._props
    
    def __str__(self):
        return "{} => {}".format(self._name, ", ".join(sorted(self._props.keys())))
    __unicode__ = __str__
    
    def __repr__(self): # pragma: no cover
        return "<PropAttr: {}>".format(str(self))
