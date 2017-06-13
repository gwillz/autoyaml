import re

class PropAttr(object):
    "Recursively convert dictionaries, so [attr] becomes .attr"
    
    @staticmethod
    def validate_key(key):
        if not isinstance(key, str):
            raise KeyError("Invalid key '{}', only accepts string types".format(key))
        
        elif re.match(r'.*[^a-zA-Z_].*', key):
            raise KeyError("Invalid key '{}', only accepts [a-zA-Z_]".format(key))
    
    def __init__(self, props, name="root"):
        self._name = name
        self._props = props
        
        for k in props:
            PropAttr.validate_key(k)
            
            if isinstance(props[k], dict):
                self._props[k] = PropAttr(props[k], k)
    
    def __getattr__(self, item):
        "Get config by key"
        return self._props[item]
    __getitem__ = __getattr__
    
    def __str__(self):
        return "{} => {}".format(self._name, ", ".join(sorted(self._props.keys())))
    __unicode__ = __str__
    
    def __repr__(self): # pragma: no cover
        return repr(self._props)
