import getpass
import telnetlib

#Pre-config
Device = "xxx.xxx.xxx.xxx"
user = "xxx"
password = "xxx"
en_password = "xxx"

#Connect to device
print("Connecting to ",Device)
tn = telnetlib.Telnet(Device)

#Enter user ID
tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")

#Router access authentication
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

#Disable pause btw pages
tn.read_until(b">")
tn.write(b"terminal length 0\n")

#Exec "xxxxx" command and get its results
tn.read_until(b">")
tn.write(b"xxxxx\n")
device_config=tn.read_until(b">").decode('utf-8')

#Close connection
print("Disconnecting from ",Device)
tn.write(b"exit \n")
tn.read_all()

#Record to text file
filename = "Device_" + Device + '.txt'
saveoutput = open(filename,"w")
saveoutput.write(device_config+"\n")
saveoutput.close()
print("Output File: " + filename)

