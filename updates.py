import mysql.connector
import datetime
from domspkg import settings

def addcustomer(ph,name,dob):
  cur=settings.mydb.cursor()
  bdate=datetime.datetime.strptime(dob,"%d-%b-%Y")
  cur.execute("insert into customers values(%s,%s,%s,current_timestamp())",(ph,name,bdate))
  if cur.rowcount==1:
    settings.mydb.commit()
    return True
  return False

def addoutlet(oid,city,loc,mngr,phone):
  cur=settings.mydb.cursor()
  cur.execute("insert into outlets values(%s,%s,%s,%s,%s,current_timestamp())",(oid,city,loc,mngr,phone))
  if cur.rowcount==1:
    settings.mydb.commit()
    return True
  return False

def addsupplier(sid,name,phone,email):
  cur=settings.mydb.cursor()
  cur.execute("insert into suppliers values(%s,%s,%s,%s,current_timestamp())",(sid,name,phone,email))
  if cur.rowcount==1:
    settings.mydb.commit()
    return True
  return False

def addproduct(pid,name,sid):
  cur=settings.mydb.cursor()
  cur.execute("insert into products values(%s,%s,%s,current_timestamp())",(pid,name,sid))
  if cur.rowcount==1:
    settings.mydb.commit()
    return True
  return False

def addopr(oid,name,user,pwd,mngr):
  cur=settings.mydb.cursor()
  cur.execute("insert into operators(id,name,userid,pwd,manager,created_time) values(%s,%s,%s,%s,%s,current_timestamp())",(oid,name,user,pwd,mngr))
  if cur.rowcount==1:
    cur.execute("insert into auditlog(operator_id,action,affected_userid,action_time) values(%s,%s,%s,current_timestamp())",(settings.operator,"adduser",user))
    settings.mydb.commit()
    return True
  return False

def chgpwd(npwd,user):
  cur=settings.mydb.cursor()
  cur.execute("update operators set pwd=%s where id=%s",(npwd,settings.operator))
  if cur.rowcount==1:
    cur.execute("update operators set initial_pwd=False where id=%s",(settings.operator,))
    cur.execute("insert into auditlog(operator_id,action,affected_userid,action_time) values(%s,%s,%s,current_timestamp())",(settings.operator,"chgpwd",user))
    settings.mydb.commit()
    settings.initial=False
    return True
  return False

def chgopwd(oid,user,npwd):
  cur=settings.mydb.cursor()
  cur.execute("update operators set pwd=%s where id=%s",(npwd,oid))
  if cur.rowcount==1:
    cur.execute("update operators set initial_pwd=%s where id=%s",(True,oid))
    cur.execute("insert into auditlog(operator_id,action,affected_userid,action_time) values(%s,%s,%s,current_timestamp())",(settings.operator,"chgpwd",user))
    settings.mydb.commit()
    return True
  return False

def deactivate(oid,user):
  cur=settings.mydb.cursor()
  cur.execute("update operators set active=%s where id=%s",(False,oid))
  if cur.rowcount==1:
    cur.execute("insert into auditlog(operator_id,action,affected_userid,action_time) values(%s,%s,%s,current_timestamp())",(settings.operator,"deactivate",user))
    settings.mydb.commit()
    settings.active=False
    return True
  return False


def activate(oid,user):
  cur=settings.mydb.cursor()
  cur.execute("update operators set active=%s where id=%s",(True,oid))
  if cur.rowcount==1:
    cur.execute("insert into auditlog(operator_id,action,affected_userid,action_time) values(%s,%s,%s,current_timestamp())",(settings.operator,"activate",user))    
    settings.mydb.commit()
    settings.active=True
    return True
  return False

def addproduct(pid,pname,sid):
  cur=settings.mydb.cursor()
  cur.execute("insert into products values(%s,%s,%s,current_timestamp())",(pid,pname,sid))
  if cur.rowcount==1:
    settings.mydb.commit()
    return True
  return False

def addstock(pid,qty,mrp,tqty,mqty):
  cur=settings.mydb.cursor()
  cur.execute("insert into stock(outlet_id,product_id,available_qty,threshold_qty,order_qty,unit_price) values(%s,%s,%s,%s,%s,%s)",(settings.outlet,pid,float(qty),float(tqty),float(mqty),float(mrp)))
  if cur.rowcount==1:
    #settings.mydb.commit()
    return True
  return False

def incrstock(pid,qty,uprice):
  cur=settings.mydb.cursor()
  cur.execute("update stock set available_qty=available_qty+%s,unit_price=%s,order_placed=false where outlet_id=%s and product_id=%s", (qty,uprice,settings.outlet,pid))
  if cur.rowcount==1:
    #settings.mydb.commit()
    return True
  return False

def decrstock(pid,qty):
  cur=settings.mydb.cursor()
  cur.execute("update stock set available_qty=available_qty-%s where outlet_id=%s and product_id=%s", (qty,settings.outlet,pid))
  if cur.rowcount==1:
    #settings.mydb.commit()
    return True
  return False

def addpurchase(pid,qty,uprice):
  cur=settings.mydb.cursor()
  cur.execute("insert into purchases(outlet_id,product_id,purchased_qty,unit_price,created_time) values(%s,%s,%s,%s,current_timestamp())",(settings.outlet,pid,float(qty),float(uprice)))
  if cur.rowcount==1:
    settings.mydb.commit()
    return True
  return False

def addsalestxn(phone,tot,mode):
  cur=settings.mydb.cursor()
  cur.execute("insert into sales_txns(outlet_id,operator_id,customer_phone,tot_amount,payment_mode,paid_time) values(%s,%s,%s,%s,%s,current_timestamp())",(settings.outlet,settings.operator,phone,tot,mode))
  if cur.rowcount==1:
    return True
  return False

def addsalesdet(cart,txn_id):
  cur=settings.mydb.cursor()
  for item in cart:
    cur.execute("insert into sales_details(txn_id,product_id,sold_qty,unit_price,amount) values(%s,%s,%s,%s,%s)",(txn_id,item["product_id"],item["sold_qty"],item["unit_price"],item["amount"]))
    if cur.rowcount==0:
      return False
    decrstock(item["product_id"],item["sold_qty"])    
  settings.mydb.commit()
  return True
