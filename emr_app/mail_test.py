import os
import smtplib
from datetime import datetime

email_address = os.environ.get("EMR_GMAIL_NAME")
email_password = os.environ.get("EMR_GMAIL_PASSWORD")
input_time_format = "%Y-%m-%dT%H:%M:%S%z"
db_time_format = "%Y-%m-%d %H:%M:%S%z"

class AppointmentEmail():
    
    """ Use the following command in terminal to create 
        a simulated email server . . . 

        python3 -m smtpd -c DebuggingServer -n localhost:1010
    
        Change the function call from send_simulated_email, to 
        send_email in order to send real emails to recipients.
     """

    def send_email(self, recipient_email, message):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(email_address, email_password)
            smtp.sendmail(email_address, recipient_email, message)
    
    def send_simulated_email(self, recipient_email, message):
        with smtplib.SMTP('localhost', 1010) as smtp:
            smtp.sendmail(email_address, recipient_email, message)

    def created_appointment(self, appointment_data):
        provider = appointment_data.provider
        client = appointment_data.client
        print('Creating appointment email')
        print(appointment_data.date_time)
        datetimeObject = datetime.strptime(appointment_data.date_time, input_time_format)
        day = datetime.strftime(datetimeObject, '%A')
        date = datetime.strftime(datetimeObject, "%B %d, %Y")
        time = datetime.strftime(datetimeObject, "%I:%M %p")
        print(f'Your appointment is on {day} {date}, at {time}')
        subject = f'New appointment for {appointment_data.client.user.first_name}!'
        body = f'Hello, {appointment_data.client.user.first_name}.\n\nYou have been scheduled for an appointment with {appointment_data.provider.user.first_name} {appointment_data.provider.user.last_name} on {day}, {date}, at {time}. It is scheduled to last {appointment_data.duration} minutes.\n\n Please contact your provider at {appointment_data.provider.user.email} at least 24 hours before your appointment if you need to cancel or reschedule.\n\nBe Well,\n\nEvolving Recovery Team'
        message = f'Subject: {subject}\n\n{body}'
        self.send_simulated_email(client.user.email, message)



    def edited_appointment(self, appointment_data):
        print('editing appointment')
        print(appointment_data.date_time)
        provider = appointment_data.provider
        client = appointment_data.client
        datetimeObject = datetime.strptime(appointment_data.date_time, input_time_format)
        day = datetime.strftime(datetimeObject, '%A')
        date = datetime.strftime(datetimeObject, "%B %d, %Y")
        time = datetime.strftime(datetimeObject, "%I:%M %p")
        print(f'Your appointment is on {day}, {date}, at {time}')

        subject = f'Rescheduled appointment {client.user.first_name}.'
        body = f'Hello, {client.user.first_name}.\n\nYour appointment with {provider.user.first_name} {provider.user.last_name} has been rescheduled to {day}, {date}, at {time}. It is scheduled to last {appointment_data.duration} minutes.\n\n Please contact your provider at {provider.user.email} at least 24 hours before your appointment if you need to cancel or reschedule.\n\nBe Well,\n\nEvolving Recovery Team'
        message = f'Subject: {subject}\n\n{body}'
        self.send_simulated_email(client.user.email, message)
        
    def canceled_appointment(self, appointment_data):
        print('Canceling appointment')
        provider = appointment_data.provider
        client = appointment_data.client
        print(appointment_data.date_time)
        datetimeObject = appointment_data.date_time
        day = datetime.strftime(datetimeObject, '%A')
        date = datetime.strftime(datetimeObject, "%B %d, %Y")
        time = datetime.strftime(datetimeObject, "%I:%M %p")
        print(f'Your appointment is on {day}, {date}, at {time}')
        
        subject = f'Appointment Cancelation'
        body = f'Hello, {client.user.first_name}.\n\nYour appointment with {provider.user.first_name} {provider.user.last_name}, on {day}, {date}, at {time}, has been canceled.\n\n Please contact your provider at {provider.user.email} if you would like to reschedule.\n\nBe Well,\n\nEvolving Recovery Team'
        message = f'Subject: {subject}\n\n{body}'
        self.send_simulated_email(client.user.email, message)