import unittest
from autoyaml._propattr import PropAttr, validate_key, validate_all

class PropAttr_test(unittest.TestCase):
    def setUp(self):
        self.config = PropAttr({
            "one": 1,
            "two": 2,
            "nested": {
                "another": True,
                "bool": False,
                "nest_again": {
                    "hello": "world"
                }
            }
        })
    
    def tearDown(self):
        del self.config
    
    def test(self):
        self.assertEqual(self.config.one, 1)
        self.assertEqual(self.config.two, 2)
        self.assertEqual(self.config.nested.another, True)
        self.assertEqual(self.config.nested.bool, False)
        self.assertEqual(self.config.nested.nest_again.hello, "world")
    
    def test_str(self):
        self.assertEqual(str(self.config), "root => nested, one, two")
        self.assertEqual(str(self.config.nested), "nested => another, bool, nest_again")
        self.assertEqual(str(self.config.nested.nest_again), "nest_again => hello")
    
    def test_iter(self):
        # print(self.config.nested)
        
        expected = {
            "another": True,
            "bool": False,
            "nest_again": PropAttr({"hello": "world"}, "nest_again")
        }
        self.assertEqual(dict(self.config.nested), expected)

class PropAttr_validate_test(unittest.TestCase):
    def test_key(self):
        self.assertRaises(KeyError, lambda: validate_key("bad key"))
        self.assertRaises(KeyError, lambda: validate_key("123"))
        self.assertRaises(KeyError, lambda: validate_key(5.5))
    
    def test_all(self):
        CONFIG = {
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
        self.assertEqual(validate_all(CONFIG), None)
