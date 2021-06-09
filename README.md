getotrs
=======

Download otrs ticket attachments. Based on the ticket-id syncs all attachments
to a local folder and if desired decompresses possible archives. 

Uses the new OTRS 4.0.1 REST API, for REST API setup an predefined yml
description is included, see below.

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

EXAMPLES
------------

Download all attachments to automatically created folder:

 `getotrs` --url https://otrs.url.de/ --ticket 7496 --user username --pw password

Download attachments to specified folder:

 `getotrs` --url https://otrs.url.de/ --ticket 7496 --user username --pw password --folder download

Download attachments to specified folder and decompress zipped attachments:

 `getotrs` --url https://otrs.url.de/ --ticket 7496 --user username --pw password --folder download --unpack

Predefined path, __ticketid__ is replaced with real ticket number, so files go to /logfiles/<ticketnumber>:

<pre>
 `getotrs` --url URL --user username --pw password --folder /logfiles/_ticketid_ --ticket 7496
</pre>

CONFIG
------------

By default getotrs attempts to load `~/.getotrs` as config file, which can be
used to configure username/url/password. See example file.

OTRS WebService
------------

getotrs.yml includes an service description, in otrs 4.0.1 it is possible to import this service description
with the GenericInterface Webservices administration tool. The URL for this WebService is:

 https://otrs.url.de/otrs/nph-genericinterface.pl/Webservice/getotrs/TicketGet/

TRIVIA
------------
If a file with the same name is attached to the ticket twice, the filename will be appended
with an upcounting number (foo, 2_foo), 3_foo) and so on.
