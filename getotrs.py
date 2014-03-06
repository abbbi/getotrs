#!/usr/bin/env python
import mechanize
import requests
from bs4 import BeautifulSoup

username='user'
password="pass"

base_url = 'https://otrsurl.de/'
otrs_path = 'otrs/index.pl?Action=AgentTicketZoom;TicketID=7545;ArticleID=56272;ZoomExpand=1'

browser=mechanize.Browser()

browser.open(base_url+otrs_path)
browser.select_form(name='login')
browser['User'] = username
browser['Password'] = password
browser.submit()

data = BeautifulSoup(browser.response().read())

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
