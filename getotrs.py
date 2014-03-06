#!/usr/bin/env python
import argparse
import mechanize
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("--url", help="Base URL to otrs (http://host/)", type=str, required=1)
parser.add_argument("--ticket", help="Ticket URL to download (otrs/index.pl?Action=AgentTicketZoom;TicketID=7496)", type=str, required=1)
parser.add_argument("--user", help="OTRS Username", type=str, required=1)
parser.add_argument("--pw", help="OTRS Password", type=str, required=1)
args = parser.parse_args()

base_url = args.url
otrs_path = args.ticket
username = args.user
password = args.pw

browser=mechanize.Browser()

browser.open(base_url+otrs_path)
browser.select_form(name='login')
browser['User'] = username
browser['Password'] = password
browser.submit()

data = BeautifulSoup(browser.response().read())

if 'Login failed!' in data.get_text():
    print 'Login failed! Your username or password was entered incorrectly.'
    exit

attachments=[]
for a in data.find_all('a', href=True):
    if 'AgentTicketAttachment' in a['href']:
        print "Found Attachment:", a['href']
        if a['href'] not in attachments:
            attachments.append(a['href'])

for file in attachments:
    print base_url+file
    t = file.split('?')
    n = t[0].split('/')
    browser.retrieve(base_url+file, n[3])
