import re
from git import Repo
import time



# This is where you should modify

# PROJECT = 'spring-framework'
# VERSION = 'v5.1.0.RELEASE..'

# PROJECT = 'esp-idf'
# VERSION = 'v3.0..'

# PROJECT = 'neovim'
# VERSION = 'v0.2.0..'

# PROJECT = 'freeswitch'
# VERSION = 'v1.5.0..'

# PROJECT = 'openssl'
# VERSION = 'OpenSSL_1_1_0..'

# PROJECT = 'mpv'
# VERSION = 'v0.3.0..'

# PROJECT = 'freeradius-server'
# VERSION = 'release_3_0_0..'

# PROJECT = 'git'
# VERSION = 'v2.11.0..'

# PROJECT = 'spring-boot'
# VERSION = 'v1.4.0.RELEASE..'

# PROJECT = 'freeswitch'
# VERSION = 'v1.8.0..'

# ==============================================================================
# 0: java 1: c
LAN = 0
# ==============================================================================
PATH = 'dataset/raw_project/'+PROJECT
FILE = PROJECT+'_'+VERSION+'_bug'+time.strftime('%d%H%M')

# pattern for defect commit extraction
# PAT_BUG = '\s(?!de)bug|\s(?!pre)fix|issue|error|crash|problem|fail|defect|patch|not\s|can\'t|doesn\'t'
PAT_BUG = '\s(?!de)bug|\s(?!pre)fix|issue|error|crash|problem|fail|defect|patch|incorrect'
# pattern for matching commit bound
PAT_BEGIN = 'commit-begin-762-project'
PAT_END = 'commit-end-762-project'

# pattern for defect file extraction
PAT_LAN = ['.+\.java', '.+\.c$']
PAT_JAVA = '\s.+\.java'


def get_one_line_commits():
    repo = Repo(PATH)
    g = repo.git
    diff_arg = '--name-only'
    commit_format = '--pretty=format:'+PAT_BEGIN+'%n%B%n'+PAT_END
    # one_line_commits = g.log(VERSION, diff_arg, commit_format, '--all', '--reverse').split('\n')
    # one_line_commits = g.log(VERSION, diff_arg, commit_format, '--all', '--full-history', '--reverse').split('\n')
    one_line_commits = g.log(VERSION, diff_arg, commit_format, '--full-history', '--sparse', '--reverse').split('\n')
    return one_line_commits


# # check modified files
# def get_files_dict(one_line_commits):
#     files_dict = {}
#     pre_begin = False
#     pre_end = False
#     bug = False
#     # check each line of commits. 4 Possible lines: begin, end, commit, and files revised
#     cur_commit = ''
#     for line in one_line_commits:
#         if line == PAT_BEGIN:
#             pre_begin = True
#             pre_end = False
#             cur_commit = ''
#             continue
#         if line == PAT_END:
#             pre_end = True
#             pre_begin = False
#             continue
#         # commits
#         if pre_begin:
#             cur_commit += line
#             continue
#             # if re.search(PAT_BUG, line):
#             #     bug = True
#             # else:
#             #     bug = False
#             # continue
#         # files revised
#         if pre_end:
#             if re.search(PAT_BUG, cur_commit):
#                 print('BUG commit: '+cur_commit)
#                 bug = True
#             else:
#                 bug = False
#             if files_dict.get(line) is not None:
#                 continue
#             if re.match(PAT_LAN[LAN], line):
#                 files_dict[line] = bug
#                 if bug:
#                     print('Bug File:'+line)
#     return files_dict

# # not check duplicated
# def get_files_dict(one_line_commits):
#     files_dict = {}
#     pre_begin = False
#     pre_end = False
#     bug = False
#     # check each line of commits. 4 Possible lines: begin, end, commit, and files revised
#     cur_commit = ''
#     for line in one_line_commits:
#         if line == PAT_BEGIN:
#             pre_begin = True
#             pre_end = False
#             cur_commit = ''
#             continue
#         if line == PAT_END:
#             pre_end = True
#             pre_begin = False
#             continue
#         # commits
#         if pre_begin:
#             cur_commit += line
#             continue
#             # if re.search(PAT_BUG, line):
#             #     bug = True
#             # else:
#             #     bug = False
#             # continue
#         # files revised
#         if pre_end:
#             if re.search(PAT_BUG, cur_commit):
#                 print('BUG commit: '+cur_commit)
#                 bug = True
#             else:
#                 bug = False
#             if re.match(PAT_LAN[LAN], line):
#                 files_dict[line] = bug
#                 if bug:
#                     print('Bug File:'+line)
#     return files_dict

def get_def_files(files_dict):
    return [file for file in files_dict if files_dict[file] is True]


def write2log(texts):
    with open('log', 'w') as f:
        for text in texts:
            f.write(text+'\n')


def write_list2file(texts, path):
    with open(path, 'w') as f:
        for text in texts:
            f.write(text+'\n')


def main():
    one_line_commits = get_one_line_commits()
    # write_list2file(one_line_commits, 'log')
    files_dict = get_files_dict(one_line_commits)
    def_files = get_def_files(files_dict)
    write_list2file(def_files, 'defects/'+FILE)
    # print(bug_files)
    # with open('maven_bugs3.0-3.1.0', 'w') as f:
    #     for file in bug_files:
    #         f.write(file+'\n')


if __name__ == '__main__':
    main()





