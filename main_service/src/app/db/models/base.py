"""Модуль для инициализации переменной для генерации таблиц."""
from sqlalchemy.orm import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()
