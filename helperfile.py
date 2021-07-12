import numpy as np
from PIL import Image
import hashlib
import pandas as pd

#!Setup parameters
def setup():
    #Set up username
    name = input("Enter your username: ")
    with open("user.txt", "w") as f:
        f.write(name)
    #Set up credentials
    user = input("Enter your email: ")
    pswd = input("Enter your password: ")
    with open("credentials.txt", "w") as f:
        f.write(user+","+pswd)
    #Set up vigenere key
    key = input("Enter key for vigenere: ")
    with open("key.txt", "w") as f:
        f.write(key.upper()) #Saved in uppercase only
    #Set up RSA
    pq = input("Enter p and q (Eg. 11 17): ").rstrip("\n").split(" ")
    end = set_RSA(int(pq[0]),int(pq[1])) #e,n,d
    with open("end.txt", "w") as f:
        f.write(end)
    print("Username, Key and RSA credentials saved")

#!Setup RSA
def set_RSA(p,q):
    n = p * q
    tot = (p - 1) * (q - 1)
    #Get e
    for e in range(2, tot):
        if np.gcd(e, tot) == 1:
            break
    print("Public key is ({0}, {1})".format(n, e))
    #Get d
    for x in range(1, 10):
        rhs = 1 + x * tot
        if rhs % e == 0:
            d = int(rhs / e)
            break
    print("Private key is ({0}, {1})".format(n, d))
    end = str(e)+" "+str(n)+" "+str(d)
    return end

#!Text encrypt-Vigenere
def encrypt_text(mes, key):
    encrypted = ""
    key_length = len(key)
    i = 0
    for c in mes:
        if c.isalpha():
            k = ord(key[i%key_length])-ord("A")
            #For small
            if c.islower(): shifter = ord("a")
            #For caps
            else: shifter = ord("A")
            c = chr((ord(c) - shifter + k)%26 + shifter)
            i += 1
        encrypted += c
    return encrypted

#!Text decrypt-Vigenere
def decrypt_text(mes, key):
    decrypted = ""
    key_length = len(key)
    i = 0
    for c in mes:
        if c.isalpha():
            k = ord(key[i % key_length]) - ord("A")
            # For small
            if c.islower():
                shifter = ord("a")
            # For caps
            else:
                shifter = ord("A")
            c = chr((ord(c) - shifter - k) % 26 + shifter)
            i += 1
        decrypted += c
    return decrypted

#!Image encrypt-Random
def encrypt_image(img, seed):
    #Set seed
    np.random.seed(seed)
    #Generate random image
    rimg = 10*np.random.randint(0, 256, size=img.shape)
    #Encrypt
    encrypted_image = img+rimg
    return encrypted_image

#!Image decrypt-Random
def decrypt_image(img, seed):
    #Set seed
    np.random.seed(seed)
    #Generate random image
    rimg = 10 * np.random.randint(0, 256, size=img.shape)
    #Decrypt
    decrypted_image = img - rimg
    return decrypted_image

#!Convert image to csv data
def img2csv(img):
    df = pd.DataFrame(img)
    return df.to_csv(index=False)

#!RSA encrypt data
def encrypt_rsa(data, e, n):
    #Encryption for integer
    if isinstance(data, int):
        return pow(data,e,n)
    #Encryption for text
    encrypted = ""
    for i in data:
        encrypted += str(pow(ord(i),e,n))+ " "
    return encrypted

#!RSA decrypt
def decrypt_rsa(data, d, n):
    #Decryption for integer
    if isinstance(data, int):
        return pow(data,d,n)
    #Decryption for text in list form
    decrypted = ""
    for i in data:
        decrypted += chr(pow(int(i),d,n))
    return decrypted

#!Digital Signature-sender
def sender_ds(message):
    #Get private key
    with open("end.txt", "r") as f:
        end = f.read().rstrip("\n").split(" ")
    n,d = int(end[1]), int(end[2])
    #Get hasher and hash
    hasher = hashlib.blake2b(digest_size=2)
    hasher.update(message)
    hash_hex = hasher.hexdigest()
    hash = int(hash_hex,16)
    encr_hash = encrypt_rsa(hash,d,n)
    return str(encr_hash)

