import csv
import requests
from datetime import date
import smtplib

CSV_URL = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'


def get_current_date():
      day = int(date.today().day)
      if day < 10:
            new_day = '0' + str(day)
      else:
            new_day = str(day)
      month = str(date.today().month)


      year = str(date.today().year)


      current_date = new_day + '/0' + month + '/' + year

      return current_date


def download_data_and_search():
      with requests.Session() as s:

            download = s.get(CSV_URL)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

            for row in my_list:
                  if row[0] == get_current_date() and row[6] == 'Poland':

                      data =  'INFECTED:' + row[4] + ', DEAD:' + row[5]
                      return  data



def start():
      print('Starting script...')
      print('Checking for an update...')
      new_data =  download_data_and_search()
      print('Done...')
      print('#####'*5)
      print(new_data)
      print('#####'*5)
      print('I will send an E-mail!')
      send_mail(new_data)

def send_mail(data):

    server = smtplib.SMTP('example', 123 )  # give your SMTP name and port number
    server.starttls()
    server.login('login@login.com','password') # give login and password to mail from witch script will send an email
    message = data
    server.sendmail(
        'example@example.com', # give email login
        'example@example.com', # give receivers e mail address
        message)
    server.quit()
    print('E-mail has been send.')



def main():
    start()

if __name__ == "__main__":
    main()