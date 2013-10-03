#!/usr/bin/python

from ConfigParser import RawConfigParser
import email
import email.header
import smtplib
import sys
import os
import time
import uuid
import unicodedata
import re

# Taken from Django
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

_cfg = RawConfigParser()
_cfg.read(sys.argv[1])
cfg = dict()
for sect in _cfg.sections():
    cfg[sect] = dict()
    for (name, value) in _cfg.items(sect):
        cfg[sect][name] = value

message = email.message_from_string(sys.stdin.read())

relay = (cfg['relay']['host'], int(cfg['relay']['port']))
fileformat = cfg['destination']['format']

store = False

if 'filter_any' in cfg and cfg['filter_any']:
    for header in cfg['filter_any']:
        if header in message and message[header] == cfg['filter_any'][header]:
            store = True
else:
    store = True

if 'filter_all' in cfg and cfg['filter_all']:
    for header in cfg['filter_all']:
        store = store and header in message and message[header] == cfg['filter_all'][header]
elif 'filter_any' not in cfg or not cfg['filter_any']:
    store = True

if store:
    if fileformat == 'timestamp':
        filename = str(int(time.time() * 1000000))
    elif fileformat == 'uuid':
        filename = str(uuid.uuid4())
    else:
        filename = slugify(unicode(' '.join([x[0] for x in email.header.decode_header(message['Subject'])])))

    target = open(os.path.join(cfg['destination']['dir'], filename + '.eml'), 'w')
    target.write(message.as_string())
    target.close()

from_addr = message['From']
to_addr = sys.argv[2:]

smtp = smtplib.SMTP(relay[0], relay[1])
smtp.sendmail( from_addr, to_addr, message.as_string() )
