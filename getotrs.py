#!/usr/bin/env python
import os
import argparse
import mechanize
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('--url', help='Base URL to otrs (http://host/)', type=str, required=1)
parser.add_argument('--ticket', help='Ticket ID as seen in URL (TicketID=7496 = 7496)', type=str, required=1)
parser.add_argument('--user', help='OTRS Username', type=str, required=1)
parser.add_argument('--pw', help='OTRS Password', type=str, required=1)
parser.add_argument('--folder', help='Folder to download stuff (default full subject ticket id)', type=str, required=0)
parser.add_argument('--pdf', help='Download ticket as printable PDF', action='store_true', required=0)
args = parser.parse_args()

base_url = args.url
otrs_path = 'otrs/index.pl?Action=AgentTicketZoom;TicketID=' + args.ticket
username = args.user
password = args.pw

browser=mechanize.Browser()

try:
    browser.open(base_url+otrs_path)
except mechanize.URLError, e:
    print 'ERROR opening site:' + str(e)
    exit(1)
except mechanize.HTTPError, e:
    print 'ERROR downloading:' + str(e)
    exit(1)


browser.select_form(name='login')
browser['User'] = username
browser['Password'] = password
browser.submit()

data = BeautifulSoup(browser.response().read())

if 'Insufficient Rights' in  data.get_text():
    print 'Unable to open ticket information: wrong url?'
    exit(1)

if 'Login failed!' in data.get_text():
    print 'Login failed! Your username or password was entered incorrectly.'
    exit(1)

if args.folder:
    target_folder= args.folder
else:
    target_folder =  data.title.string.split(' ')[0]

print 'Target Folder:' + target_folder

attachments=[]
for a in data.find_all('a', href=True):
    if 'AgentTicketAttachment' in a['href']:
        print 'Found Attachment:', a['href']
        if a['href'] not in attachments:
            attachments.append(a['href'])
    if 'Action=Logout' in a['href']:
        logout_url = a['href']
        print 'Logout URL: ' + logout_url
    if 'AgentTicketPrint' in a['href']:
        pdf_url = a['href'];

if not os.path.exists(target_folder):
    os.makedirs(target_folder)

for file in attachments:
    t = file.split('?')
    n = t[0].split('/')
    if not os.path.exists(target_folder + '/' + n[3]):
        print 'Downloading:' + base_url+file
        try:
            browser.retrieve(base_url+file, target_folder + '/' + n[3])
        except mechanize.URLError, e:
            print 'ERROR downloading file:' + str(e)
        except mechanize.HTTPError, e:
            print 'ERROR downloading file:' + str(e)
    else:
        print 'Skipping file' + n[3] + ': already exists'

if args.pdf:
    print 'Download ticket PDF file:' 
    try:
        browser.retrieve(base_url+pdf_url, target_folder + '/ticketdata.pdf')
    except:
        print 'Error retrieving PDF file'

print 'Logout'
p = browser.click_link(url=logout_url)
browser.open(p)
resp =  BeautifulSoup(browser.response().read())
if 'Abmelden' or 'Logout' in  resp.title.string:
    print "Ok"
browser.close()
