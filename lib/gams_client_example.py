# Request an analysis from the GAMS server

import rpyc

conn = rpyc.connect("127.0.0.1", 19913)
results = conn.root.run_analysis("this is some GAMS code")

print results