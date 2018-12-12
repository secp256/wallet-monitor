#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import urllib2
import urllib
import time
import os

WITNESS_URL = "http://127.0.0.1:8888/v1/chain/get_info"

WECHAT_NOTIFY_URL = "http://172.19.19.49:8091/notify/wechat/send?message=%s&agent=GXCHAIN"
NO_RESULT_MSG = "EOS钱包同步节点监控程序，无法获取最新区块号, 错误信息:"
WARNING_MSG = "EOS钱包同步节点，最新区块号10分钟无更新，当前区块头时间:"

def download(url, data = None):
  opener = urllib2.build_opener()
  request = urllib2.Request(url, data)
  response = opener.open(request, timeout=60)
  return response.read()

def write_head_block_num(content):
    fp = open("/root/opt/monitor/head_block_num.txt", "w")
    fp.write(content)
    fp.close()

def read_head_block_num():
    fp = open("/root/opt/monitor/head_block_num.txt", "r")
    res =  fp.readline()
    fp.close()
    return res.strip()

def check_node_sync_status():
  error_msg = ""
  for i in xrange(15):
    try:
      res =  download(WITNESS_URL)
      js = json.loads(res)
      head_block_num = js['head_block_num']
      head_block_time = js['head_block_time']

      old_head_block_num = read_head_block_num()
      print old_head_block_num
      print head_block_num

      if int(head_block_num) == int(old_head_block_num):
        error_msg = "%s %d %s" % (WARNING_MSG, int(head_block_num), str(head_block_time))
      else:
        write_head_block_num(str(head_block_num))
      error_msg = ""
      break
    except Exception as e:
      error_msg = NO_RESULT_MSG + str(e)
      print i, error_msg
      time.sleep(10)
      continue
  return error_msg

def main():
  # get error_msg
  error_msg = check_node_sync_status()
  if (len(error_msg)) > 0:
    os.system('/root/opt/eos/start.sh')
  error_msg = check_node_sync_status()

  # send error_msg
  if len(error_msg) > 0:
    notify_url = WECHAT_NOTIFY_URL % (urllib.quote(error_msg))
    print notify_url
    download(notify_url)

if __name__ == "__main__":
  main()
