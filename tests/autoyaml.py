import unittest, types, os, sys
from autoyaml._config import Config, create, verify, load

CONFIG_PATH = os.sep.join([os.getenv("HOME"), ".autoyaml.yml"])
CONFIG_DEFAULTS = {
    "one": 1,
    "two": 2,
    "nested": {
        "another": True,
        "bool": False,
        "nest_again": {
            "hello": "world"
        }
    }
}
ALT_CONFIG = {
    "one": 5,
    "two": 5,
    "nested": {
        "another": 5,
        "bool": 5,
        "nest_again": {
            "hello": 5
        }
    }
}

class PropAttr_test(unittest.TestCase):
    def setUp(self):
        class config(types.ModuleType):
            import autoyaml
            
            PATH = CONFIG_PATH
            DEFAULTS = CONFIG_DEFAULTS
            __name__ = "config"
            __file__ = "mock/file.py"
            __loader__ = 'mock_loader'
            __package__ = "mock_package"
            __spec__ = "mock_spec"
            autoyaml.load_hijack(locals(), PATH, DEFAULTS)
    
    def tearDown(self):
        os.remove(CONFIG_PATH)
    
    def test(self):
        config = sys.modules['config']
        
        self.assertEqual(config.one, 1)
        self.assertEqual(config.two, 2)
        self.assertEqual(config.nested.another, True)
        self.assertEqual(config.nested.bool, False)
        self.assertEqual(config.nested.nest_again.hello, "world")


class PropAttr_helpers_test(unittest.TestCase):
    def tearDown(self):
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)
    
    def test_verify(self):
        cfg = {
            "one": 1,
            "two": 2,
            "nested": {
                "another": True,
                "bool": False,
                "nest_again": {
                    "hello": "world"
                }
            }
        }
        actual = verify(cfg, CONFIG_DEFAULTS)
        expected = None
        
        self.assertEqual(actual, expected)
    
    def test_verify_missing(self):
        def actual():
            verify({
                "one": 1,
                "two": 2
            }, CONFIG_DEFAULTS)
        
        self.assertRaises(KeyError, actual)
    
    def test_verify_bad_nested(self):
        expected = {
            "one": None,
            "two": 2,
            "nested": 'lol'
        }
        def actual():
            verify(expected, CONFIG_DEFAULTS)
        
        self.assertRaises(KeyError, actual)
    
    def test_bad_load(self):
        with open(CONFIG_PATH, 'w') as f:
            f.write("")
        
        def actual():
            load(CONFIG_PATH, CONFIG_DEFAULTS)
        
        self.assertRaises(KeyError, actual)
    
    def test_create_load(self):
        create(CONFIG_PATH, ALT_CONFIG)
        
        self.assertTrue(os.path.exists(CONFIG_PATH))
        self.assertEqual(load(CONFIG_PATH, CONFIG_DEFAULTS), ALT_CONFIG)
    
    def test_config_add(self):
        actual = Config(CONFIG_PATH, CONFIG_DEFAULTS).add(added='this').load_or_create()
        expected = ['one', 'two', 'nested', 'added']
        
        self.assertTrue(sum(k in actual._config for k in expected) == len(expected))
        self.assertEqual(actual._config['added'], 'this')
        
    
    
