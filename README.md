delete-forgotten-web-accounts
=============================

Helps you to delete web accounts you've long forgotten based on the emails they sent you

Description
-----------
Checks your IMAP server for received emails, sorts them by the amount of emails received, extracts their hostname and matches them against the http://justdelete.me database, leaving you with a HTML page, providing all the links you need to delete the accounts.

Usage
-----

	usage: delete-forgotten-accounts.py [-h] [--username USERNAME]
	                                    [--password PASSWORD] [--server SERVER]

	optional arguments:
	  -h, --help           show this help message and exit
	  --username USERNAME  IMAP username
	  --password PASSWORD  IMAP password
	  --server SERVER      IMAP server
