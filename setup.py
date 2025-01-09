from setuptools import setup

APP_NAME = "Todo List Manager"
APP_VERSION = "1.0.0"

setup(
    name=APP_NAME,
    version=APP_VERSION,
    author="Naveed Jawaid",
    description="A simple and efficient To-Do List Manager",
    packages=["."],
    install_requires=[
        "tkcalendar>=1.6.1",
    ],
) 