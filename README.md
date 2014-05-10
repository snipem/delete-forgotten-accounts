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

Example
-------

If you run `python delete-forgotten-accounts.py --username yourusername@somewhere.com --password secretpassword --server imap.somewhere.com` the scripts parses your SSL secured IMAP server for all emails you ever received. The result will be a file named `deleteaccounts.html` in your current folder containing links like these:

[amazon.com](https://www.amazon.com/gp/help/customer/contact-us/ref=cu_cf_email?ie=UTF8&mode=email#a)
[aol.com](http://cancel.aol.com)
[battle.net](https://eu.battle.net/support/en/ticket/submit)
[bbc.co.uk](https://ssl.bbc.co.uk/id/settings/delete)
[booking.com](https://secure.booking.com/login.en-us.html?tmpl=profile/delete_account)
[boxee.tv](http://bbx.boxee.tv/user/delete)
[clickandbuy.com](https://customer.eu.clickandbuy.com/surfer/spring/settings-terminateaccount-flow)
[deviantart.com](https://www.deviantart.com/settings/deactivation)