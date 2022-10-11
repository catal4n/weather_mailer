import requests
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googletrans import Translator

def get_weather_data(city):
    translator = Translator()
    API_KEY= '6280e45b9a3800ffd7054d0dc58f868c'
    URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    data = requests.get(URL).json()
    description = str(data['weather'][0]['description'])
    traducere = translator.translate(description, dest='ro', src='en')
    temperatureC = int(data['main']['temp']) - 273.15 #Kelvin
    tempResimtita = int(data['main']['feels_like']) - 273.15 #feels
    format_temp = "{:.2f}".format(temperatureC)
    oras = data['name']
    presiune = str(data['main']['pressure'])
    umiditate = str(data['main']['humidity'])
    print('Oras:' + oras + '\n' + 'Cer: ' + traducere.text.title() + '\n' +
          'Temperatura: ' + str(format_temp) +'°C' +
          '\n'+ 'Se resimte ca: ' + str("{:.2f}".format(tempResimtita)) + '°C' + '\n' +
          'Presiune: ' + presiune + ' mm Hg' + '\n' + 'Umiditate: ' + umiditate + ' %')

    messagex = ('Oras:' + oras + '\n' + ' Cer: ' + traducere.text.title() + '\n' +
                ' Temperatura: ' + str(format_temp) +'°C' +
                '\n'+ ' Se resimte ca: ' + str("{:.2f}".format(tempResimtita)) + '°C' + '\n' +
                ' Presiune: ' + presiune + ' mm Hg' + '\n' + ' Umiditate: ' + umiditate + ' %')

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "ryone13@gmail.com"  # Enter your address
    receiver_email = input('Email:')  # Enter receiver address
    password = "xskrucjeuqqmdviq"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Weather report"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = f" {messagex}"
    messagebody = MIMEText(text, "plain")
    message.attach(messagebody)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print('Mail sent')
    except KeyError as e:
        print('Mail cannot be sent!')

if __name__ == '__main__':
    city=input('City: ')
    get_weather_data(city)