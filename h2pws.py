import time
import BaseHTTPServer
from urlparse import urlparse, parse_qs
import subprocess
import base64 
import qrcode
import qrcode.image.svg
import cStringIO

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
		
		# params
		url_params = parse_qs(urlparse(s.path).query)
		args = ["wkhtmltopdf"]
		for n in [ 'orientation', 'page-size', 'margin-bottom', 'margin-left', 'margin-right', 'margin-top' ]:
			if n in url_params:
				args += [ '--' + n, url_params[n][0] ]
		args += ["-", "-"]
		print args
		html = s.rfile.read(int(s.headers.getheader('content-length')))
		# Replace "qr::xxxxxxxxxxxxxxxxx" to sql qr code
		if "qr-to-svg" in url_params :
			new_html = ''
			pos = 0
			while True:
				begin_str = '"qr::'
				pos_a = html.find(begin_str, pos)
				if pos_a == -1: break
				# copy text before
				new_html += html[pos:pos_a]
				# extract src of QR code
				pos_a += len(begin_str)
				pos_b = html.find('"', pos_a + 1)
				qr_src = html[pos_a:pos_b]
				print "qr:src='" + qr_src + "'"

				# new_html += '[[' + qr_src + ']]'
				factory = qrcode.image.svg.SvgPathImage
				img = qrcode.make(qr_src, image_factory=factory)
				output = cStringIO.StringIO()
				img.save(output)
				svgb = 'data:image/svg+xml;base64,' + base64.b64encode(output.getvalue())
				output.close()
				new_html += svgb
				pos = pos_b

			new_html += html[pos:]
			html = new_html

		p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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