import imaplib
import email
import pandas as pd


def fetch_mail(u, p):

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(u, p)

    imap.select('"[Gmail]/All Mail"', readonly=True)

    response, messages = imap.search(None, 'Unseen')

    print(response, messages)

    messages = messages[0].split()

    # print(messages)

    latest = int(messages[-1])

    res, msg = imap.fetch(str(latest), "(RFC822)")

    # print(latest)

    print(res, msg)

    for mail in msg:

        # print(mail[0]

        if isinstance(mail, tuple):
            msg = email.message_from_bytes(mail[1])
            print(msg)

    for part in msg.walk():
        b = part.get_payload()

    body = b.split(",")

    print(body)

    print(body[0])


cred = pd.read_csv("credentials.txt")
user = cred.columns[0]

passw = cred.columns[1]


fetch_mail(user, passw)
