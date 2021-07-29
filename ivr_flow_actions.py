from __main__ import app
from flask import render_template, url_for, flash, request, redirect, Response, session
from flask_login import   current_user
import sqlite3

import json

with open('config/config.json') as f:
     ccConfig = json.load(f)

@app.route("/add_ivr_flow")
def add_ivr_flow():
     if not current_user.is_authenticated:
       return redirect(url_for('login'))
     if(session['is_admin']):
        return render_template("add_ivr_flow.html", active_tab_ivr_flows="active")
     else:
        return "No access to this page"

@app.route('/ivr_flows_list', methods=['GET','POST'])
def ivr_flows_list():
   if not current_user.is_authenticated:
       return redirect(url_for('login'))
   if(session['is_admin']):
     conn = sqlite3.connect(ccConfig['settings']['database_file'])
     conn.row_factory = sqlite3.Row
     curs = conn.cursor()
     curs.execute("SELECT * from ivr_flow")
     rows = curs.fetchall()
     return render_template("ivr_flow_list.html",rows = rows, active_tab_ivr_flows="active")
   else:
      return "No access to this page"


@app.route("/save_ivr_flow_details",methods = ["POST","GET"])
def save_ivr_flow_etails():
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    if not (session['is_admin']):
       return "No access to this page"
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            
            with sqlite3.connect(ccConfig['settings']['database_file']) as con:
                cur = con.cursor()
                cur.execute("INSERT into ivr_flow (Ivr_flow_name) values (?)",(name))
                con.commit()
                msg = "Ivr Flow successfully Added"
        except:            
            con.rollback()
            msg = "We can not add the Ivr Flow to the list"  
            print(msg)
        finally:
            print(msg)
            return  redirect(url_for('ivr_flows_list'))
            con.close()

@app.route("/delete_ivr_flow/<ivr_flow_id>",methods = ["POST"])
def delete_ivr_flow(ivr_flow_id):
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    try:
        with sqlite3.connect(ccConfig['settings']['database_file']) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM ivr_flow where ivr_flow_id=?",(ivr_flow_id))
            con.commit()
            msg = "Ivr Flow deleted sucessfully"
    except:            
        con.rollback()
        msg = "We can not delete the Ivr Flow from the list"  
    finally:
        con.close()
        return  redirect(url_for('ivr_flows_list'))
        
@app.route("/update_ivr_flow",methods = ["POST"])
def update_ivr_flow():
    msg=""
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    try:
        name = request.form["name"]
        ivr_flow_id=request.form["ivr_flow_id"]
        print(ivr_flow_id)
        with sqlite3.connect(ccConfig['settings']['database_file']) as con:
            cur = con.cursor()        
            cur.execute("UPDATE ivr_flow set Ivr_flow_name=? where ivr_flow_id=?",(name, ivr_flow_id))
            con.commit()
            msg = "Ivr Flow deleted sucessfully"
    except Exception as e:            
        con.rollback()
        print(e)
        msg = "We can not update the Ivr Flow from the list "+ e  
    finally:
        con.close()
        return  redirect(url_for('ivr_flows_list'))

@app.route("/create_ivr_flow/<ivr_flow_id>", methods=['GET','POST'])
def create_ivr_flow(ivr_flow_id):
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    return render_template("create_ivr_flow.html", active_tab_ivr_flows="active")


@app.route('/ivr_flows_data/<ivr_flow_id>', methods=['GET'])
def ivr_flows_data(ivr_flow_id):
   if not current_user.is_authenticated:
       return redirect(url_for('login'))
   if(session['is_admin']):
     conn = sqlite3.connect(ccConfig['settings']['database_file'])
     conn.row_factory = sqlite3.Row
     curs = conn.cursor()
     curs.execute("SELECT * from ivr_flow where ivr_flow_id = ?",(ivr_flow_id))
     rows = curs.fetchone()
     return render_template("ivr_flow_list.html",rows = rows, active_tab_ivr_flows="active")
   else:
      return "No access to this page"