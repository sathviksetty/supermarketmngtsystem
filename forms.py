from getpass import getpass
from domspkg.queries import *
from domspkg.updates import *
from domspkg.reports import *
from os import system
from domspkg import settings 
import random

def dlogin():
  system("cls")
  print("\n\n\n")
  print("".center(20," "),end="")
  olet=input("Outlet ID:")
  getmydb()
  if not isoutletavl(olet):
    print(" ~~~ Error 300: Invalid Outlet ID ~~~")
    print(" *** Access DENIED ***")
    print(" === Good BYE ===")
    exit(300)
  print("".center(20," "),end="")
  user=input("\aUsername:")
  pwd=getpass(prompt="\a                    Password:")
  settings.outlet=olet
  settings.passwd=pwd
  success=login(user,pwd)
  if not success:
    print(" ~~~ Error 100: User ID OR Password does NOT match ~~~")
    print(" *** Access DENIED ***")
    print(" === Good BYE ===")
    exit(100)
  if not settings.active:
    print(" ~~~ Error 200: User ID NOT active ~~~")
    print(" *** Access DENIED ***")
    print(" === Good BYE ===")
    exit(200)
  if settings.initial:
    dchgpwd()
  return

def doprmenu():
  system("cls")
  print("OUTLET = ",settings.outlet, "OPERATOR ID = ",settings.operator, end="")
  print(" ROLE = OPERATOR\n")
  print("~~~Welcome to RATNADEEP ORDER MANAGEMENT SYSTEM ~~~")
  print("\n")
  print('''1.  Sales Entry
2.  Print Invoice
3.  My Cash Report
4.  Add Customer Record
5.  Change My Password
0.  EXIT

''')
  ch=input("Enter your choice:")
  return ch

def dmngrmenu():
  system("cls")
  print("OUTLET = ",settings.outlet, "OPERATOR ID = ",settings.operator, end="")
  print(" ROLE = MANAGER\n")
  print("~~~Welcome to RATNADEEP ORDER MANAGEMENT SYSTEM ~~~")
  print("\n")
  print(''' 1.  Add Outlet
 2.  Add Operator
 3.  Add Supplier
 4.  Add Product
 5.  Print Invoice
 6.  Outlet Cash Report
 7.  Daily Demand Report
 8.  Change My Password
 9.  Change Operator Password
10.  Deactivate Operator
11.  Activate Operator
12.  Audit Log
13.  Stock Received
0.  EXIT

''')
  ch=input("Enter your choice:")
  return ch

def daddcustomer():
  system("cls")
  print("\n\n")
  print("~~~ Customer Entry Form ~~~")  
  print("\n\n")
  ph=input("Enter customer Phone (10 digit) : ")
  name=input("Enter customer Name : ")
  dob=input("Enter customer Date of Birth (like 10-May-1987) ")
  success=addcustomer(ph,name,dob)
  if success:
    print("-> -> -> customer added sucessfully...")
  else:
    print("ALERT: customer could not be added ...")

def daddoutlet():
  system("cls")
  print("\n\n")
  print("~~~ Outlet Entry Form ~~~")  
  print("\n\n")
  oid=input("Enter outlet ID (4 char) : ")
  city=input("Enter City name : ")
  loc=input("Enter Location : ")
  mngr=input("Enter Manager name : ")
  phone=input("Enter Phone (10 digit) : ")
  success=addoutlet(oid,city,loc,mngr,phone)
  if success:
    print("-> -> -> OUTLET added sucessfully...")
  else:
    print("ALERT: outlet could not be added ...")

def daddsupplier():
  system("cls")
  print("\n\n")
  print("~~~ Outlet Entry Form ~~~")  
  print("\n\n")
  sid=input("Enter supplier ID (4 char) : ")
  name=input("Enter Supplier name : ")
  phone=input("Enter Supplier Phone (10 digit) : ")
  email=input("Enter Supplier email : ")
  success=addsupplier(sid,name,phone,email)
  if success:
    print("-> -> -> SUPPLIER added sucessfully...")
  else:
    print("ALERT: supplier could not be added ...")

def daddproduct():
  system("cls")
  print("\n\n")
  print("~~~ Outlet Entry Form ~~~")  
  print("\n\n")
  pid=input("Enter Product ID (6 char) : ")
  name=input("Enter Product name : ")
  sid=input("Enter Supplier ID (4 char) : ")
  success=addproduct(pid,name,sid)
  if success:
    print("-> -> -> PRODUCT added sucessfully...")
  else:
    print("ALERT: product could not be added ...")

def gen_pwd(l=6):
  pchr="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
  password = ''.join(random.choice(pchr) for _ in range(l))
  return password

def daddopr():
  system("cls")
  print("\n\n")
  print("~~~ Operator Entry Form ~~~")  
  print("\n\n")
  oid=input("Enter operator ID (4 char) : ")
  name=input("Enter operator name : ")
  user=input("Enter user id : ")
  pwd=gen_pwd();
  mngr=input("Is the role MANAGER? (y/n)")
  if mngr.upper()=="Y":
    mngr=True
  else:
    mngr=False
  success=addopr(oid,name,user,pwd,mngr)
  if success:
    print("-> -> -> Operator added sucessfully...")
    print("Please share this pwd with operator : ",pwd)
  else:
    print("ALERT: operator could not be added ...")

