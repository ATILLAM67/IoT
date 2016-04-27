import webiopi
import datetime
import calendar

GPIO = webiopi.GPIO

LIGHT = 2  # GPIO pin using BCM numbering
WEEKEND = 3

# on/off time hours 
ontimehours = [5,12,21]
offtimehours = [5,12,22]

# on/off time mins
ontimemis = [1,0,30]
offtimemis = [15,1,12]

# low state GPIO.LOW
low=GPIO.LOW

# high state GPIO.HIGH
high=GPIO.HIGH

# my control
ihome=1

# overwrite
iforcehigh=1


# setup function is automatically called at WebIOPi startup
def setup():
    # set the GPIO used by the light to output
    GPIO.setFunction(LIGHT, GPIO.OUT)
    GPIO.setFunction(WEEKEND, GPIO.OUT)

    # retrieve current datetime
    now = datetime.datetime.now()
    
    GPIO.digitalWrite(LIGHT, GPIO.LOW)
    GPIO.digitalWrite(WEEKEND, GPIO.LOW)

# loop function is repeatedly called by WebIOPi 
def loop():
    # retrieve current datetime
    now = datetime.datetime.now()

    # retrieve the current weekday
    nameoftoday = calendar.day_name[now.weekday()]


    # Set next weekend level 
    nextweekendstate=low


    # manage the disable control
    if ((((nameoftoday == "Saturday") or (nameoftoday == "Sunday")) and (ihome==1)) or (iforcehigh==1)):
       nextweekendstate = high
       
    # GPIO.digitalRead(WEEKEND) 
    currentweekendstate=GPIO.digitalRead(WEEKEND) 
 
    # toggle weekend
    if (currentweekendstate == low):
        GPIO.digitalWrite(WEEKEND,nextweekendstate)

        
        
    if (nextweekendstate == low) :
      
       # GPIO.digitalRead(WEEKEND) 
       currentweekendstate=GPIO.digitalRead(WEEKEND) 
 
       # toggle weekend
       if (currentweekendstate == high):
          GPIO.digitalWrite(WEEKEND,nextweekendstate) 
    
       # GPIO.digitalRead(LIGHT) 
       currentlightstate=GPIO.digitalRead(LIGHT) 
      
    
       # toggle light ON or OFF all days at the correct time
       if (((now.hour == ontimehours[0]) and (now.minute == ontimemis[0])) or ((now.hour == ontimehours[1]) and (now.minute == ontimemis[1])) or ((now.hour == ontimehours[2]) and (now.minute == ontimemis[3]))):
          if currentlightstate == low:
             GPIO.digitalWrite(LIGHT,high)

       if (((now.hour == offtimehours[0]) and (now.minute == offtimemis[0])) or ((now.hour == offtimehours[1]) and (now.minute == offtimemis[1])) or ((now.hour == offtimehours[2]) and (now.minute == offtimemis[3]))):
          if currentlightstate == high:
             GPIO.digitalWrite(LIGHT,low)
       
         
    # gives CPU some time before looping again
    webiopi.sleep(1)

# destroy function is called at WebIOPi shutdown
def destroy():
    GPIO.digitalWrite(LIGHT, GPIO.LOW)
    
@webiopi.macro
def getiforcehighValue():
   return int(iforcehigh)
   
@webiopi.macro
def setiforcehighValue(val): 
   global iforcehigh
   iforcehigh = int(val)
   return iforcehigh 