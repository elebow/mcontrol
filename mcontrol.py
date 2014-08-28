#!/usr/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess

page = """
<html>
<head>
<script>
	function send(command) {
		xhr = new XMLHttpRequest();
		xhr.open("GET", command, true);
		xhr.send(null);
		return false;
	}
</script>
<style>
table {
	border-collapse: separate;
	border:1px
}
td {
	border: 1px solid;
}
tr {
	height: 50px;
}
.green {
	background: #ddffdd;
}
.gray {
	background: #dddddd;
}
.blue {
	background: #ddddff;
}
</style>
<meta name="viewport" content="width=device-width, user-scalable=no">
</head>
<body>
<table>
<tr>
	<td width="29%">&nbsp;</td>
	<td width="29%" onclick="send('/ossmix -q mplayer -- -1')" class="blue">mpl vol-</td>
	<td width="29%" onclick="send('/ossmix -q mplayer -- +1')" class="blue">mpl vol+</td>
	<td width="13%" onclick="send('/cmd pt_step -1')" class="green">plist -</td>
</tr>
<tr>
	<td onclick="send('/ossmix -q misc.front1 -- +4')" class="blue">vol+</td>
	<td onclick="send('/cmd seek -600')" class="gray">seek -600</td>
	<td onclick="send('/cmd seek +600')" class="gray">seek +600</td>
	<td rowspan="2" onclick="send('/cmd pt_step +1')" class="green">plist +</td>
</tr>
<tr>
	<td onclick="send('/ossmix -q misc.front1 -- -4')" class="blue">vol-</td>
	<td onclick="send('/cmd seek -60')" class="gray">seek -60</td>
	<td onclick="send('/cmd seek +60')" class="gray">seek +60</td>
</tr>
<tr>
	<td onclick="send('/ossmix -q misc.front-mute toggle')" class="blue">mute</td>
	<td onclick="send('/cmd seek -10')" class="gray">seek -10</td>
	<td onclick="send('/cmd seek +10')" class="gray">seek +10</td>
	<td rowspan="2">&nbsp;</td>
</tr>
<tr>
	<td colspan="2" onclick="send('/cmd pause')" class="green">play/pause</td>
	<td>&nbsp;</td>
</tr>
</table>
<table>
<tr style="height:25px"></tr>
<tr>
	<td style="width:40px;text-align:center" onclick="send('/cmd seek -0.05 0 1')" class="gray">F5</td>
	<td style="width:40px;text-align:center" onclick="send('/cmd seek -1 0 1')" class="gray">F6</td>
</tr>
<tr style="height:25px"></tr>
<tr>
	<td style="width:40px;text-align:center" onclick="send('/cmd sub_select')" class="gray">j</td>
	<td style="width:40px;text-align:center" onclick="send('/cmd vo_fullscreen')" class="gray">f</td>
	<td style="width:40px;text-align:center" onclick="send('/cmd sub_visibility')" class="gray">v</td>
	<td style="width:40px;text-align:center" onclick="send('/cmd mute')" class="gray">m</td>
</tr>
</table>
</body>
</html>
""".encode("utf8")

def is_running(process):
	s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
	for x in s.stdout:
		if process in x.decode("utf8"):
			return True
	return False

def mcontrol(command):
	if not is_running("mplayer"):
		return

	#print(command)
	with open("/home/eddie/.mplayer/control.fifo", "w") as fifo:
		fifo.write(command)
		fifo.write("\n")

def ossmix(command):
	s = subprocess.call(("/usr/bin"+command).split(" "))

class RequestHandler(BaseHTTPRequestHandler):
	def _writeheaders(self):
		self.send_response_only(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def do_HEAD(self):
		self._writeheaders()

	def do_GET(self):
		self._writeheaders()
		if self.path == "/":
			self.wfile.write(page)
		else:
			self.path = self.path.replace("%20", " ")
			if self.path.startswith("/cmd"):
				mcontrol(self.path.split(" ", maxsplit=1)[1])
			elif self.path.startswith("/ossmix "):
				ossmix(self.path)
			else:
				print("unknown arg '%s'" % self.path)

srv = HTTPServer(("", 8190), RequestHandler)
srv.serve_forever()
