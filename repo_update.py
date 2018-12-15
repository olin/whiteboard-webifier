from git import Repo
import os
import datetime
cur_time = datetime.datetime.utcnow().isoformat()

# Open the local repo path, and the YAML file to edit
dir_path = os.path.dirname(os.path.realpath(__file__))
repo_path = os.path.join(dir_path, 'greenhouse-log')
yaml_path = os.path.join(repo_path, '_data', 'whiteboard.yml')

repo = Repo(repo_path)

def write_yaml():
    with open(yaml_path, "a") as whiteboard_yaml:
        whiteboard_yaml.write('-\n')
        whiteboard_yaml.write('  src: {}\n'.format('http://localhost:4000/assets/balloon.png'))
        whiteboard_yaml.write('  date: {}\n'.format(cur_time))

# Update link to latest YAML
def update_yaml_link():
    write_yaml()
    repo.git.add(yaml_path)
    repo.git.commit("Adding new whiteboard image {} UTC".format(cur_time))

    repo.git.pull('origin', 'master')
    repo.git.push('origin', 'master')
