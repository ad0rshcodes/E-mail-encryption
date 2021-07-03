import smtplib
import pandas as pd
import numpy as np
from smtplib import SMTP


def vignere(message, key):

    message = message.replace(" ", "")
    message = message.lower()

    j = 0

    enc_message = ''

    for i in message:

        x = ord(i) + ord(key[j]) - 2 * ord('a')
        y = x % 26 + ord('a')

        enc_message += chr(y)

        j += 1

        if j > (len(key) - 1):
            j = 0

    return enc_message, key


def send_mail(u, p):
    receivers_email = input("email of the receiver:")

    message = input("What's the message you want to send:")

    key = input("key:")

    enc_message, key = vignere(message, key)

    enc_message = enc_message + ',' + key

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(u, p)

    s.sendmail(u, receivers_email, enc_message)

    s.quit()
