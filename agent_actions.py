from __main__ import app
from flask import render_template, url_for, flash, request, redirect, Response, session
from flask_login import   current_user
import sqlite3

import json

with open('config/config.json') as f:
     ccConfig = json.load(f)

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
     conn = sqlite3.connect(ccConfig['settings']['database_file'])
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
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            personal_number = request.form["personal_number"]
            office_number = request.form["office_number"]
            sip_address = request.form["sip_address"]
            sip_user_name = request.form["sip_user_name"]
            sip_password = request.form["sip_password"]
            with sqlite3.connect(ccConfig['settings']['database_file']) as con:
                cur = con.cursor()
                cur.execute("INSERT into agent (name, email, password,personal_number,office_number,sip_address,sip_user_name,sip_password) values (?,?,?,?,?,?,?,?)",(name,email,password,personal_number,office_number,sip_address,sip_user_name,sip_password))
                con.commit()
                msg = "Agent successfully Added"
        except:            
            con.rollback()
            msg = "We can not add the Agent to the list"  
            print(msg)
        finally:
            print(msg)
            return  redirect(url_for('agents_list'))
            con.close()

@app.route("/delete_agent/<agent_id>",methods = ["POST"])
def delete_agent(agent_id):
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    try:
        with sqlite3.connect(ccConfig['settings']['database_file']) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM agent where agent_id=?",(agent_id))
            con.commit()
            msg = "Agent deleted sucessfully"
    except:            
        con.rollback()
        msg = "We can not delete the Agent from the list"  
    finally:
        con.close()
        return  redirect(url_for('agents_list'))
        
@app.route("/update_agent",methods = ["POST"])
def update_agent():
    msg=""
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    try:
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        personal_number = request.form["personal_number"]
        office_number = request.form["office_number"]
        sip_address = request.form["sip_address"]
        sip_user_name = request.form["sip_user_name"]
        sip_password = request.form["sip_password"]
        agent_id = request.form["agent_id"]
        print(agent_id)
        with sqlite3.connect(ccConfig['settings']['database_file']) as con:
            cur = con.cursor()        
            cur.execute("UPDATE agent set name=?, email=?, password=?, personal_number=?,office_number=?,sip_address=?,sip_user_name=?,sip_password =? where agent_id=?",(name, email, password,personal_number,office_number,sip_address,sip_user_name,sip_password, agent_id))
            con.commit()
            msg = "Agent deleted sucessfully"
    except Exception as e:            
        con.rollback()
        print(e)
        msg = "We can not update the Agent from the list "+ e  
    finally:
        print("***************************************")
        print(msg)
        con.close()
        return  redirect(url_for('agents_list'))
