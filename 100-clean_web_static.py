#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import env, cd, lcd, local, run

env.hosts = ["104.196.168.90", "35.196.46.172"]


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of most recent archives to keep.
            If set to 0, only the most recent archive will be kept.
    """
    try:
        number = int(number)
    except ValueError:
        print("Invalid number provided. Please provide a valid integer.")
        return

    if number < 0:
        print("Number must be a non-negative integer.")
        return

    with lcd("versions"):
        archives = sorted(os.listdir("."))
        archives_to_delete = archives[:-number] if number > 0 else archives[:-1]

        if archives_to_delete:
            print("Deleting local archives:")
            for archive in archives_to_delete:
                print("Removing:", archive)
                local("rm -f {}".format(archive))

    with cd("/data/web_static/releases"):
        archives = run("ls -tr | grep web_static_").split()
        archives_to_delete = archives[:-number] if number > 0 else archives[:-1]

        if archives_to_delete:
            print("Deleting remote archives:")
            for archive in archives_to_delete:
                print("Removing:", archive)
                run("rm -rf {}".format(archive))
