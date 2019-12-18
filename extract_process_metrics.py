import re
import os
from git import Repo
import pandas as pd
import time

# this is where we get commit messages
# SUFFIX = '.java'
# PROJECT = 'maven'
# PATH = 'dataset/raw_project/' + PROJECT
# VERSION = 'maven-3.0'  # ATTENTION: just TAG NAME, NO ..
# # this is where we get all target files list of a specific version
# OLD_PATH = 'old_version'
# OLD_NAME = 'guava-20.0'

# SUFFIX = '.c'
# PROJECT = 'esp-idf'
# PATH = 'dataset/raw_project/' + PROJECT
# VERSION = 'v3.0'  # ATTENTION: just TAG NAME, NO ..
# # this is where we get all target files list of a specific version
# OLD_NAME = 'esp-idf-3.0'

# SUFFIX = '.c'
# PROJECT = 'neovim'
# PATH = 'dataset/raw_project/' + PROJECT
# VERSION = 'v0.2.0'  # ATTENTION: just TAG NAME, NO ..
# # this is where we get all target files list of a specific version
# OLD_NAME = 'neovim-0.2.0'

# SUFFIX = '.c'
# PROJECT = 'freeswitch'
# PATH = 'dataset/raw_project/' + PROJECT
# VERSION = 'v1.5.0'  # ATTENTION: just TAG NAME, NO ..
# # this is where we get all target files list of a specific version
# OLD_NAME = 'freeswitch-1.5.0'

# SUFFIX = '.c'
# PROJECT = 'openssl'
# PATH = 'dataset/raw_project/' + PROJECT
# VERSION = 'OpenSSL_1_1_0'  # ATTENTION: just TAG NAME, NO ..
# # this is where we get all target files list of a specific version
# OLD_NAME = 'openssl-OpenSSL_1_1_0'

# SUFFIX = '.c'
# PROJECT = 'mpv'
# VERSION = 'v0.3.0'  # ATTENTION: just TAG NAME, NO ..
# # this is where we get all target files list of a specific version
# OLD_NAME = 'mpv-0.3.0'

# SUFFIX = '.c'
# PROJECT = 'freeradius-server'
# VERSION = 'release_3_0_0'  # ATTENTION: just TAG NAME, NO ..
# # this is where we get all target files list of a specific version
# OLD_NAME = 'freeradius-server-release_3_0_0'

# SUFFIX = '.c'
# PROJECT = 'git'
# VERSION = 'v2.11.0'  # ATTENTION: just TAG NAME, NO ..
# # this is where we get all target files list of a specific version
# OLD_NAME = 'git-2.11.0'

SUFFIX = '.c'
PROJECT = 'freeswitch'
VERSION = 'v1.8.0'  # ATTENTION: just TAG NAME, NO ..
# this is where we get all target files list of a specific version
OLD_NAME = 'freeswitch-1.8.0'


# =================================================================
PATH = 'dataset/raw_project/' + PROJECT
OLD_PATH = 'old_version'
# For a specific file, get the commit and diff info.
def get_file_commits(filename):
    repo = Repo(PATH)
    g = repo.git
    # try:
    #     # the file is not deleted or moved
    #     # file_commits = g.log(VERSION, '--all', '-p', '--full-history', filename).split('\n')
    #     file_commits = g.log(VERSION, '-p', '--', filename).split('\n')
    # except:
    # If the file is deleted or moved
    file_commits = g.log(VERSION, '-p', '--parents', '--', filename).split('\n')

    return file_commits


# get process metrics for a specific file
def get_process_metrics(commits):
    num_revision = 0
    num_add = 0
    num_deleted = 0
    author = set()

    for line in commits:
        len_line = len(line)
        # print(line[0:6])
        if len_line is 0:
            continue
        if line[0:6] == 'commit':
            num_revision += 1
            continue
        if line[0:6] == 'Author':
            if line not in author:
                author.add(line)
            continue
        if line[0] is '+' and len_line is not 1 and line[1] is not '+':
            num_add += 1
            continue
        if line[0] is '-' and len_line is not 1 and line[1] is not '-':
            num_deleted += 1
    # if num_add < num_deleted
    return [num_revision, num_add, num_deleted, len(author)]


def get_all_files():
    ret = []
    owd = os.getcwd()
    os.chdir(OLD_PATH)
    for root, dirs, files in os.walk(OLD_NAME):
        for file in files:
            if file.endswith(SUFFIX):
                ret.append(os.path.join(root, file))
    os.chdir(owd)
    return ret


def main():
    all_files = get_all_files()
    metrics_for_all_file = []
    prefix_len = len(OLD_NAME)
    lfiles = []
    lnum_revision = []
    lnum_add = []
    lnum_deleted = []
    lnum_author = []
    # file = all_files[0]
    # print(file)
    # print(get_file_commits(file[prefix_len+1:]))
    # commits = get_file_commits(file[prefix_len + 1:])
    # print(get_process_metrics(commits))
    for file in all_files:
        lfiles.append(file)
        file_tmp = file[prefix_len + 1:]
        print('For ' + file_tmp)
        commits = get_file_commits(file_tmp)
        pmetrics = get_process_metrics(commits)
        lnum_revision.append(pmetrics[0])
        lnum_add.append(pmetrics[1])
        lnum_deleted.append(pmetrics[2])
        lnum_author.append(pmetrics[3])
    df = pd.DataFrame({
        'Name': lfiles,
        'NumRevision': lnum_revision,
        'NumAdded': lnum_add,
        'NumDeleted': lnum_deleted,
        'NumAuthor': lnum_author
    })
    print(metrics_for_all_file)
    print(len(metrics_for_all_file))
    file_name = OLD_NAME + time.strftime('%d%H%M') + 'pmetrics.csv'
    df.to_csv('process_metrics/'+file_name, encoding='utf-8', index=False)


if __name__ == '__main__':
    main()
