from machine import  Pin, Timer
import  time


    
import network
try:
  import usocket as socket
except:
  import socket

ap = network.WLAN(network.AP_IF) # create access-point interface

ap.config(essid='Geiger') # set the SSID of the access point
ap.config(max_clients=10) # set how many clients can connect to the network
ap.active(True) # activate the interface

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())

def web_page():
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
  <body><h1>radiation level is: """ + str(radiation) + """</h1></body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


p1 = Pin(18, Pin.IN)
p2 = Pin(21, Pin.OUT)


def impulse():
    p2.value(0)
    time.sleep_ms(100)
    p2.value(1)
    
def Radiation(x):
    global radiation
    global count
    if p1.value()==1:
        radiation = count/(radiation + time.ticks_ms()) 
        impulse()
        count += 1
        
    
tim = Timer(-1)
start = time.ticks_ms()
impulse()
radiation = 0
start = 0
count = 1
tim.init(period=100, mode=Timer.PERIODIC, callback=Radiation)
while True:
    time.sleep_ms(100)
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    response = web_page()
    conn.send(response)
    conn.close()
    radiation += 1

