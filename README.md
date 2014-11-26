getotrs
=======

Download otrs ticket attachments. Based on the ticket-id syncs all attachments
to a local folder and if desired decompresses possible archives. Also downloads
the printable pdf version of the ticket created by otrs.

Uses the new OTRS 4.0.1 REST API

USAGE
------------

<pre>
usage: getotrs.py [-h] --url URL --ticket TICKET --user USER --pw PW
                  [--folder FOLDER] [--pdf] [--unpack]

optional arguments:
  -h, --help       show this help message and exit
  --url URL        Base URL to otrs (http://host/)
  --ticket TICKET  Ticket ID as seen in URL (TicketID=7496 = 7496)
  --user USER      OTRS Username
  --pw PW          OTRS Password
  --folder FOLDER  Folder to download stuff (default full subject ticket id)
  --unpack         Decompress downloaded files based on filetype (zip, tar.gz)
</pre>

EXAMPLE
------------

Download all attachments to automatically created folder:

 getotrs.py --url https://otrs.url.de/otrs/nph-genericinterface.pl/Webservice/SN/TicketGet/ --ticket 7496 --user username --pw password

Download attachments to specified folder:

 getotrs.py --url https://otrs.url.de/otrs/nph-genericinterface.pl/Webservice/SN/TicketGet/ --ticket 7496 --user username --pw password --folder download

Download attachments to specified folder and decompress zipped attachments:

 getotrs.py --url https://otrs.url.de/otrs/nph-genericinterface.pl/Webservice/SN/TicketGet/ --ticket 7496 --user username --pw password --folder download --unpack

Predefined path, __ticketid__ is replaced with real ticket number, so files go to /logfiles/<ticketnumber>:

<pre>
 getotrs.py --url URL --user username --pw password --folder /logfiles/_ticketid_ --ticket 7496
</pre>

BASHRC
------------

<pre>
 alias getotrs='python /path/to/getotrs.py --url https://otrs.url.de/ --user username --pw password --folder /logfiles/_ticketid_ --ticket'
</pre>

So simply:

 getotrs 7545

will do the job and places ticket information to /logfiles/2014030680000094 for example.


OTRS WebService
------------

getotrs.yml includes an service description, in otrs 4.0.1 it is possible to import this service description
with the GenericInterface Webservices administration tool. The URL for this WebService is:

 https://otrs.url.de/otrs/nph-genericinterface.pl/Webservice/getotrs/TicketGet/

DEPENDENCIES
------------
additional packages may have to be installed (debian):

<pre>
 python-bs4
 python-mechanize
 python-magic
 python-json
 python-base64
</pre>

TRIVIA
------------
If a file with the same name is attached to the ticket twice, the filename will be appended
with an upcounting number (foo, 2_foo), 3_foo) and so on.
