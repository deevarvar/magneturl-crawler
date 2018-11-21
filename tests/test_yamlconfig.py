#  -*- encoding =  utf-8 -*-
# author: zhihuaye@gmail.com

import unittest
import sys
import os
curpath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(curpath, '../'))
from utils import YamlConfig, readconf


class TestYamlConfig(unittest.TestCase):
    def setUp(self):
        # call every time
        self.configfile = os.path.join(curpath, 'testdata', 'test.yml')
        self.config = YamlConfig(filename=self.configfile)

    def test_set(self):
        self.config['foo'] = 'Hello'
        newconfig = readconf(cfile=self.configfile)
        self.assertEqual(newconfig['foo'], 'Hello')

    def test_update(self):
        self.config['bar'] = 'Hello'
        self.config['bar'] = 'world!'
        newconfig = readconf(cfile=self.configfile)
        self.assertEqual(newconfig['bar'], 'world!')

    def test_delete(self):
        self.config['foobar'] = "Hello,World!"
        del self.config['foobar']  # self.config.pop('foobar', None)
        newconfig = readconf(cfile=self.configfile)
        self.assertNotIn('foobar', newconfig)


if __name__ == '__main__':
    unittest.main()