from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import string
import random
import time



#Return field's position x,y
def GetXY(Field):
    xy=Field.get_attribute("id")
    x,y=xy.split('_')
    return int(x),int(y)

# Right clicks for every undiscovered elements that surround a given point(x,y)
def RightClicks(x,y):
    Fields=HiddenSurrounding(x,y)
    print(x," ",y,"  ", len(Fields))
    for x in Fields:
        action=ActionChains(driver)
        action.context_click(x).perform()
        print("RightClick")


# Left clicks for every undiscovered elements that surround a given point(x,y)
def LeftClicks(x,y):
    Fields=HiddenSurrounding(x,y)
    for Field in Fields:
        Field.click()
      

#returns undiscovered fields that surround a given point (x, y)
def HiddenSurrounding(x,y):
    tab = ['eee' for p in range(8)]   #eee means empty
    tab[0]=str(x+1)+'_'+str(y) # to the down
    tab[1]=str(x-1)+'_'+str(y) #to the up
    tab[2]=str(x)+'_'+str(y+1)  #to the right
    tab[3]=str(x)+'_'+str(y-1)  #to the left
    tab[4]=str(x-1)+'_'+str(y+1) #to the up right
    tab[5]=str(x+1)+'_'+str(y+1) #to the down right
    tab[6]=str(x-1)+'_'+str(y-1) #to the left up
    tab[7]=str(x+1)+'_'+str(y-1) #to the left down

    count=0
    H=[]
    for i in range(8):
        xpath="//*[(contains(@class,'square blank'))and not(contains(@style,'display')) and(@id='" + tab[i] + "')]"  
        Hidden=driver.find_elements_by_xpath(xpath)
        H=H+Hidden
    return H  
        
#returns Flags that surround a given point
def HowManyFlags(x,y):
    tab = ['eee' for p in range(8)]   #eee means empty
    tab[0]=str(x+1)+'_'+str(y) # to the down
    tab[1]=str(x-1)+'_'+str(y) #to the up
    tab[2]=str(x)+'_'+str(y+1)  #to the right
    tab[3]=str(x)+'_'+str(y-1)  #to the left
    tab[4]=str(x-1)+'_'+str(y+1) #to the up right
    tab[5]=str(x+1)+'_'+str(y+1) #to the down right
    tab[6]=str(x-1)+'_'+str(y-1) #to the left up
    tab[7]=str(x+1)+'_'+str(y-1) #to the left down

    count=0
    F=[]
    for i in range(8):
        xpath="//*[(contains(@class,'square bombflagged'))and not(contains(@style,'display')) and(@id='" + tab[i] + "')]"  
        Flags=driver.find_elements_by_xpath(xpath)
        F=F+Flags
    return len(F)


#Setting the flag in places where there is definitely a bomb for 1,2,3,4,5,6,7,8
def SetAllFlags():
    for i in range(1,8):
        xpath="//*[(contains(@class,'square open"+str(i)+"')) and not(contains(@style,'display'))]"
        FoundElements=driver.find_elements_by_xpath(xpath)
        FoundElements=set(FoundElements)-set(L)-set(D)
        for it in FoundElements:
            x,y=GetXY(it)
            HiddenFields=len(HiddenSurrounding(x,y))
            Flags=HowManyFlags(x,y)
            #start = time.time()
            if(((HiddenFields+Flags)==i)and(HiddenFields!=0)):   
                RightClicks(x,y)
            if(HiddenFields==0):
                L.append(it)
            if(Flags==i):
                D.append(it)
            #end = time.time()


            
#unhide fields where there is no bomb
def ClickOpenFields():
    for i in range(1,8):
        xpath="//*[(contains(@class,'square open"+str(i)+"')) and not(contains(@style,'display'))]"
        FoundElements=driver.find_elements_by_xpath(xpath)
        FoundElements=set(FoundElements)-set(L)
        for itt in FoundElements:
            x,y=GetXY(itt)
            if(HowManyFlags(x,y)==i):
                LeftClicks(x,y)
                #if a given point is surrounded by the number of flags equal to the value of a given point, i.e. 1,2,3,4,5,6,7,8
                # then I click on all the other fields that surround it.
           
         



D=[]
L=[]
adress='http://minesweeperonline.com'
driver=webdriver.Chrome()
driver.maximize_window()
driver.get(adress)


while True:
    SetAllFlags()
    ClickOpenFields()




