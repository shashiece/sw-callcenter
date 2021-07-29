from __main__ import app
from flask import render_template, url_for, flash, request, redirect, Response, session
from flask_login import  current_user
import sqlite3

import json

with open('config/config.json') as f:
     ccConfig = json.load(f)

@app.route('/product_agents_list/<product_id>', methods=['GET','POST'])
def product_agents_list(product_id):
   if not current_user.is_authenticated:
       return redirect(url_for('login'))
   if(session['is_admin']):
     conn = sqlite3.connect(ccConfig['settings']['database_file'])
     conn.row_factory = sqlite3.Row
     curs = conn.cursor()
     curs.execute("SELECT *,pa.product_agent_id from agent a left join product_agent pa on a.agent_id=pa.agent_id where pa.product_id=?",(product_id))
     rows = curs.fetchall()

     conn = sqlite3.connect(ccConfig['settings']['database_file'])
     conn.row_factory = sqlite3.Row
     curs = conn.cursor()
     curs.execute("SELECT * from agent ")
     agents = curs.fetchall()

     return render_template("product_agents_list.html",rows = rows,agents= agents, product_id=product_id, active_tab_products="active")
   else:
      return "No access to this page"


@app.route("/save_product_agent_details",methods = ["POST"])
def save_product_agent_details():
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    if not (session['is_admin']):
       return "No access to this page"
    msg = "msg"
    if request.method == "POST":
        try:
            agent_id = request.form["agent_id"]
            product_id = request.form["product_id"]
            with sqlite3.connect(ccConfig['settings']['database_file']) as con:
                cur = con.cursor()
                cur.execute("INSERT into product_agent (agent_id, product_id) values (?,?)",(agent_id,product_id))
                con.commit()
                msg = "product_agent successfully Added"
        except:            
            con.rollback()
            msg = "We can not add the product_agent to the list"  
            print(msg)
        finally:
            print(msg)
            return  redirect(url_for('product_agents_list',product_id=int(product_id)))
            con.close()

@app.route("/delete_product_agent/<product_agent_id>",methods = ["POST"])
def delete_product_agent(product_agent_id):
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    try:
        with sqlite3.connect(ccConfig['settings']['database_file']) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM product_agent where product_agent_id=?",(product_agent_id))
            con.commit()
            msg = "product_agent deleted sucessfully"
    except:            
        con.rollback()
        msg = "We can not delete the Product Agnet from the list"  
    finally:
        con.close()
        return  redirect(url_for('product_agents_list',product_id=1))
        