def dchgpwd():
  opwd=getpass("Old password:")
  npwd=getpass("New password:")
  rpwd=getpass("Repeat password:")
  if opwd==settings.passwd and npwd==rpwd and opwd!=npwd:
    user=getuser(settings.operator)
    success=chgpwd(npwd,user)
    if success:
      settings.passwd=npwd
      return True
    return False
  else:
    print("Password mismatch...")
    return False

def dchgopwd():
  oid=input("Which operator?")
  pwd=gen_pwd()
  user=getuser(oid)
  if user==None:
    print("Operator ID doesn't exist")
    return
  success=chgopwd(oid,user,pwd)
  if success:
    print("password successfully changed")
    print("Please share this pwd with operator : ",pwd)
  else:
    print("ALERT: password could not be changed")


def ddeactivate():
  oid=input("Enter operator ID to be Deactivated: ")
  user=getuser(oid)
  if user==None:
    print("Operator ID doesn't exist")
    return
  success=deactivate(oid,user)
  if success:
    print("-> ->operator DEactivated successfully...")
  else:
    print("ALERT: operator could not be deactivated")  

def dactivate():
  oid=input("Enter operator ID to be Activated: ")
  user=getuser(oid)
  if user==None:
    print("Operator ID doesn't exist")
    return
  success=activate(oid,user)
  if success:
    print("-> ->operator Activated successfully...")
  else:
    print("ALERT: operator could not be activated")  

def dstockrecd():
  system("cls")
  print("~~~ Stock Received at Outlet ~~~")
  pid=input("Enter product id:")
  qty=input("Enter quantity:")
  uprice=input("Enter product unit price:")
  if not isproductavl(pid):
    print("New product entry form :")
    pname=input("Enter product name :")
    sid=input("Enter supplier id :")
    addproduct(pid,pname,sid)
  if not isstockavl(pid):
    print("New stock entry form :")
    tqty=input("Enter product threshold qty:")
    mqty=input("Enter product min order qty:")
    addstock(pid,qty,uprice,tqty,mqty)
  else:
    incrstock(pid,qty,uprice)
  addpurchase(pid,qty,uprice)
  print("Success: Stock updated fully")

def dauditlog():
  system("cls")
  print("~~~ Audit Log Form ~~~")
  dfrom=input("From date (like 21-May-2023): ")
  dto=input("To date (like 25-May-2023): ")
  data=auditlog(dfrom,dto)
  if data==None:
    print("No log found during this period")
  else:
    plog(data)

def dsales():
  system("cls")
  print("~~~ Sales Entry Form ~~~")
  cart=[]
  while True:
    d={}
    pid=input("Enter product ID: ")
    if not isstockavl(pid):
      print("product ID",pid,"not available at",settings.outlet)
    else:
      qty=input("Enter quantity  : ")
      d.update({"product_id":pid,"sold_qty":float(qty)})
      cart.append(d)
    ans=input("More items (y/n)? ")
    if ans.lower()=="n":
      break
    elif ans.lower()=="y":
      continue
    print("Press either 'y' or 'n' ...")
  cphone=input("Enter customer phone # : ")
  if not iscustavl(cphone):
    print("Customer entry form :")
    cname=input("Enter customer name : ")
    cdob=input("Enter customer dob (like 21-may-2023): ")
    success=addcustomer(cphone,cname,cdob)
    if success:
      print("-> -> -> customer added sucessfully...")
    else:
      print("ALERT: customer could not be added ...")
      return
  data=billedcart(cart)
  tot=data[0]
  cart=data[1]
  for item in cart:
    print("%s %6.2f %6.2f %10.2f"%(item["product_id"],item["sold_qty"],item["unit_price"],item["amount"]))
  ans=input("Have you collected Rs."+str(tot)+" (y/n) ? ")
  if ans.lower()=="y":
    mode=input("Payment mode (cash/bank) ? ")
  success=addsalestxn(cphone,tot,mode)
  if not success:
    print("sales txn couldn't be added for some reason...")
    print("you can refund the amount to customer...")
    return False
  txn=gettxnid(cphone)
  print("customer txn_id generated :",txn)
  success=addsalesdet(cart,txn)
  if not success:
    print("sales txn couldn't be added for some reason...")
    print("you can refund the amount to customer...")
    return False
  input("-> -> -> Sales txn added fully... press enter for invoice...")
  dpinvoice(txn)

def dpinvoice(txn=None):
  if txn==None:
    txn=input("enter transaction id:")
  data_txn=getsalestxn(txn)
  data_detail=getsalesdetail(txn)
  if data_txn==None:
    print("txn not available")
  else:
    pinvoice(data_txn,data_detail)

def doprcashrep():
  data=oprcashrep()
  poprcashrep(data)

def doutletcashrep():
  data=outletcashrep()
  poutletcashrep(data)

def ddailydemandrep():
  data=dailydemandrep()
  pdailydemandrep(data)