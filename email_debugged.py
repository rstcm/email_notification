import difflib
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from netmiko import ConnectHandler

ip = '10.10.10.2'

device_type = 'arista_eos'

username = 'admin'
password = 'python'

command = 'show running'

#Connect to the device via SSH
session = ConnectHandler(device_type = device_type, ip = ip, username = username, password = password, global_delay_factor = 3)

#Entering enable mode
enable = session.enable()

#Sending the command and storing the output (running configuration)
output = session.send_command(command)

#Defining the file from yesterday, for comparison
device_cfg_old = ip + '_' + (datetime.date.today() - datetime.timedelta(days = 1)).isoformat()

#Writing the command output to a file for today
with open(ip + '_' + datetime.date.today().isoformat(), 'w') as device_cfg_new:
    device_cfg_new.write(output + '\n')
    
#Extracting the difference between yesterdays's and todays file in HTML format
with open(device_cfg_old, 'r') as old_file, open(ip + '_' + datetime.date.today().isoformat(), 'r') as new_file:
    difference = difflib.HtmlDiff().make_file(fromlines = old_file.readlines(), tolines = new_file.readlines(), fromdesc = 'Yesterday', todesc = 'Today')
    
#Sending the differences bia email
#Defining the e-mail parameters
fromaddr = 'python3testubuntu@gmail.com'
toaddr = 'python3testubuntu@gmail.com'

#More on MIME and multipart: https://en.wikipedia.org/wiki/MIME#Multipart_messages
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Daily Configuration Management Report'
msg.attach(MIMEText(difference, 'html'))
 
#Sending the email via Gmail's SMTP server on port 587
server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()
#SMTP connection is in TLS (Transport Layer Security) mode. All SMTP that follow will be encrypted.
server.login('python3testubuntu', 'ciscopython')
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()

#End of Program