#!Digital Signature-receiver
def receiver_ds(message, rcvd_hash):
    #Get hasher and hash
    hasher = hashlib.blake2b(digest_size=2)
    hasher.update(message)
    hash_hex = hasher.hexdigest()
    hash = int(hash_hex, 16)
    #Compare
    if hash == rcvd_hash:
        print("Signature: Authenticated")
    else:
        print("Signature: Error/Tampered")

#!Send text mail
def make_text_mail(e, n):
    #Get your username
    with open("user.txt", "r") as f:
        username = "U~"+f.read().rstrip("\n")
    #Get text message
    message = input("Enter message: ")
    #Get key
    key = open("key.txt","r").read().rstrip("\n")
    #Encrypt message with vigenere
    encr_message = "M~"+encrypt_text(message, key)
    #Encrypt key with RSA
    encr_key = "K~"+encrypt_rsa(key, e, n)
    #Digital signature encrypted hash
    encr_hash = "H~"+sender_ds(message.encode())
    #Merge them into a single message
    print("Protocol: U~ K~ H~ M~")
    merged = username+'\n'+encr_key+'\n'+encr_hash+'\n'+encr_message+'\n'
    print(merged)
    return merged

#!Send image mail
def make_image_mail(e, n):
    #Get your username
    with open("user.txt", "r") as f:
        username = "U~" + f.read().rstrip("\n")
    #Get SEED
    seed = int(input("Enter SEED: "))
    #Get image path
    image_path = input("Enter image path: ")
    #Encrypt image
    #Load image in grayscale
    img = np.array(Image.open(image_path).convert("L"))
    encrypted_image = encrypt_image(img, seed)
    #Convert to csv to send
    conv_img = img2csv(encrypted_image)
    #Encrypt seed
    encr_seed = "S~"+str(encrypt_rsa(seed, e, n))
    #Digital signature hash for image
    encr_hash = "H~"+sender_ds(img)
    #Get shape
    shape = "X~"+str(encrypted_image.shape)
    #Merge
    print("Protocol: U~ S~ H~")
    merged = username+'\n'+encr_seed+'\n'+encr_hash+'\n'
    print(merged)
    return merged, conv_img

#Receive text part
def receive_text(body):
    #Initialize variables
    decr_message, decr_key, decr_seed, decr_hash = 0,0,0,0
    #Separate lines
    sections = body.rstrip('\n').split('\n')
    # Get private key
    with open("end.txt", "r") as f:
        end = f.read().rstrip().split(' ')
        e = int(end[0])
        n = int(end[1])
        d = int(end[2])
    #The first one should always be "U~"
    if "U~" not in sections[0]:

        return 0, decr_message, decr_key, decr_seed, decr_hash
    #Separate sections
    for part in sections:
        tags = part.rstrip('\r').split('~')
        #Decode now
        tag = tags[0]
        content = tags[1]
        #Username
        if tag == 'U':
            print("Username: "+content)
            users = pd.read_csv("creds.csv", index_col=0)
            es = int(users.loc[content]['E'])
            ns = int(users.loc[content]['N'])
        #Key
        elif tag == 'K':
            key = content.rstrip().split(' ')
            decr_key = decrypt_rsa(key,d,n)
            print("Key: "+decr_key)
        #Seed
        elif tag == 'S':
            seed = int(content.rstrip())
            decr_seed = decrypt_rsa(seed,d,n)
            print("Seed: ", decr_seed)
        #Hash
        elif tag == 'H':
            hash = int(content.rstrip())
            #Get sender's public key
            decr_hash = decrypt_rsa(hash,es,ns)
            print("Hash: ", decr_hash)
        #Message
        elif tag == 'M':
            #We know we'll have K for sure when M is sent
            message = content.rstrip()
            if decr_key != 0:
                decr_message = decrypt_text(message,decr_key)
                print("Message: "+decr_message)

    return 1, decr_message, decr_key, decr_seed, decr_hash
