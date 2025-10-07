"""
Tecт
"""

import unittest

import hello_world


class HelloTestCase(unittest.TestCase):
    """Возвращает 'message'"""

    def test_hello(self):
        """Возвращает 'message'"""
        m = "message"
        self.assertEqual(m, hello_world.text())
