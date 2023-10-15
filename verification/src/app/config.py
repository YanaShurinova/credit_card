"""Описание переменных окружения для подключения к БД."""
import os

from dotenv import load_dotenv

load_dotenv()

auth_url = os.environ.get('auth_url')
main_url = os.environ.get('main_url')
verify_url = os.environ.get('verify_url')
