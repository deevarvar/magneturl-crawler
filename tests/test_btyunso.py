#  -*- encoding =  utf-8 -*-
# author: zhihuaye@gmail.com

import unittest
from utils import logger

class TestBtyunso(unittest.TestCase):
    BTDOMAIN = 'www.btyunsou.co'
    NORMALURL = ''.join(['http://', BTDOMAIN])  # "http://www.btyunsou.co"
    def test_queryurl(self):
        self.assertEqual('foo'.upper(), 'FOO')
        logger.info('run one case...')

if __name__ == '__main__':
    unittest.main()