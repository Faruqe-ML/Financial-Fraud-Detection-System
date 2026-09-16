import os
import random
import uuid
from dotenv import  load_dotenv

from config.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

load_dotenv()
import requests
from django.shortcuts import render, redirect
from twilio.rest import Client
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import send_mail


def generate_otp():
    return random.randint(100000, 999999)

def send_otp_email(email, otp, catagory):
    send_mail(
        'OTP for Your Registration',
        f"Dear User,\n\nYour One-Time Password (OTP) for {catagory} is {otp}.\n\nThis OTP is valid for a short time. Please do not share it with anyone.",
        'faruqeansari9@gmail.com',
        [email],
        fail_silently=False,
    )
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
def send_otp(phone_number, otp):


    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    return message.sid

def send_email(subject, message, email):

    send_mail(
        subject=subject,
        message=message,
        from_email="faruqeansari9@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )