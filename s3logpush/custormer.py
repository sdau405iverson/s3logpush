#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-30 下午2:34
from threading import Thread
from run_logger import logger

import os
import hashlib
import botocore
from boto3.session import Session


class Custormer(Thread):
    def __init__(self, push_queue=None, aws_access_key_id=None, aws_secret_access_key=None,
                 endpoint_url=None):
        Thread.__init__(self, )
        self.daemon = True
        self.push_queue = push_queue
        try:
            self.s3_session = Session(aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key)
            self.s3 = self.s3_session.resource('s3', endpoint_url=endpoint_url)
        except Exception as e:
            logger.error(e.message)

    def run(self):
        while True:
            log_meto_info = self.push_queue.get()
            key_md5 = None
            try:
                obj = self.s3.Object(log_meto_info['bucket'], log_meto_info['key'])
                key_md5 = obj.e_tag.strip("'").strip('"')
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    # The object does not exist.
                    self.s3.Object(log_meto_info['bucket'], log_meto_info['key']).put(
                        Body=open(log_meto_info['path'], 'rb'))
                    logger.info('%s成功上传至%s' % (log_meto_info['path'], log_meto_info['key']))
                else:
                    # Something else has gone wrong.
                    logger.error(e.response['Error'])
            else:
                # The object does exist.
                if self.get_md5(log_meto_info['path']) != key_md5:
                    logger.info('%s已存在但与本地文件%s不一致，需要重新上传' % (log_meto_info['key'], log_meto_info['path']))
                    self.s3.Object(log_meto_info['bucket'], log_meto_info['key']).put(
                        Body=open(log_meto_info['path'], 'rb'))
                    logger.info('%s成功重新上传至%s' % (log_meto_info['path'], log_meto_info['key']))
                else:
                    logger.info("%s已存在且与本地文件%s一致" % (log_meto_info['key'], log_meto_info['path']))

            self.push_queue.task_done()

    def get_md5(self, fname):
        hash = hashlib.md5()
        with open(fname) as f:
            for chunk in iter(lambda: f.read(4096), ""):
                hash.update(chunk)
        # return hash.digest().encode('base64').strip()
        return hash.hexdigest()
