from __main__ import app
from flask import render_template, url_for, flash, request, redirect, Response, session
from flask_login import login_required, login_user, logout_user, current_user
import sqlite3


@app.route("/add_agent")
def add_agent():
     if not current_user.is_authenticated:
       return redirect(url_for('login'))
     if(session['is_admin']):
        return render_template("add_agent.html", active_tab_agents="active")
     else:
        return "No access to this page"

@app.route('/agents_list', methods=['GET','POST'])
def agents_list():
   if not current_user.is_authenticated:
       return redirect(url_for('login'))
   if(session['is_admin']):
     conn = sqlite3.connect('/root/signalwire_support_callcenter/signalwire_support_callcenter.db')
     conn.row_factory = sqlite3.Row
     curs = conn.cursor()
     curs.execute("SELECT * from agent")
     rows = curs.fetchall()
     return render_template("agents_list.html",rows = rows, active_tab_agents="active")
   else:
      return "No access to this page"


@app.route("/save_agent_details",methods = ["POST","GET"])
def save_agent_etails():
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    if not (session['is_admin']):
       return "No access to this page"
    msg = "msg"
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& " + request.method)
    if request.method == "POST":
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& tttttt" + request.method)
        try:
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& tttttt try" + request.method)
            print(request.form)
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            personal_number = request.form["personal_number"]
            office_number = request.form["office_number"]
            sip_address = request.form["sip_address"]
            sip_user_name = request.form["sip_user_name"]
            sip_password = request.form["sip_password"]
            with sqlite3.connect("/root/signalwire_support_callcenter/signalwire_support_callcenter.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into agent (name, email, password,personal_number,office_number,sip_address,sip_user_name,sip_password) values (?,?,?,?,?,?,?,?)",(name,email,password,personal_number,office_number,sip_address,sip_user_name,sip_password))
                con.commit()
                msg = "Agent successfully Added"
        except:
            
            con.rollback()
            msg = "We can not add the Agnet to the list"  
            print(msg)
        finally:
            print(msg)
            return  redirect(url_for('agents_list'))
            con.close()
