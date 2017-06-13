import unittest
from autoyaml import PropAttr

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

class PropAttr_validate_test(unittest.TestCase):
    def test(self):
        self.assertRaises(KeyError, lambda: PropAttr.validate_key("bad key"))
        self.assertRaises(KeyError, lambda: PropAttr.validate_key("123"))
        self.assertRaises(KeyError, lambda: PropAttr.validate_key(5.5))
