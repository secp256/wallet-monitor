#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import urllib2
import urllib
import time
import os

WITNESS_URL = "http://localhost:8645"
#curl -H "Content-Type: application/json"  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' http://localhost:8645
POST_DATA = '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'

WECHAT_NOTIFY_URL = "http://172.19.19.49:8091/notify/wechat/send?message=%s&agent=GXCHAIN"
NO_RESULT_MSG = "ETH钱包同步节点监控程序，无法获取最新区块号, 错误信息:"
WARNING_MSG = "ETH钱包同步节点，最新区块号30分钟无更新，当前区块头:"

def download(url, data = None, headers = {}):
  opener = urllib2.build_opener()
  request = urllib2.Request(url, data)
 
  # set headers
  for key, value in headers.items():
    request.add_header(key, value)
 
  response = opener.open(request, timeout=100)
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
  for i in xrange(10):
    try:
      res =  download(WITNESS_URL, POST_DATA, {"Content-Type":"application/json"})
      js = json.loads(res)
      head_block_num = int(js['result'], 16)
      print head_block_num

      old_head_block_num = read_head_block_num()

      if int(head_block_num) == int(old_head_block_num):
        error_msg = "%s %d " % (WARNING_MSG, int(head_block_num))
        print error_msg
        time.sleep(10)
      else:
        write_head_block_num(str(head_block_num))
        error_msg = ""
        break
    except Exception as e:
      error_msg = NO_RESULT_MSG + str(e)
      print error_msg
      time.sleep(10)
      continue
  return error_msg

def main():
  # get error_msg
  error_msg = check_node_sync_status()
  if (len(error_msg)) > 0:
    print "restart eth node ..."
    # os.system('/root/opt/eth/start.sh')
    error_msg = check_node_sync_status()

  # send error_msg
  if len(error_msg) > 0:
    notify_url = WECHAT_NOTIFY_URL % (urllib.quote(error_msg))
    print notify_url
    #download(notify_url)

if __name__ == "__main__":
  main()
