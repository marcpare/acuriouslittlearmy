# Connects to GAMS solver server. Runs analysis, sends back results

from config import *
import rpyc
import threading

class SolverClient(object):
	def __init__(self):
		self.conn = None

	def disconnect(self):
		if self.conn:
			self.conn.close()
			self.conn = None

	def on_close(self, widget):
		self.disconnect()

	#
	# connect/disconnect logic
	#
	def connect(self, data = None):
		try:
			self.conn = rpyc.connect(GAMS_SERVER, GAMS_PORT)
		except Exception:
			self.conn = None
			return

		try:
			# pass the server a callback function
			self.conn.root.login(self.on_message)
		except ValueError:
			self.conn.close()
			self.conn = None
			return

	#
	# called by the reactor whenever the connection has something to say
	#
	def bg_server(self, source = None, cond = None):
		print "Started GAMS solver client."
		while True:
			if self.conn:
				self.conn.poll_all()

	#
	# called by the server, with the request to run an analysis
	#
	def on_message(self, analysis_code):
		print "Just ran analysis"
		self.conn.root.process_results("This is a GAMS solution to the following code: \n" + analysis_code)

if __name__ == "__main__":
	solver_client = SolverClient()
	solver_client.connect()
	t = threading.Thread(target=solver_client.bg_server)
	#t.setDaemon(True)
	t.start()