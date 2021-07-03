plain_txt = input("Enter text to be encrypted: ")

plain_txt = plain_txt.replace(" ", "")
plain_txt = plain_txt.lower()


j = 0

encrypted = ''

key = input("Enter Key: ")

if len(key) >= len(plain_txt):

    for i in range(len(plain_txt)):
        x = ord(plain_txt[i]) - ord('a') + ord(key[i])

        encrypted += chr(x)

else:

    for i in plain_txt:

        x = ord(i) + ord(key[j]) - 2 * ord('a')
        y = x % 26 + ord('a')

        encrypted += chr(y)

        j += 1

        if j > (len(key) - 1):
            j = 0


print(encrypted)
