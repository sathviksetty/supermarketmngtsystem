import mysql.connector
from domspkg import settings 
import datetime

def getmydb():
  conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sap$0000",
    database="romsdb"
  )
  settings.mydb=conn

def login(user,pwd):
  sql = "select id,manager,initial_pwd,pwd,active from operators where userid=%s and pwd=%s"   
  mycur=settings.mydb.cursor() 
  mycur.execute(sql,(user,pwd)) 
  op=mycur.fetchall()
  if len(op)==0:
    return False
  settings.operator=op[0][0]
  settings.manager=op[0][1]
  settings.initial=op[0][2]
  settings.passwd=op[0][3]
  settings.active=op[0][4]
  return True

def getuser(oid):
  cur=settings.mydb.cursor()
  cur.execute("select userid from operators where id=%s",(oid,))
  data=cur.fetchall()
  if cur.rowcount==1:
    user=data[0][0]
    return user
  else:
    return None

def isoutletavl(oid):
  cur=settings.mydb.cursor()
  cur.execute("select id from outlets where id=%s",(oid,))
  data=cur.fetchall()
  if len(data)==0:
    return False
  return True

def isproductavl(pid):
  cur=settings.mydb.cursor()
  cur.execute("select id from products where id=%s",(pid,))
  data=cur.fetchall()
  if len(data)==0:
    return False
  return True
  
def isstockavl(pid):
  cur=settings.mydb.cursor()
  cur.execute("select product_id from stock where outlet_id=%s and product_id=%s",(settings.outlet,pid))
  data=cur.fetchall()
  if len(data)==0:
    return False
  return True

def iscustavl(phone):
  cur=settings.mydb.cursor()
  cur.execute("select phone from customers where phone=%s",(phone,))
  data=cur.fetchall()
  if len(data)==0:
    return False
  return True

def auditlog(dfrom,dto):
  df=datetime.datetime.strptime(dfrom,"%d-%b-%Y")
  dt=datetime.datetime.strptime(dto,"%d-%b-%Y")
  dt=dt+datetime.timedelta(days=1)
  cur=settings.mydb.cursor()
  cur.execute("select * from auditlog where action_time between %s and %s",(df,dt))
  data=cur.fetchall()
  if len(data)==0:
    return None
  return data

def billedcart(cart):
  cur=settings.mydb.cursor()
  tot=0
  for item in cart:
    cur.execute("select unit_price from stock where outlet_id=%s and product_id=%s",(settings.outlet,item["product_id"]))
    data=cur.fetchall()
    if len(data)==0:
      print("no data for",item["product_id"])
      return 0
    uprice=float(data[0][0])
    amt=float(item["sold_qty"])*uprice
    tot=tot+amt
    item.update({"unit_price":uprice,"amount":amt})
  data=[]
  data.append(tot)
  data.append(cart)
  return data

def gettxnid(phone):
  cur=settings.mydb.cursor()
  cur.execute("select id from sales_txns where customer_phone=%s and paid_time = (select max(paid_time) from sales_txns)",(phone,))
  data=cur.fetchall()
  if len(data)==0:
    return False  
  txn_id=data[0][0]
  return txn_id

def getsalestxn(txn):
  cur=settings.mydb.cursor(dictionary=True)
  cur.execute("select s.id,o.city,o.location,op.name op_name,c.name cu_name,s.tot_amount,s.payment_mode,s.paid_time from sales_txns s \
join outlets o on o.id=s.outlet_id \
join operators op on op.id=s.operator_id \
join customers c on c.phone=s.customer_phone \
where s.id=%s;",(txn,))
  data=cur.fetchall()
  if len(data)==0:
    return None
  return data

def getsalesdetail(txn):
  cur=settings.mydb.cursor(dictionary=True)
  cur.execute("select product_name,sold_qty,unit_price,amount from sales_details s \
    join products p on p.id=s.product_id \
    where txn_id=%s",(txn,))
  data=cur.fetchall()
  if len(data)==0:
    return None
  return data

def oprcashrep():
  tod=datetime.date.today()
  print(tod)
  cur=settings.mydb.cursor(dictionary=True)
  cur.execute("select id,tot_amount,paid_time,payment_mode from sales_txns where operator_id=%s and date(paid_time)=%s order by payment_mode",(settings.operator,tod))
  data=cur.fetchall()
  if len(data)==0:
    print("You did not do any business today")
    return None
  return data

def outletcashrep():
  tod=datetime.date.today()
  cur=settings.mydb.cursor(dictionary=True)
  cur.execute("select operator_id, payment_mode, sum(tot_amount) total_amount from sales_txns group by operator_id, payment_mode order by payment_mode desc, operator_id=%s",(settings.operator,))
  data=cur.fetchall()
  if len(data)==0:
    print("Report already generated / No business at all today")
    return None
  return data

def dailydemandrep():
  cur=settings.mydb.cursor(dictionary=True)
  cur.execute("select outlet_id, product_id, supplier_id, order_qty,available_qty,threshold_qty from stock s \
    inner join products p on s.product_id=p.id \
    where available_qty<=threshold_qty and order_placed=false")
  data=cur.fetchall()
  if len(data)==0:
    print("No daily demand data for today")
    return None
  cur.execute("update stock set order_placed=true where available_qty<=threshold_qty")
  if cur.rowcount==0:
    print("Somehow order_placed couldn't get set to true")
    return None
  settings.mydb.commit()
  return data