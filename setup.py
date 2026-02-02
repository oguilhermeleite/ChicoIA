"""
Setup script for ChicoIA Telegram Bot
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="chicobot-telegram",
    version="1.0.0",
    author="ChicoIA",
    author_email="suporte@chicoia.com.br",
    description="Bot Telegram com IA conversacional para apostas esportivas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://chicoia.com.br",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Chat",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "chicobot=bot.main:main",
        ],
    },
)
