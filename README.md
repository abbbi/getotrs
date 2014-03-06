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
  --url URL        Base URL to otrs (http://host/)
  --ticket TICKET  Ticket URL to download
                   (otrs/index.pl?Action=AgentTicketZoom;TicketID=7496)
  --user USER      OTRS Username
  --pw PW          OTRS Password
  --folder FOLDER  Folder to download stuff (default full subject ticket id)
</pre>

EXAMPLE
------------
<pre>
getotrs.py --url https://otrs.url.de/ --ticket 7496 --user username --pw password
</pre>

