import requests
from bs4 import BeautifulSoup
from datetime import *
import re
from datetime import date, timedelta
import smtplib
from details import roll_array


def spider():

    count = 0
    cn = 0
    while count <= 1270:
        new_url = 'url{}'.format(count)
        print count
        for i in range(3):
            try:
                new_source_code = requests.get(new_url, timeout=50)
                break
            except Exception:
                print "exception is due to 1"
                pass
        new_plain_text = new_source_code.text
        new_soup = BeautifulSoup(new_plain_text)
        for new_link in new_soup.find_all('a', attrs={'class': 'title'}):
            new_title = new_link.string
            new_title = new_title.strip()
            new_href = 'url' + new_link.get('href')
            try:
                print new_title
            except Exception:
                cn = cn + 1
                pass
            user_detail(new_href, new_title)
        count = count + 50
    print 'Scan completed :)'
    print cn


def user_detail(user_url, book_name):
    for i in range(15):
        try:
            user_source_code = requests.get(user_url, timeout=50)
            break
        except Exception:
            print "exception is due to 2"
            pass
    user_plain_text = user_source_code.text
    user_soup = BeautifulSoup(user_plain_text)
    for user_link in user_soup.find_all('td', {'class': 'status'}):
        for i in range(2):
            try:
                user_title = user_link.getText().strip()
                if(user_title == 'Available' or user_title == 'Item withdrawn' or ('transit' in user_title)):
                    continue
                else:
                    roll = re.findall('\d+', user_title)
                    roll_no = roll[0]
                    del roll[0]
                    try:
                        tdate = user_link.findNextSibling('td', {'class': 'date_due'})
                    except Exception:
                        print "exception is due to 3"
                        continue
                    for datee in tdate.find_all('span'):
                        try:
                            datee = datee.getText()
                            due_date = datetime.strptime(datee, '%d/%m/%Y').date()
                        except Exception:
                            print "exception is due to 4"
                            continue
                        today_date = date.today() + timedelta(days=1)
                        if today_date == due_date and roll_no in roll_array:
                            send_to = roll_array[roll_no]
                            send_mail(send_to, book_name, roll_no)
                            print "Notification sent to ", roll_no, " for ",book_name
                break
            except Exception:
                print "exception is due to 5"
                pass

def send_mail(send_to, book_name, roll_no):
    fromaddr = 'email_id'
    toaddrs = send_to
    username = 'email_id'
    password = 'password'
    msg = '''Hello %s,

    Tomorrow is the due date for '%s'.
    Please Return/Re-issue the book on or before due date.



    ---The system is under testing if you find any problem, feel free to reply---''' % (roll_no, book_name)
    msg = "\r\n".join(["From: Name <email_id>", "To: " + toaddrs, "Subject: Due date reminder: " + book_name , "", msg])
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls() 
    server.login(username, password)
    server.sendmail('From: Name <email_id>', toaddrs, msg)
    server.quit()

spider()
