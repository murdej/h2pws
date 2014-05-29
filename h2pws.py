import time
import BaseHTTPServer

#1630-1800

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000 # Maybe set this to 9000.


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_GET(s):
		"""Respond to a GET request."""
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write("<html><head><title></title></head>")
		s.wfile.write("<body><p>Send html source by POST.</p>")
		# s.wfile.write("<p>You accessed path: %s</p>" % s.path)
		s.wfile.write("</body></html>")
	def do_POST(s):
		"""Respond to a POST request."""
		s.send_response(200)
		s.send_header("Content-type", "application/x-pdf")
		s.end_headers()
		
		html = s.rfile.read(int(s.headers.getheader('content-length')))
		import subprocess
		p = subprocess.Popen(["wkhtmltopdf", "-", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		p.stdin.write(html)
		p.stdin.close()
		
		s.wfile.write(p.stdout.read())
		p.wait()

if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)