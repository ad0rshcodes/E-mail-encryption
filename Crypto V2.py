# Import libraries
import smtplib
import imaplib
import email

import pandas as pd

from helperfile import *
from email.message import EmailMessage
import matplotlib.pyplot as plt

# Final code
# Get credentials
cred = open("credentials.txt", "r").read().split(",")
# Users
username = cred[0]
password = cred[1]
users = pd.read_csv("creds.csv", index_col=0)
print("Current Users: ", end='')
print(users.index.tolist())
# Ask if wanna send or receive
task = int(input("Enter task: 0-setup, 1-send, 2-receive: "))
# Setup
if task == 0:
    setup()
# Send
elif task == 1:
    # Start SMTP
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(username, password)
    print("Sending message")
    # Get receiver's email
    r_username = input("Enter receiver username: ")
    r_email = users.loc[r_username]['Email']
    r_e = int(users.loc[r_username]['E'])
    r_n = int(users.loc[r_username]['N'])
    print(r_email+":"+str(r_e)+":"+str(r_n))
    # Create message
    message = EmailMessage()
    message['Subject'] = input("Enter subject: ")
    message['From'] = username
    message['To'] = r_email
    task2 = int(input("Enter task: 0-text, 1-image: "))
    # Send Text
    if not task2:
        merged = make_text_mail(r_e, r_n)
        message.set_content(merged)
        s.send_message(message)
        print("Mail sent!")
    # Send Image
    else:
        merged, conv_img = make_image_mail(r_e, r_n)
        message.set_content(merged)
        message.add_attachment(conv_img.encode(
            'utf-8'), maintype='text', subtype='csv', filename="encrypted_img.csv")
        s.send_message(message)
        print("Mail sent!")
    s.quit()
# Receive
else:
    # Set up imap
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)
    imap.select('"[Gmail]/All Mail"', readonly=True)
    # Get message idexes
    response, messages = imap.search(None, "UnSeen")
    messages = messages[0].split()
    num_messages = len(messages)
    print("Messages unread: "+str(num_messages))
    # Get the number of messages to check
    checklen = int(input("How many unread messages to check: "))
    # checklen = 1
    for index in messages[num_messages-checklen:num_messages]:
        res, msg = imap.fetch(index, "(RFC822)")
        print("Getting message: " + str(int(index)))
        for mail in msg:
            if isinstance(mail, tuple):
                msg = email.message_from_bytes(mail[-1])
        for part in msg.walk():
            # Get text part
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                res, message, key, seed, hash = receive_text(body)
                if message != 0:
                    receiver_ds(message.encode(), hash)
                # If not a good one, res=1 will be good crypto mail
                if res == 0:
                    print("Not Crypto Email")
                    continue

            # Get attachment
            if part.get_content_type() == "text/csv":
                attachment = part.get_payload(decode=True).decode()
                # Save as encrypted_image.csv
                with open("encrypted_img.csv", "w") as f:
                    f.write(attachment)
                # We know we'll have decr_seed if image was sent
                csv = pd.read_csv("encrypted_img.csv")
                arr = csv.values
                decr_img = decrypt_image(arr, seed)
                # Check Signature
                receiver_ds(decr_img, hash)
                plt.imshow(decr_img)
                plt.savefig("img.jpeg")
                plt.show()
