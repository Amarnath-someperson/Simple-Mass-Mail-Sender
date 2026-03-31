# Code snippets referenced -

# Source - https://stackoverflow.com/a/12424439
# Posted by David Okwii, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-20, License - CC BY-SA 4.0
#
import smtplib
import csv
from email.mime.text import MIMEText
import itertools
import threading
import time
import sys


filename_csv = input("\033[34mcsv filename with details of the recipients:\033[0m ")
filename_text = input("\033[34mlocation of text file for email:\033[0m ")

data = []
unsent = []
sent = []

sender = input("\033[34msender email id:\033[0m ")
pwd = input("\033[34msender pwd (use GApps App Password):\033[0m ")
subject = input("\033[34mmail subject:\033[0m ")


text = open(filename_text).read()

#terminal looks

line = 2
chars = ['/', '|', '\\']
done = False

def animate():
    global line
    global chars
    global done
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        print(f"\033[1;2H      \033[47m <{c}> sending mails...\n\033[0m")
        time.sleep(0.1)
    sys.stdout.write('\rDone! Mails have been sent.   ')

with open(filename_csv, newline = '') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        data.append(row)

def send_email(user, pwd, recipient, subject, body):
    global line
    global unsent
    global sent

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    MESSAGE = MIMEText(body, 'plain', 'utf-8')
    MESSAGE["Subject"] = SUBJECT
    # Prepare actual message
    # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    # """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, MESSAGE.as_string().encode('utf-8'))
        server.close()

        print (f'\033[{line % 7 + 1};2H \033[32m [-] successfully sent the mail to ' + recipient + "\033[0m")
        line = line + 1
        sent.append(recipient)
    except Exception as e:
        unsent.append(recipient)
        print (f"\033[{line % 7 + 7};2H\033[35m  [x] failed to send mail to addr:" + recipient + "\033[0m")

print("\033[2J")

t = threading.Thread(target=animate)
t.start()

#long process here

try:
    for i in data:
        mail_body = text.replace("<company>", i[1])
        send_email(sender, pwd, i[0].strip(), subject, mail_body)

    with open('unsent.log', 'w') as f:
        f.write(str(unsent))

    with open('sent.log', 'w') as f:
        f.write(str(sent))
except:
    print(f"\033[2;2H      \033[44m <{c}> [EXCEPTION] Process terminated. Check logs for sent/unsent mails.\033[0m")

    done = True

done = True
