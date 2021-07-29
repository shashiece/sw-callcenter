from __main__ import app
from flask import render_template, url_for, flash, request, redirect, Response, session
from flask_login import  current_user
import sqlite3
import json

with open('config/config.json') as f:
     ccConfig = json.load(f)



@app.route('/products_list', methods=['GET','POST'])
def products_list():
   if not current_user.is_authenticated:
       return redirect(url_for('login'))
   if(session['is_admin']):
     conn = sqlite3.connect(ccConfig['settings']['database_file'])
     conn.row_factory = sqlite3.Row
     curs = conn.cursor()
     curs.execute("SELECT * from product")
     rows = curs.fetchall()
     return render_template("products_list.html",rows = rows, active_tab_products="active")
   else:
      return "No access to this page"


@app.route("/save_product_details",methods = ["POST"])
def save_product_details():
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    if not (session['is_admin']):
       return "No access to this page"
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            description = request.form["description"]
            with sqlite3.connect(ccConfig['settings']['database_file']) as con:
                cur = con.cursor()
                cur.execute("INSERT into product (name, description) values (?,?)",(name,description))
                con.commit()
                msg = "product successfully Added"
        except:            
            con.rollback()
            msg = "We can not add the product to the list"  
            print(msg)
        finally:
            print(msg)
            return  redirect(url_for('products_list'))
            con.close()

@app.route("/delete_product/<product_id>",methods = ["POST"])
def delete_product(product_id):
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    try:
        with sqlite3.connect(ccConfig['settings']['database_file']) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM product where product_id=?",(product_id))
            con.commit()
            msg = "product deleted sucessfully"
    except:            
        con.rollback()
        msg = "We can not delete the Agnet from the list"  
    finally:
        con.close()
        return  redirect(url_for('products_list'))
        
@app.route("/update_product",methods = ["POST"])
def update_product():
    msg=""
    if not current_user.is_authenticated:
       return redirect(url_for('login'))
    try:
        name = request.form["name"]
        description = request.form["description"]
        product_id = request.form["product_id"]
        print(product_id)
        with sqlite3.connect(ccConfig['settings']['database_file']) as con:
            cur = con.cursor()        
            cur.execute("UPDATE product set name=?, description=? where product_id=?",(name, description, product_id))
            con.commit()
            msg = "product deleted sucessfully"
    except Exception as e:            
        con.rollback()
        msg = "We can not update the Product from the list "+ e  
    finally:

        con.close()
        return  redirect(url_for('products_list'))
