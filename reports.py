from domspkg.queries import *
from os import system
from domspkg import settings 
import datetime
from fpdf import FPDF

def plog(data):
  '''plog() prints Security Audit Log of Operator changes'''
  system("cls")
  print("Ratnadeep Supermarkets Pvt Ltd".center(50,"~"))
  print("Security Audit Log".center(50,))
  print("-"*50)
  print("User ID    Action     By   On At")
  print("-"*50)
  for row in data:
    print(row[2].ljust(10),row[1].ljust(10),row[0],row[3].strftime("%d-%b-%Y at %H:%M %p"))
  print("-"*50)

def pinvoice(txn,det):
  '''pinvoice() prints latest invoice of the given customer'''  
  system("cls")
  print("Ratnadeep Supermarkets Pvt Ltd".center(45,"~"))
  trow=txn[0]
  print((trow["location"]+","+trow["city"]).center(45))
  print("Txn ID:",trow["id"],"...@...",datetime.datetime.strftime(trow["paid_time"],"%d-%b-%Y %H:%M %p"))
  print("Operator:",trow["op_name"])
  print("Customer:",trow["cu_name"])
  print("-"*45)
  print("PRODUCT_NAME       QUANTITY   RATE     AMOUNT")
  print("-"*45)
  for drow in det:
    print("%s %6.2f %6.2f %10.2f"%(drow["product_name"].ljust(20),drow["sold_qty"],drow["unit_price"],drow["amount"]))
  print("-"*45)
  print("Total Amount:",trow["tot_amount"])
  print("Payment Mode:",trow["payment_mode"])

def poprcashrep(data):
  '''poprcashrep() prints current-day txn-wise report of the operator'''  
  if data==None:
    return
  cash=0
  bank=0
  system("cls")
  print("Ratnadeep Supermarkets Pvt Ltd".center(57,"~"))
  print("\n  ~~~~~    %s Operator Cash Report for Today    ~~~~~\n"%settings.operator)
  print("-"*57)
  print("Date & Time         Txn ID    Txn Amount     Payment Mode")
  print("-"*57)
  for row in data:
    print(datetime.datetime.strftime(row["paid_time"],"%d:%b:%Y %H:%M")," ",row["id"],"     ",row["tot_amount"],"      ",row["payment_mode"])
    if row["payment_mode"]=="cash":
      cash = cash + row["tot_amount"]
    elif row["payment_mode"]=="bank": 
      bank = bank + row["tot_amount"]
  print("-"*57)
  print("Cash total=",cash,"Bank total=",bank)

def poutletcashrep(data):
  '''poutletcashrep() prints current-day operator-wise report of the outlet'''  
  if data==None:
    return
  cash=0
  bank=0
  tod=datetime.date.today()
  system("cls")
  print("Ratnadeep Supermarkets Pvt Ltd".center(50,"~"))
  print("\n~~~~~ %s Outlet Cash Report for "%settings.operator+datetime.datetime.strftime(tod,"%d-%b-%Y")+" ~~~~\n")
  print("-"*50)
  print("Operator    Total Amount    Payment Mode")
  print("-"*50)
  for row in data:
    print(row["operator_id"].ljust(15),"%8.2f"%row["total_amount"],row["payment_mode"].center(15))
    if row["payment_mode"]=="cash":
      cash = cash + row["total_amount"]
    elif row["payment_mode"]=="bank": 
      bank = bank + row["total_amount"]
  print("-"*50)
  print("Cash total=",cash,"Bank total=",bank)

def pdailydemandrep(data):
  '''pdailydemandrep() prints & generates pdf
of the products whose availability quantity
touches, or fallen down below the threshold quantity'''  
  tod=datetime.date.today()
  pdf=FPDF()
  pdf.add_page()
  pdf.set_font("Arial","B",15)
  pdf.set_text_color(255,0,0)  #RGB
  pdf.set_fill_color(155,255,80)
  pdf.set_draw_color(50,150,175)
  if data==None:
    return
  system("cls")
  print("Ratnadeep Supermarkets Pvt Ltd".center(68,"~"))
  txt="\n          ~~~~~  Daily Demand Report for "+datetime.datetime.strftime(tod,"%d-%b-%Y")+"  ~~~~~\n"
  print(txt)
  pdf.cell(200,10,txt=txt,ln=2,fill=True,border=1,align="L")
  txt="-"*68
  print(txt)
  pdf.cell(200,10,txt=txt,ln=2,fill=True,border=1,align="L")
  txt="Outlet  Product  Supplier  Order_Qty  (Available_Qty/Threshold_Qty)"
  print(txt)
  pdf.cell(200,10,txt=txt,ln=2,fill=True,border=1,align="L")
  txt="-"*68
  print(txt)
  pdf.cell(200,10,txt=txt,ln=2,fill=True,border=1,align="L")
  for row in data:
    txt=row["outlet_id"]+"    "+str(row["product_id"])+"   "+str(row["supplier_id"])+"      "+str(row["order_qty"])+"     ( "+str(row["available_qty"])+" / "+str(row["threshold_qty"])+" )"
    print(txt)
    pdf.cell(200,10,txt=txt,ln=2,fill=True,border=1,align="L")
  txt="-"*68
  print(txt)
  pdf.cell(200,10,txt=txt,ln=2,fill=True,border=1,align="L")
  filename="ddr"+str(tod)+".pdf"
  pdf.output(filename,"F")
  print(filename,"generated and saved in the current directory")