#!/usr/bin/env python
import os
import argparse
import requests
import zipfile
import tarfile
import json
import sys
from base64 import b64decode
if not 'win32' in sys.platform:
    import magic

def unpack(file):
    destdir=file+'_data/'

    if os.path.exists(destdir):
        print 'Skip decompress, already exists: ' + destdir
        return

    if not 'win32' in sys.platform:
        m = magic.open(magic.MIME)
        m.load()
        type = m.file(file)
        if type == None:
            type = file
    else:
        type = file 

    if 'text/plain' in type or type.endswith('.txt'):
        return

    if 'application/zip' in type or type.endswith('.zip'):
        print 'Decompress .zip into: ' + destdir
        createdir(destdir)
        try:
            with zipfile.ZipFile(file) as zf:
                try:
                    zf.extractall(destdir)
                    zf.close()
                except:
                    print 'error decompressing'
        except zipfile.BadZipfile:
            print 'Error: file is not a correct zipfile'
    elif 'application/x-gzip' in type or 'application/x-tar' in type or type.endswith('.tar.gz'):
        print 'Decompress .tar.z into: ' + destdir
        createdir(destdir)
        if tarfile.is_tarfile(file):
            try:
                with tarfile.TarFile.open(file) as tf:
                    tf.extractall(destdir)
                    tf.close()
            except tarfile.ExtractError, e:
                print 'error decompressing' + str(e)

def createdir(destdir):
    try:
        os.makedirs(destdir)
    except OSError, e:
        print 'Error creating directory:'+ e.strerror
        exit(1)

def set_target_folder(ticket_id):
    if args.folder:
        if '_ticketid_' in args.folder:
            target_folder = args.folder.replace('_ticketid_', ticket_id)
        else:
            target_folder= args.folder
    else:
        target_folder =  ticket_id

    print 'Target Folder: ' + target_folder

    if not os.path.exists(target_folder):
        createdir(target_folder)

    return target_folder

def get_json_data(username,password, url):
    payload = {
        'UserLogin': username,
        'Password': password,
        'AllArticles': '1',
        'Attachments' : '1'
    }
    try:
        r = requests.get(url, params=payload, verify=False)
    except Exception as e:
        print 'Error accesing api %s', e
        sys.exit(1)

    return json.loads(r.content)


def find_attachments(data):
    attachments = []

    if len(data) < 1:
        print 'No valid json data found'
        sys.exit(1)

    cnt=0
    for td in data['Ticket']:
        print 'Ticket has %s articles' % len(td['Article'])
        for article in td['Article']:
            cnt=cnt+1
            try:
                print 'Article %s has %s attachments' % (cnt, len(article['Attachment']))
                for file in article['Attachment']:
                    attachments.append({ 'filename': file['Filename'], 'content' : file['Content']})
            except KeyError:
                print "No attachment for Article %s" % cnt

    return attachments

def save_attachments(attachments, target_folder):
    if len(attachments) > 0:
        processed=[]
        fc = 0
        for file in attachments:
            filename = file['filename'];

            pc = processed.count(filename);

            if pc > 0:
                fc=fc+1
                filename=str(fc)+'_'+filename

            targetfile = target_folder + '/' + filename

            if not os.path.exists(targetfile):
                with open(targetfile, 'w') as FH:
                    FH.write(b64decode(file['content']))
                    FH.close()
                    processed.append(filename)
                    if args.unpack:
                        unpack(targetfile)
            else:
                processed.append(filename)
                if args.unpack:
                    unpack(unicode(targetfile))
                print 'Skipping file ' + filename + ': already exists'
    else:
        print 'No attachments found'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='Base URL to otrs (http://host/)', type=str, required=1)
    parser.add_argument('--ticket', help='Ticket ID as seen in URL (TicketID=7496 = 7496)', type=str, required=1)
    parser.add_argument('--user', help='OTRS Username', type=str, required=1)
    parser.add_argument('--pw', help='OTRS Password', type=str, required=1)
    parser.add_argument('--folder', help='Folder to download stuff (default full subject ticket id)', type=str, required=0)
    parser.add_argument('-p','--pdf', help='Download ticket as printable PDF', action='store_true', required=0)
    parser.add_argument('-u','--unpack', help='Decompress downloaded files based on filetype (zip, tar.gz)', action='store_true', required=0)
    args = parser.parse_args()

    username = args.user
    password = args.pw

    url = args.url+args.ticket

    data = get_json_data(username,password,url)
    tf = set_target_folder(data['Ticket'][0]['TicketNumber'])
    attachments = find_attachments(data)
    save_attachments(attachments, tf )
