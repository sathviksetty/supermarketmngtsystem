Super Market Management System
Developed using Python 3.10.4 and MySQL 8.0.3 on Windows 11
===========================================================
I. Introduction

We have chosen to develop this Super Market Management System, as this is the most typical use case for using computers in a commercial environment.  
We have completely normalised the database tables until at least the boyce codd normal form has been achieved.
We have separated the front-end and back-end to simulate full stack environment, although none of the frameworks have been used.  
We have used core python and MySQL for the entire project.  This project’s emphasis is on writing clean, efficient and maintainable code rather than using high end frameworks or technologies.
This application is not only suitable for super markets, but also for any similar sales outlets like electronic shops, sports shops etc.
We have automated all the master data management, purchase & sales transactions, as well as the log in security audit log tracking to avoid or detect any fraudulent activity.  This kind of automation will help accountability for the business.  We have incorporated security features by recording and reporting audit log of operator creation, initial / password reset, activation/deactivation etc.
We have also automated the purchase orders of the stock in outlets whose available quantity touches or fall below the given threshold quantity.
We have generated reports like 1) customer invoice 2) operator cash collected report 3) outlet cash collected report 4) daily purchase demand report 5) audit log report

II. Project Description

The Super Market Management System, automates the process of introducing new outlets, operators, suppliers, products, customers, purchase & sales transactions, adding the stock as and when received at outlet, reducing the stock as and when it is sold.  It creates purchase order report of stocks whose available quantity goes below threshold quantity.  Once the daily purchase demand report is generated (as and when the report is run), the report is generated in the pdf format and saved in the current directory with the date stamp.  Once the report is generated, the items are marked as order placed until purchased stock receives at outlet, so to avoid repeat ordering of same items.
The Security feature has been introduced to safeguard from fraud.  The system allows operators to change their initial password, reset the password when they suspect it may have been compromised.  The manager can change the password on request from operator, he can deactivate / activate the operator when the operator is terminated or goes on long leave.  The system tracks all the changes to operator identity information like user creation, initial password reset, password reset by operator, password reset by manager, deactivation / activation etc.  The manager can get the audit log report between any two given dates.
The manager can get reports of cash collected by each and every operator in the given outlet.  The operator also can verify his own cash balance with the self-cash report. 
The system prints invoice for each customer transaction.  The manager / operator can re-print the invoice as and when needed.
Each outlet can have their own pricing of items, and the price can be reset when the new stock arrives.  Each and every transaction and each and every product in the cart is logged.  Every transaction is time-stamped for easy future reference.

III. Design Phase

We have chosen water fall method for the project, wherein we have created a 0 level DFD for the overall project, and from there drilled down to detail.
Data Flow diagrams have not been included here.

ROMS Python package structure
D:\PYTHON\ROMS (Project folder)
|   roms.py (Main program which calls functions in the package)
+---romspkg (Package folder)
|   |   forms.py (for Input forms)
|   |   queries.py (for pulling data from DB)
|   |   reports.py (for displaying / generating PDF of reports)
|   |   updates.py (for inserts / updates etc to DB)
|   |   settings.py (for maintaining global variables)
|   |   __init__.py (dummy file with no content)

DB Schema diagram has not been included here (however SQL statements attached in a separate file)
 
Different Menu displayed as per role of Operator/Manager
Various functions developed at Front-End vs Back-End

FE Function  --> 	BE Function
===========	=========
			            getmydb
Dlogin			      Login
DMngrMenu
DOprMenu
DAddCust		      AddCust
DAddOutlet				AddOutlet
DAddSupp					AddSupp
DAddProduct				AddProduct
DAddOperator			AddOperator
Dchgpwd						Chgpwd
Dchgopwd					Chgopwd
DAuditLog,Plog		AuditLog
DStockRecd				InsertStock
									IncrStock
									DecrStock
									AddPurchase
DoprCashRep				oprcashrep
PoprCashRep
DOutletCashReport	outletcashrep
Poutletcashrep
DPrintInvoice			PrintInvoice
DailyDemandRep		DailyDemandRep
Pdailydemandrep
DpInvoice					Pinvoice
Ppinvoice

IV. Implementation Phase

We have created the project folder, package folder, and modules necessary for Front-end, back-end separately.
We have developed login screen at the beginning.
Once the login is successful, the different menu is displayed based on the role of the user – i. e. operator / manager.
Then we have designed and created master tables at the DB level.
Then we have developed separate functions to manage each of the master tables.
Then we have floated master tables with some sample data – a few outlets, operators, suppliers, products, customers etc.
Then we have created the tables necessary to maintain stock received and stock available at store.
Then we have developed functions necessary to populate to stock received at store.
Once the stock is ready, we have created tables necessary to handle sales transactions, and sales details.
Then we have developed the functions necessary to handles the sales process.
Finally we have developed the functions to generate various reports – invoice, audit log, transaction-wise cash report of the individual operator, operator-wise cash report of the individual outlet, daily purchase demand report of the products whose available quantity touches / falls down below the threshold quantity of each product.

V. Conclusion & Future scope

Most common aspects of the Super Market Management have been developed with clear, efficient and maintainable code.
However, as always there is a scope for improvement.  We see the below features can be added to enhance this application in the future.
•	Graphical User Interface for the front-end to improve user experience.
•	API functions in the backend to improve scalability.
•	Reward points can be introduced to encourage customer engagement.
•	A new feature can be included to promote operator as manager

