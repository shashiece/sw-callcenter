import os
from flask import Flask
from flask import render_template, url_for, flash, request, redirect, Response, session
import sqlite3
from flask_login import UserMixin
from flask_login import login_required, login_user, logout_user, current_user
from flask_login import LoginManager
from forms import LoginForm
import pprint
import json

app = Flask(__name__)
app.debug=True

# read menus from json file
with open('config/config.json') as f:
     ccConfig = json.load(f)
     # Dump config to console, for debugging
     pprint.pprint(ccConfig)


import ivr_routes
import admin_actions

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager(app)
login_manager.login_view = "login"
class Agent(UserMixin):
    def __init__(self, agent_id,name, email, password,is_admin):
         self.agent_id = agent_id
         self.name = name
         self.email = email
         self.password = password
         self.authenticated = False
         self.is_admin=is_admin
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.agent_id

@login_manager.user_loader
def load_user(agent_id):
   conn = sqlite3.connect('/root/signalwire_support_callcenter/signalwire_support_callcenter.db')
   curs = conn.cursor()
   curs.execute("SELECT * from agent where agent_id = (?)",[agent_id])
   lu = curs.fetchone()
   if lu is None:
      return None
   else:
      return Agent(int(lu[0]), lu[1], lu[2],lu[3],lu[10])

@app.route('/')
def index():
  return redirect(url_for('profile'))

@app.route('/profile')
def profile():
   if not current_user.is_authenticated:
      return redirect(url_for('login'))
   return render_template('profile.html',title='Profile',active_profile="active")   

@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
     return redirect(url_for('profile'))
  form = LoginForm()
  if form.validate_on_submit():
     conn = sqlite3.connect('/root/signalwire_support_callcenter/signalwire_support_callcenter.db')
     curs = conn.cursor()
     curs.execute("SELECT * FROM agent where email = (?)",    [form.email.data])
     agent = list(curs.fetchone())
     Ag = load_user(agent[0])
     if form.email.data == Ag.email and form.password.data == Ag.password:
        session['is_admin']=Ag.is_admin
        login_user(Ag, remember=form.remember.data)
        Umail = list({form.email.data})[0].split('@')[0]
        flash('Logged in successfully '+Umail)
        return redirect(url_for('profile'))
     else:
        flash('Login Unsuccessfull.')
  return render_template('login.html',title='Login', form=form, page='login',data={})

@app.route("/logout", methods=['GET','POST'])
def logout():
  current_user=None
  logout_user()
  return redirect(url_for('login'))
@app.route("/support_queues", methods=['GET'])
def support_queues():
  if not current_user.is_authenticated:
    return redirect(url_for('login'))

  from signalwire.rest import Client as signalwire_client
  client = signalwire_client("981ab3f3-3bee-408f-ad96-5ebe87c318ac", "PT44f71ed3fd40a1fc83e1d8d67a4b80f200b0862c5675d794", signalwire_space_url = 'shashi-fs.signalwire.com')
  support_members = client.queues('a2bff28a-8dce-4dca-b36f-1bcca187a563').members.list()
  support_members_data=dict()
  support_members_data['members_count'] = len(support_members)
  support_members_data['members'] = support_members

  sales_members = client.queues('17404eb3-b4aa-4a02-9bc8-5ccc810361ce').members.list()
  sales_members_data=dict()
  sales_members_data['members_count'] = len(sales_members)
  sales_members_data['members'] = sales_members

  return render_template('support_queues.html',title='Support Queues',data={"support_members_data": support_members_data,"sales_members_data":sales_members_data},active_queues="active")

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8080,threaded=True)

