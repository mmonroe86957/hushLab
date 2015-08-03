import MySQLdb

def connection():
	conn = MySQLdb.connect(host="localhost",
							user = "root",
							passwd = "Bluecali-86",
							db = "MyAPP")
							
	c = conn.cursor()
	return c, conn