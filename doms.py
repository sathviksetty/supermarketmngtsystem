from domspkg.forms import  *
from domspkg.reports import  *
#from domspkg.queries import  *
#from domspkg.updates import  *
from os import system
from domspkg import settings 

dlogin()

while(True):
  if settings.manager:
    choice=dmngrmenu()
    if choice=="0":
      break
    elif choice=="1":
      daddoutlet()     
    elif choice=="2":
      daddopr() 
    elif choice=="3":
      daddsupplier() 
    elif choice=="4":
      daddproduct() 
    elif choice=="5":
      dpinvoice(None)
    elif choice=="6":
      doutletcashrep()
    elif choice=="7":
      ddailydemandrep()     
    elif choice=="8":
      dchgpwd()
    elif choice=="9":
      dchgopwd()
    elif choice=="10":
      ddeactivate()
    elif choice=="11":
      dactivate()
    elif choice=="12":
      dauditlog()
    elif choice=="13":
      dstockrecd()
    else:
      print("~~~ *** WRONG CHOICE *** ~~~")    
    input("Press ENTER key to continue...")
  else:
    choice=doprmenu()
    if choice=="0":
      break
    elif choice=="1":
      dsales()     
    elif choice=="2":
      dpinvoice(None)  
    elif choice=="3":
      doprcashrep()
    elif choice=="4":
      daddcustomer()   
    elif choice=="5":
      dchgpwd()
    else:
      print("~~~ *** WRONG CHOICE *** ~~~")    
    input("Press ENTER key to continue...")

print("***~~~ Thanks for using ROMS~~~***")   