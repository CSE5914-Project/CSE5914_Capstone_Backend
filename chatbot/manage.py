#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import multiprocessing
import time

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Start main() as a process
    p = multiprocessing.Process(target=main, name="Main")
    p.start()

    # Wait 30 seconds for main()
    time.sleep(30)

    # If thread is active
    if p.is_alive():
        print ("main() is running... let's kill it...")

        # Terminate main()
        p.terminate()

    # Cleanup
    p.join()

