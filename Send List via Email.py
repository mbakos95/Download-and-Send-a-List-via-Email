import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def login_and_download(username, password):
    # Specify the path to the webdriver for your browser (e.g., Chrome)
    driver = webdriver.Chrome('path_to_chromedriver')

    # Open the website
    driver.get("https://example.com/login")

    # Fill in the login form
    username_field = driver.find_element_by_id("username")
    username_field.send_keys(username)
    password_field = driver.find_element_by_id("password")
    password_field.send_keys(password)
    login_button = driver.find_element_by_id("login-button")
    login_button.click()

    # Wait for the page to load
    time.sleep(5)

    # Find and click on the download button
    download_button = driver.find_element_by_id("download-button")
    download_button.click()

    # Wait for the download to complete (you may need to adjust this timing)
    time.sleep(10)

    # Close the browser
    driver.close()

def send_email(sender_email, sender_password, receiver_email, subject, body, file_path):
    # Set up SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Open the file to be sent
    with open(file_path, "rb") as attachment:
        # Add file as application/octet-stream
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file_path}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Send email
    server.sendmail(sender_email, receiver_email, text)

    # Quit SMTP server
    server.quit()

# Provide your login credentials, email credentials, and other details
username = "your_username"
password = "your_password"
sender_email = "your_email@gmail.com"
sender_password = "your_email_password"
receiver_email = "receiver_email@gmail.com"
subject = "Excel file from the website"
body = "Please find the attached Excel file."

# Execute the login and download function
login_and_download(username, password)

# Path to the downloaded file
file_path = "path_to_downloaded_file/excel_file.xlsx"

# Send the email with the downloaded file attached
send_email(sender_email, sender_password, receiver_email, subject, body, file_path)
