import threading
import beanstalkc

beanstalk = beanstalkc.Connection(host=BEANSTALK_HOST, port=BEANSTALK_PORT)

def do_job(job):
	print job.body
 
def worker():
	while True:
		job = beanstalk.reserve()
		do_job(job)
		job.delete

t = threading.Thread(target=worker)
#t.setDaemon(True)
t.start()