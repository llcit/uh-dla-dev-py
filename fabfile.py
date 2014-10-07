from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm
from fabric.context_managers import prefix
import time

def push_changes(message='fabfile committed this without comments.'):
    local("git add -A && git commit -m '%s'" % message)
    local("git push origin master")

def deploy(proj_dir, python_home, deploy_setting):
    
    """
    Usage\n: fab -H <HOST> -u <USER> deploy:proj_dir=<project dir name>,python_home=<python root path (full)>,deploy_setting=<django settings file> 
    
    Keyword arguments:
    project_dir: name of the directory containing the django project (no slashes)
    python_home: absolute path to pythonhome (e.g., /pythonapps) which is the parent dir of project_dir
    deploy_setting: file name of django settings module to use w/o .py
    """
    
    # Make sure user knows they are going modify production environment
    if not confirm("You are about to modify a production environment.\nAre you sure you want to do this?"):
        abort("Aborting at user request.")

    # Check to see if there is an existing git deployment on the remote
    deploy_dir = '%s/%s' % (python_home, proj_dir)
    with settings(warn_only=True):
        if run("test -d %s" % deploy_dir).failed:
            print('This is new deployment. Cloning from git.')
            run("git clone https://llcit@github.com/llcit/nflrcpydev.git %s" % deploy_dir)

    # Create a backup of the existing production directory
    with cd(python_home):
        if confirm("Do you want to backup the directory first?"):
            ts = time.strftime('%Y%m%d%H%M%S')
            run('tar cf backups/nflrcpydev-backup-%s.tar %s' % (ts, proj_dir))
            print('Backed up the code directory.')
        else:
            print('Not backing up.')

    # Run a git pull request from the repository, then run collectstatic to write to the static directories
    # Note: this works with a django installation that runs from a virtual environment as specified.
    with prefix('workon nflrcpython'):
        print('Now updating code from git...')
        with cd(deploy_dir):
            run("git pull origin master")
            run('python manage.py collectstatic --settings=nflrcsite.settings.%s' % deploy_setting)

def prompt():
    if not confirm("You are about to push changes to the repository to a production environment. Are you sure you want to do this?"):
        abort("Aborting at user request.")
    ts = time.strftime('%Y%m%d')
    print(ts)