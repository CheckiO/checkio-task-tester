import git
import shutil
import os

import checkio_task_tester.settings as S


def init():
    git.Repo.clone_from(S.INIT_REPO, S.REPO_FOLDER)
    shutil.rmtree(os.path.join(S.REPO_FOLDER, '.git'))

def link_repo(original_url):
    folder = os.path.abspath(S.REPO_FOLDER)
    repo = git.Repo.init(folder)
    for root, dirs, files in os.walk(folder):
        if root.endswith('.git') or '/.git/' in root:
            continue

        for file_name in files:
            abs_file_name = os.path.join(root, file_name)
            repo.index.add([abs_file_name])

    repo.index.commit("initial commit")
    origin = repo.create_remote('origin', original_url)
    origin.push(repo.refs)
    origin.fetch()
    repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master)