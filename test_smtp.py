#!/usr/bin/env python3
"""
Simple script to test home SMTP
Author: Jose Vicente Nunez

Sample session:

./test_smtp.py --relay smtpout.XXXX.net --fromemail me@domain.com --to me@domain.com This is a test
Type your password and press enter:
send: 'mail FROM:<me@domain.com> size=199\r\n'
reply: b'250 <me@domain.com> sender ok\r\n'
reply: retcode (250); Msg: b'<me@domain.com> sender ok'
send: 'rcpt TO:<me@domain.com>\r\n'
reply: b'250 <me@domain.com> recipient ok\r\n'
reply: retcode (250); Msg: b'<me@domain.com> recipient ok'
send: 'data\r\n'
reply: b'354 OK\r\n'
reply: retcode (354); Msg: b'OK'
data: (354, b'OK')
send: b'Subject: This is a test\r\nFrom: me@domain.com\r\nTo: me@domain.com\r\nContent-Type: text/plain; charset="utf-8"\r\nContent-Transfer-Encoding: 7bit\r\nMIME-Version: 1.0\r\n\r\nThis is a test\r\n.\r\n'
reply: b'250 VQFeljt0P83tO mail accepted for delivery\r\n'
reply: retcode (250); Msg: b'VQFeljt0P83tO mail accepted for delivery'
data: (250, b'VQFeljt0P83tO mail accepted for delivery')
send: 'QUIT\r\n'
reply: b'221 p3plsmtpa12-07.prod.phx3.XXXX.net :SMTPAUTH: closing connection\r\n'
reply: retcode (221); Msg: b'p3plsmtpa12-07.prod.phx3.XXXX.net :SMTPAUTH: closing connection'


"""
import smtplib
from email.message import EmailMessage
import ssl
import getpass
import argparse

PORT = 465


def send_email(
        my_server: smtplib.SMTP_SSL,
        **kwargs
) -> None:
    password = getpass.getpass("Type your password and press enter: ")
    my_server.login(kwargs['from_e'], password)
    my_server.set_debuglevel(1)
    msg = EmailMessage()
    msg['Subject'] = kwargs['subject']
    msg['From'] = kwargs['from_e']
    msg['To'] = kwargs['to_e']
    msg.set_content(" ".join(kwargs['message']))
    my_server.send_message(msg)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    PARSER.add_argument('--relay', action='store', required=True, help='SMTP relay')
    PARSER.add_argument('--fromemail', action='store', required=True, help='Source email address')
    PARSER.add_argument('--toemail', action='store', required=True, help='Destination email address')
    PARSER.add_argument('--subject', action='store', default="This is a test", help='What is this all about?')
    PARSER.add_argument('message', type=str, nargs='+', help='Text message')
    ARGS = PARSER.parse_args()

    CONTEXT = ssl.create_default_context()
    with smtplib.SMTP_SSL(ARGS.relay, PORT, context=CONTEXT) as server:
        send_email(
            server,
            from_e=ARGS.fromemail,
            to_e=ARGS.toemail,
            subject=ARGS.subject,
            message=ARGS.message
        )
