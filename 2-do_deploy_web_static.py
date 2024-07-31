#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run

env.hosts = ["104.196.168.90", "35.196.46.172"]


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        True if the deployment was successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        print("Archive not found:", archive_path)
        return False

    file = os.path.basename(archive_path)
    name = file.split(".")[0]

    # Upload archive
    if put(archive_path, "/tmp/{}".format(file)).failed:
        print("Failed to upload archive to remote server")
        return False

    # Create release directory
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        print("Failed to create release directory")
        return False

    # Extract archive
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed:
        print("Failed to extract archive")
        return False

    # Cleanup
    if run("rm /tmp/{}".format(file)).failed:
        print("Failed to remove archive from /tmp")
        return False

    # Move contents and create symbolic link
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed:
        print("Failed to move contents to release directory")
        return False

    # Remove redundant directory and update current symlink
    if run("rm -rf /data/web_static/releases/{}/web_static && "
           "rm -rf /data/web_static/current && "
           "ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name, name)).failed:
        print("Failed to update current symlink")
        return False

    print("Deployment successful")
    return True
