from tools import current, unzip, textify, reconfiguration, setRepo, colorify, packagesList
from datetime import datetime
from pysondb import db

import urllib.request
import shutil
import json
import os

try:
    os.mkdir('/usr/lib/semicircles/')
except:
    pass

workspaces = db.getDb('/usr/lib/semicircles/workspaces.json')

def initialize():
    while True:
        created = datetime.now().strftime("%H:%M:%S %d %B, %Y")
        name = str(input('Project name: '))
        author = str(input('Author: '))
        description = (str(input('Description: ')))
        print(f'Created: {created}\n')
        boolean = str(input('Is everything right? [y/n] '))
        if boolean.lower() == 'y':
            if name and author and description:
                break
        print()

    if workspaces.reSearch('project_folder', current()):
        for query in workspaces.reSearch('project_folder', current()):
            workspaces.deleteById(query['id'])
        try:
            shutil.rmtree(current() + '/semi-packages/')
        except:
            pass

    workspaces.add(
        {
            "name"            : name,
            "author"          : author,
            "created"         : created,
            "project_folder"  : current(),
            "packages_folder" : current() + '/semi-packages',
        }
    )

    with open(f'{current()}/workspace.json', 'w') as file:
        workspace = {
            "name"        : name,
            "version"     : '1.0.0',
            "description" : description,
            "author"      : author,
            "created"     : created,
            "packages"    : [],
            "de4oult"     : 'Good luck with the project, buddy! ;)'
        }

        try:
            os.mkdir(current() + '/semi-packages') # create packages folder
        except:
            pass

        try:
            with open('/usr/lib/semicircles/.repo', 'w') as repo:
                repo.write('http://46.151.27.39/semi-packages/') # set default repo 
        except:
            pass

        file.write(json.dumps(workspace, indent=4)) # write configuration to workspace.json
        colorify('Workspace successfuly initialized', 'green')
        


def download(name):
    projects = workspaces.getBy(
        {
            "project_folder" : current()
        }
    )

    if projects and projects[0]:
        workspace = projects[0]
        with open(current() + '/workspace.json', 'r+') as file:
            configuration = json.loads(textify(file.readlines()))
            if name in packagesList(current() + '/semi-packages/'):
                colorify('Package already installed!', 'red')
                for package in packagesList(current() + '/semi-packages/'):
                    if package not in configuration['packages']:
                        reconfiguration(configuration, package, file)
                return                    

            saveTo = f'{str(workspace["packages_folder"])}/{str(name)}'
            try:
                urllib.request.urlretrieve(setRepo('.repo') + str(name) + '.zip', f'{saveTo}.zip')
                unzip(f'{saveTo}.zip', saveTo)
                reconfiguration(configuration, name, file)
                colorify('Package installed successfuly!', 'green')
                return
            except:
                colorify('Package not found!', 'red')
                return

    colorify('Workspace not initialized!', 'red')
    return

def build(name):
    pass

