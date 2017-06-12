class PropAttr(object):
    "Recursively convert dictionaries, so [attr] becomes .attr"
    
    def __init__(self, props, name="root"):
        self._name = name
        self._props = props
        
        for k in props:
            if isinstance(props[k], dict):
                self._props[k] = PropAttr(props[k], k)
    
    def __getattr__(self, item):
        return self._props[item]
    
    def __str__(self):
        return "Config: {} => {}".format(self._name, ", ".join(self._props.keys()))
    __unicode__ = __str__
    __repr__ = __str__
