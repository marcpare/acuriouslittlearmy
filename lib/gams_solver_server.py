# Server for passing messages to GAMS solvers on remote
# computers. Based on the rpyc chat server.
#
# http://rpyc.wikidot.com/demo:chat

from __future__ import with_statement

from config import *

from rpyc import Service, async
from rpyc.utils.server import ThreadedServer
from threading import RLock

broadcast_lock = RLock()
tokens = set()

class UserToken(object):
	def __init__(self, name, callback):
		self.name = name
		self.stale = False
		self.callback = callback
		# self.broadcast("* Hello %s *" % (self.name,))
		tokens.add(self)

class SolverService(Service):
	def on_connect(self):
		self.token = None

	def on_disconnect(self):
		if self.token:
			self.token.exposed_logout()

	def exposed_login(self, callback):
		print "Did login for dummy."
		
		if self.token and not self.token.stale:
			raise ValueError("already logged in")
		
		self.token = UserToken("Dummy", async(callback))
		return self.token
		
	def exposed_run_analysis(self, analysis_code):
		print "Trying to run analysis in the server."
		
		# grab one of the solver clients to process this
		global tokens
		stale = set()
		with broadcast_lock:
			for tok in tokens:
				try:
					return tok.callback(analysis_code)
				except:
					stale.add(tok)
					tokens -= stale
		
		return "Failed to find solver."
		
	def exposed_process_results(self, analysis_results):
		print "Alert the interested worker with the results"
		print "Here they are: "
		print analysis_results
				
if __name__ == "__main__":
	t = ThreadedServer(SolverService, port=GAMS_PORT)
	t.start()