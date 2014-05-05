import getpass, imaplib
import email
import tldextract
import collections
import pickle
import sys
import json
import argparse

version = sys.version_info[0]

# import only once
if version == 3:
    from urllib.request import urlopen
    from urllib.parse import quote
elif version == 2:
    from urllib2 import urlopen
    from urllib2 import quote
else:
    version == False

from email.utils import parseaddr

def savePickle(data):
	with open('entry.pickle', 'wb') as f:
		pickle.dump(data, f)

def loadPickle():
	with open('entry.pickle', 'rb') as f:
		data = pickle.load(f)  

	return data

def getJsonResponse(url):

    response = urlopen(url)

    enc = response.read().decode('utf-8')
    data = json.loads(enc)

    return data

def print_enc(uncoded):
    if version == 2:
        print (uncoded.encode("utf-8"))
    else:
        uncoded = uncoded +"\n"
        sys.stdout.buffer.write(uncoded.encode('utf8'))

def prettyPrintJson(jsonString):
    return json.dumps(jsonString, sort_keys=True,indent=4, separators=(',', ': '))


parser = argparse.ArgumentParser()
parser.add_argument("--username", help="IMAP username")
parser.add_argument("--password", help="IMAP password")
parser.add_argument("--server", help="IMAP server")

args = parser.parse_args()

M = imaplib.IMAP4_SSL(args.server)
M.login(args.username, args.password)
M.select()

domains = []
debug = True
mode = "Save"

##Get all FROM information from the IMAP server, containing all email senders that sent emails to the receiver

#Saves the IMAP return on disk when in debug mode
if (debug == False):
	resp,data = M.uid('FETCH', '1:*' , '(BODY.PEEK[HEADER.FIELDS (FROM)])')
	if (mode == "Save"):
		savePickle(data)
else:
	data = loadPickle()

for fromByte in data:
	try:
		fromLine = fromByte[1].decode('ascii')
		fromMail = email.message_from_string(fromLine)['from']
		fromMailAddress = parseaddr(fromMail)[1]

		if  "@" in fromMailAddress:
			mailHost =  fromMailAddress.split('@')[1]
			mailDomain = tldextract.extract(mailHost)
			domains.append(mailDomain.registered_domain)
	except Exception:
		pass
	 
M.close()
M.logout()

##Synchronization with the justdelete.me database
domainsSortedWithNumbers=collections.Counter(domains).most_common()
domainsSorted = [x[0] for x in domainsSortedWithNumbers]

domainsSortedDeletable = []

deleteMeJson = getJsonResponse("https://raw.githubusercontent.com/rmlewisuk/justdelete.me/master/sites.json")

for entry in deleteMeJson:

	for domain in entry['domains']:

		if domainsSorted.count(domain) > 0:
			domainsSortedDeletable.append([domain, entry['url'], ""])

##HTML Output
htmlOut = []
htmlOut.append("<html>\n\t<body>")

for domainDeletable in domainsSortedDeletable:

	linkLine = "\t\t<p><a href='"+domainDeletable[1]+"'>"+domainDeletable[0]+"</a></p>"
	htmlOut.append(linkLine)


htmlOut.append("\t</body>\n</html>")

htmlWrite = "\n".join(htmlOut)
f = open("deleteaccounts.html","w")
f.write(htmlWrite)
f.close()

