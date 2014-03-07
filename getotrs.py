#!/usr/bin/env python
import os
import argparse
import mechanize
import requests
import zipfile
import tarfile
import magic
from bs4 import BeautifulSoup

def unpack(file):
    destdir=file+'_data/'

    if os.path.exists(destdir):
        print 'Skip decompress, already exists: ' + destdir
        return

    m = magic.open(magic.MIME)
    m.load()
    type = m.file(file)
    if 'application/zip' in type:
        print 'Decompress .zip into: ' + destdir
        createdir(destdir)
        try:
            with zipfile.ZipFile(file) as zf:
                try:
                    zf.extractall(destdir)
                except:
                    print 'error decompressing'
        except zipfile.BadZipfile:
            print 'Error: file is not a correct zipfile'
    elif 'application/x-gzip' in type:
        print 'Decompress .tar.z into: ' + destdir
        createdir(destdir)
        if tarfile.is_tarfile(file):
            try:
                with tarfile.TarFile.open(file) as tf:
                    tf.extractall(destdir)
            except tarfile.ExtractError, e:
                print 'error decompressing' + str(e)

def createdir(destdir):
    try:
        os.makedirs(destdir)
    except OSError, e:
        print 'Error creating directory:'+ e.strerror
        exit(1)

def login():
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

    return data

def set_target_folder(data):
    if args.folder:
        if '_ticketid_' in args.folder:
            target_folder = args.folder.replace('_ticketid_', data.title.string.split(' ')[0])
        else:
            target_folder= args.folder
    else:
        target_folder =  data.title.string.split(' ')[0]

    print 'Target Folder: ' + target_folder

    if not os.path.exists(target_folder):
        createdir(target_folder)

    return target_folder

def find_attachments(data):
    attachments=[]
    for a in data.find_all('a', href=True):
        if 'AgentTicketAttachment' in a['href']:
            if a['href'] not in attachments:
                print 'Found Attachment:', a['href']
                attachments.append(a['href'])
        if 'Action=Logout' in a['href']:
            logout_url = a['href']
            print 'Logout URL: ' + logout_url
        if 'AgentTicketPrint;TicketID' in a['href']:
            if not 'ArticleID' in a['href']:
                pdf_url = a['href'];

    return attachments, logout_url, pdf_url

def download_pdf(pdf_url, target_folder):
    if args.pdf:
        print 'Download ticket PDF file: ' + target_folder + '/ticketdata.pdf'
        try:
            browser.retrieve(base_url+pdf_url, target_folder + '/ticketdata.pdf')
        except:
            print 'Error retrieving PDF file'

def download_attachments(attachments, target_folder):
	if len(attachments) > 0:
	    processed=[]
	    for file in attachments:
	        t = file.split('?')
	        n = t[0].split('/')
	        
	        filename = n[3];
	
	        fc = processed.count(n[3]);
	
	        if fc > 0:
	            nfc=fc+1
	            filename=str(nfc)+'_'+filename
	
	        targetfile = target_folder + '/' + filename
	
	        if not os.path.exists(targetfile):
	            print 'Downloading:' + base_url+file + ' to: ' + targetfile
	            try:
	                browser.retrieve(base_url+file, targetfile)
	                processed.append(filename)
	                if args.unpack:
	                    unpack(targetfile)
	            except mechanize.URLError, e:
	                print 'ERROR downloading file:' + str(e)
	            except mechanize.HTTPError, e:
	                print 'ERROR downloading file:' + str(e)
	        else:
	            processed.append(filename)
	            if args.unpack:
	                unpack(targetfile)
	            print 'Skipping file ' + filename + ': already exists'
	else:
	    print 'No attachments found'

def logout(logout_url):
	print 'Logout'
	p = browser.click_link(url=logout_url)
	browser.open(p)
	resp =  BeautifulSoup(browser.response().read())
	if 'Abmelden' or 'Logout' in  resp.title.string:
	    print "Ok"
	browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='Base URL to otrs (http://host/)', type=str, required=1)
    parser.add_argument('--ticket', help='Ticket ID as seen in URL (TicketID=7496 = 7496)', type=str, required=1)
    parser.add_argument('--user', help='OTRS Username', type=str, required=1)
    parser.add_argument('--pw', help='OTRS Password', type=str, required=1)
    parser.add_argument('--folder', help='Folder to download stuff (default full subject ticket id)', type=str, required=0)
    parser.add_argument('--pdf', help='Download ticket as printable PDF', action='store_true', required=0)
    parser.add_argument('--unpack', help='Decompress downloaded files based on filetype (zip, tar.gz)', action='store_true', required=0)
    args = parser.parse_args()
	
    base_url = args.url
    otrs_path = 'otrs/index.pl?Action=AgentTicketZoom;TicketID=' + args.ticket + ';ZoomExpand=1'
    username = args.user
    password = args.pw
	
    browser=mechanize.Browser()
    data = login()
    tf = set_target_folder(data)
    attachments,logout_url,pdf_url = find_attachments(data)
    download_pdf(pdf_url, tf)
    download_attachments(attachments, tf )
    logout(logout_url)
