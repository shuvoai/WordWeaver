#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    settings_module = config("DJANGO_SETTINGS_MODULE", default=None)
    if settings_module is None:
        print(
            "Error: no DJANGO_SETTINGS_MODULE found. Will NOT start devserver."
            "Remember to create .env file at project root. "
            "Check README for more info."
        )
        sys.exit(1)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    execute_from_command_line(sys.argv)
