import git
import os
import datetime
cur_time = datetime.datetime.utcnow().isoformat()

# Open the local repo path, and the YAML file to edit
dir_path = os.path.dirname(os.path.realpath(__file__))
repo_path = os.path.join(dir_path, 'greenhouse-log')
yaml_path = os.path.join(repo_path, '_data', 'whiteboard.yml')

repo = git.Repo(repo_path)

def write_yaml(img_src):
    with open(yaml_path, "a") as whiteboard_yaml:
        whiteboard_yaml.write('-\n')
        whiteboard_yaml.write('  src: {}\n'.format(img_src))
        whiteboard_yaml.write('  date: {}\n'.format(cur_time))

# Update link to latest YAML
def update_yaml_link(img_src):
    write_yaml(img_src)
    # print(yaml_path)
    repo.git.add('_data/whiteboard.yml')
    repo.git.commit(message="Adding new whiteboard image {} UTC".format(cur_time))

    repo.git.pull('origin', 'master')
    repo.git.push('origin', 'master')

