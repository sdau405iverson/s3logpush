#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-31 上午10:01
import sys
import os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.realpath(__file__)),'site-packages'))
from s3logpush import s3logpush
import json
print json.__file__

if __name__ == '__main__':
    s3logpush.run()
