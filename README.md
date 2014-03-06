getotrs
=======

Download otrs ticket attachments to local folder

USAGE
------------

<pre>
usage: getotrs.py [-h] --url URL --ticket TICKET --user USER --pw PW
                  [--folder FOLDER]

optional arguments:
  -h, --help       show this help message and exit
  --url URL        Base URL to otrs (https://host/)
  --ticket TICKET  Ticket ID as seen in URL (TicketID=7496 = 7496)
  --user USER      OTRS Username
  --pw PW          OTRS Password
  --folder FOLDER  Folder to download stuff (default full subject ticket id)
</pre>

EXAMPLE
------------

Download all attachments to automatically created folder:

 getotrs.py --url https://otrs.url.de/ --ticket 7496 --user username --pw password

Download attachments to specified folder:

 getotrs.py --url https://otrs.url.de/ --ticket 7496 --user username --pw password --folder download

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
