from flask import Flask, render_template, json, request, flash, get_flashed_messages, redirect, url_for, session, jsonify, redirect, Response
from flask import Markup
from MySQLdb import escape_string as thwart
from werkzeug import generate_password_hash, check_password_hash
from db_conn import connection
import gc

from memberdataclass import Member
from memberdataclass import Client


app = Flask(__name__)

class ClientData(object):

	def __init__(self, id):
		self.member_id = id


	def get_member_clients(self):
		try:
			c,conn = connection()
		except Exception as e:
			return str(e)

		c.execute("SELECT client_name FROM member_clients WHERE member_id_fk='%s'" % self.member_id)
		clients_query = c.fetchall()
		c.close()
		conn.close()
		clients = [client[0] for client in clients_query]
		self.client_names = []
		for client in clients:
			client_name = {'client': client}
			self.client_names.append(client_name)

		return self.client_names

	def get_client_data(self):
		try:
			c,conn = connection()
		except Exception as e:
			return str(e)

		c.execute("SELECT mc.client_name, mc.client_id, ci.item_type, ci.item_price, iq.item_quantity, iq.item_time FROM member_login ml join member_clients mc ON ml.member_id = mc.member_id_fk join client_items ci ON mc.client_id = ci.client_id_fk join item_quantities iq ON ci.item_id = iq.item_id_fk WHERE ml.member_id='%s' AND iq.item_time >= '2015-01-05 06:55:51' AND iq.item_time <= '2015-12-29 23:07:59' ORDER BY iq.item_time" % self.member_id)
		data = c.fetchall()
		c.close()
		conn.close()
		for datum in range(len(data)):
			

		return str(data)





@app.route("/")
def main():
	#return json.dumps({'html':'<span>Enter the something else fields</span>'})
	return render_template('index.html')


@app.route('/signUp/', methods=['POST', 'Get'])
def signUp():
	return render_template('signup.html')


@app.route('/signIn/', methods=['POST', 'GET'])
def signIn():
		message = Markup("Welcome back. Please sign in.")
		flash(message)
		return render_template('signin.html')
	
@app.route('/getInfo/', methods=['POST', 'GET'])
def getInfo():
	try:
		_companyName = request.form['co_name']
		_companyEmail = request.form['co_email']
		_companyUser = request.form['userName']
		_companyPass = request.form['passWord']

		if _companyUser and _companyPass and _companyName and _companyEmail:
			c, conn = connection()
			x = c.execute("SELECT * FROM member_login WHERE member_username = '%s' or member_password = '%s'" %(thwart(_companyUser), thwart(_companyPass)))

			if x > 0:
				c.close()
				conn.close()
				message = Markup("Username or Password Already Exists.")
				flash(message)
				return render_template('signin.html')
			
			else:
				data = c.execute("INSERT INTO member_login (member_name, member_username, member_password, member_email) VALUES ('%s', '%s', '%s', '%s')" %(thwart(_companyName), thwart(_companyUser), thwart(_companyPass), thwart(_companyEmail))) 
				
				#session['id'] = c.execute("SELECT member_id FROM member_login WHERE member_username = '%s''" %(thwart(_companyUser)))
				#data = c.fetchall()
				#return redirect(url_for('members', id=str(data[0][0])))
				#return str(data[0][0])
				conn.commit()
				c.close()
				conn.close()
				message = Markup("Your information has been Stored.")
				flash(message)
				return render_template('signin.html')
		else: 
			return json.dumps({'html':'<span>Please sign up or sign in.</span>'})
	except Exception as e:
			return (str(e))

@app.route('/checkUser/', methods=['POST', 'GET'])
def checkUser():
		# Need to add validators for user inputs 
		try:
			_companyUser = request.form['userName']
			_companyPass = request.form['passWord']
			
			if _companyUser and _companyPass:
				c, conn = connection()
				x = c.execute("SELECT * FROM member_login WHERE member_username = '%s' AND member_password = '%s'" %(thwart(_companyUser), thwart(_companyPass)))
			
			if x > 0:
				session['logged_in'] = True
				session['username'] = _companyUser
				session['id'] = c.execute("SELECT member_id FROM member_login WHERE member_username = '%s'" %(thwart(_companyUser)))
				c.close()
				conn.close()
				return redirect(url_for ('members', session_id=str(session['id'])))
				
			else:
				c.close()
				conn.close()
				message = Markup("Login Failed. Please try again.")
				flash(message)
				return render_template('signin.html')
				
		except Exception as e:
				#return (str(e))
				return "Something is broken"

@app.route('/members/<session_id>', methods=['POST', 'GET'])
def members(session_id):
	CLIENTS = ClientData(session_id)
	client_names = CLIENTS.get_member_clients()
	client_data = CLIENTS.get_client_data()
	return str(client_data)
	#member_data = Member(client_meta_data)
	#client_badge_data = member_data.get_member_client_meta()
	#return render_template('memberhomepage.html', member_name=member_name, client_names=client_names)
	#return str(client_names)
	
	

	#return render_template('memberhomepage.html', session_id=str(session['id']))









'''
@app.route('/getclientdata/', methods=['POST', 'GET'])
def getclientdata():
	clientName = request.form['client_name']
	return str(clientName)	



















@app.route('/members/<session_id>/addClient/', methods=['POST', 'GET'])
def addClient():	
	try:
		_clientName = request.form['clientName']
		_memberID = session.get('id')
		if _clientName:
			c, conn = connection()
			exists = c.execute("Select * FROM member_clients WHERE client_name ='%s'" %(thwart(_clientName))) 
		
			if exists:
				c.close()
				conn.close()
				message = Markup("Client already exists.")
				flash(message)
				return render_template('memberhomepage.html', session_id=str(session.get('id')))
				
			else: 
				x = c.execute("Insert INTO member_clients (client_name, member_id) VALUES ('%s', '%s')" % (thwart(_clientName), _memberID))
				c.close()
				conn.close()
				


				
				
	except Exception as e:
		return(str(e))'''
		
		
	
	

			
if __name__=="__main__":
	app.secret_key=':F\x030\x1fS\x1fw\x84i\x93\xb6\x8d\x89l=eA/\xf3\xc1\x076\x90'
	app.run(port=8080, debug=True)
