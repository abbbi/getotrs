getotrs
=======

Download otrs ticket attachments to local folder

USAGE
------------

<pre>
usage: getotrs.py [-h] --url URL --ticket TICKET --user USER --pw PW
                  [--folder FOLDER] [--pdf]

optional arguments:
  -h, --help       show this help message and exit
  --url URL        Base URL to otrs (http://host/)
  --ticket TICKET  Ticket ID as seen in URL (TicketID=7496 = 7496)
  --user USER      OTRS Username
  --pw PW          OTRS Password
  --folder FOLDER  Folder to download stuff (default full subject ticket id)
  --pdf            Download ticket as printable PDF
</pre>

EXAMPLE
------------

Download all attachments to automatically created folder:

 getotrs.py --url https://otrs.url.de/ --ticket 7496 --user username --pw password

Download attachments to specified folder:

 getotrs.py --url https://otrs.url.de/ --ticket 7496 --user username --pw password --folder download

Download ticket as printable PDF:

 getotrs.py --url https://otrs.url.de/ --ticket 7496 --user username --pw password --pdf

Predefined path, _ticketid_ is replaced with real ticket number, so files go to /logfiles/<ticketnumber>:

 getotrs.py --url https://otrs.url.de/ --user username --pw password --folder /logfiles/_ticketid_ --ticket 7496


BASHRC
------------

 alias getotrs='python /path/to/getotrs.py --url https://otrs.url.de/ --user username --pw password --folder /logfiles/_ticketid_ --ticket'

So simply:

 getotrs 7545

will do the job and places ticket information to /logfiles/2014030680000094 for example.

DEPENDENCIES
------------
additional packages may have to be installed (debian):

<pre>
 python-bs4
 python-mechanize
</pre>

TODO
------------
 * does not handle attachments with different contents but same attachment name
