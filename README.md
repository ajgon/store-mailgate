store-mailgate
==============

A simple postfix mailgate to export desired emails to files on disc.

## Installation

1. Put `store-mailgate.py` somewhere in your path (i.e. `/usr/local/bin/store-mailgate.py`)
2. Configure `store-mailgate.conf` based on the provided sample config, then move it to the place where you store config files (typically `/etc/store-mailgate.conf`)
3. Add this to the end of your postfix `master.cf` file (replace paths to application and config file with your own, also change host and port of the relay if you adjusted them in configuration):

        store-mailgate  unix    -       n       n       -       -       pipe
          flags= user=vmail:vmail argv=/usr/local/bin/store-mailgate.py /etc/store-mailgate.conf ${recipient}

        127.0.0.1:10028 inet    n       -       n       -       10      smtpd
                -o content_filter=
                -o receive_override_options=no_unknown_recipient_checks,no_header_body_checks
                -o smtpd_helo_restrictions=
                -o smtpd_client_restrictions=
                -o smtpd_sender_restrictions=
                -o smtpd_recipient_restrictions=permit_mynetworks,reject
                -o mynetworks=127.0.0.0/8
                -o smtpd_authorized_xforward_hosts=127.0.0.0/8

4. Add the following to your postfix `main.cf`:

        content_filter = store-mailgate

5. Restart postfix
