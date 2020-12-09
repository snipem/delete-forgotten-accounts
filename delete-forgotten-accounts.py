#!/usr/bin/env python3
import imaplib
from getpass import getpass
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


def save_pickle(data):
    with open("entry.pickle", "wb") as f:
        pickle.dump(data, f)


def load_pickle():
    with open("entry.pickle", "rb") as f:
        data = pickle.load(f)

    return data


def get_json_response(url):

    response = urlopen(url)

    enc = response.read().decode("utf-8")
    data = json.loads(enc)

    return data


def print_enc(uncoded):
    if version == 2:
        print(uncoded.encode("utf-8"))
    else:
        uncoded = uncoded + "\n"
        sys.stdout.buffer.write(uncoded.encode("utf8"))


def pretty_print_json(json_string):
    return json.dumps(json_string, sort_keys=True, indent=4, separators=(",", ": "))


def get_domains(entry):
    """
    Returns a list of domains from an entry. Picks the nested domains list if present.
    If not present, the registered domain is extracted from the url.
    """

    if "domains" in entry:
        return entry["domains"]
    else:
        return [tldextract.extract(entry["url"]).registered_domain]


parser = argparse.ArgumentParser()
parser.add_argument("--username", help="IMAP username")
parser.add_argument("--server", help="IMAP server")

args = parser.parse_args()

if args.username is None:
    print("Username is not set")
    sys.exit(1)

if args.server is None:
    print("Server is not set")
    sys.exit(1)

M = imaplib.IMAP4_SSL(args.server)
M.login(args.username, getpass())
M.select()

domains = []
debug = False
mode = "Not Save"

##Get all FROM information from the IMAP server, containing all email senders that sent emails to the receiver

# Saves the IMAP return on disk when in debug mode
if debug == False:
    resp, data = M.uid("FETCH", "1:*", "(BODY.PEEK[HEADER.FIELDS (FROM)])")

    if resp != "OK":
        print("Response from IMAP Server was %s" % resp)
        sys.exit(1)

    if mode == "Save":
        save_pickle(data)

else:
    data = load_pickle()

# Access IMAP
for from_byte in data:
    try:
        from_line = from_byte[1].decode("ascii")
        from_mail = email.message_from_string(from_line)["from"]
        from_mailAddress = parseaddr(from_mail)[1]

        if "@" in from_mailAddress:
            mail_host = from_mailAddress.split("@")[1]
            mail_domain = tldextract.extract(mail_host)
            domains.append(mail_domain.registered_domain)
    except Exception:
        pass

M.close()
M.logout()

print("Found %d domains on imap server" % len(domains))

##Synchronization with the justdelete.me database
domains_sorted_with_numbers = collections.Counter(domains).most_common()
domains_sorted = [x[0] for x in domains_sorted_with_numbers]

domains_sorted_deletable = []

delete_me_json = get_json_response(
    "https://raw.githubusercontent.com/rmlewisuk/justdelete.me/master/sites.json"
)

print("Found %d domains in deleteme database" % len(delete_me_json))

for entry in delete_me_json:
    for domain in get_domains(entry):
        if domains_sorted.count(domain) > 0 and "url" in entry:
            domains_sorted_deletable.append([domain, entry["url"], ""])

##HTML Output
html_out = []
html_out.append("<html>\n\t<body>")

for domain_deletable in domains_sorted_deletable:

    link_line = (
        "\t\t<p><a href='"
        + domain_deletable[1]
        + "'>"
        + domain_deletable[0]
        + "</a></p>"
    )
    html_out.append(link_line)


html_out.append("\t</body>\n</html>")

html_write = "\n".join(html_out)
f = open("deleteaccounts.html", "w")
f.write(html_write)
f.close()
