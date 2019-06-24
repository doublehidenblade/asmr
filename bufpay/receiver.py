#!/usr/bin/python
#coding=utf8
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
"""
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import logging
import time

PORT_NUMBER = 8080
RES_FILE_DIR = "."

# 接口地址：你传入的 notify_url 参数
# 调用方法：POST
# 调用参数：
#  - aoid, bufpay平台订单唯一标识
#  - order_id, 你传入的 order_id 参数
#  - order_uid, 你传入的 order_uid 参数
#  - price, 订单价格
#  - pay_price, 用户支付的金额
#  - sign, 签名, 参数 aoid + order_id + order_uid + price + pay_price + app secret 顺序拼接后 MD5
#
# 当你收到 BufPay 的回调请求后，如果响应 HTTP code 200 那么 BufPay 会认为通知成功,
# 否则会再次通知 6 次，间隔为 1/2/4/16/64/300 分钟。

class myHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path=="/":
			self.path="/index_example3.html"

		try:
			#根据请求的文件扩展名，设置正确的mime类型
			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#读取相应的静态资源文件，并发送它
				f = open(curdir + sep + self.path, 'rb')
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	def do_POST(self):
		logging.warning(self.headers)
		form = cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={'REQUEST_METHOD':'POST',
					'CONTENT_TYPE':self.headers['Content-Type'].encode(),
					})

		print("name=%s\n" % form.getvalue("name",""))
		print("addr=%s\n" % form.getvalue("addr",""))

		self.send_response(200)
		self.end_headers()
		self.wfile.write("Thanks for you post".encode())

	def get_data_string(self):
		now = time.time()
		clock_now = time.localtime(now)
		cur_time = list(clock_now)
		date_string = "%d-%d-%d-%d-%d-%d" % (cur_time[0],
				cur_time[1],cur_time[2],cur_time[3],cur_time[4],cur_time[5])
		return date_string
try:
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' , PORT_NUMBER)

	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()
# ---------------------
# 作者：maximuszhou
# 来源：CSDN
# 原文：https://blog.csdn.net/MaximusZhou/article/details/39557483
# 版权声明：本文为博主原创文章，转载请附上博文链接！
