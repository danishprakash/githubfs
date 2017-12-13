#!/usr/bin/env python3

import os
import sys
import errno
import getpass
import pwd

from stat import S_IFDIR, S_IFLNK, S_IFREG, S_ISREG
from github import Github
from fuse import FUSE, FuseOSError, Operations
from time import time, mktime, sleep

class gfs(Operations):
    def __init__(self, root):
        print('[init]: ', root)
        self.root = root
        self.user = Github(input("Username: "), getpass.getpass("Password: "))
        print('[init]: Establishing connection....')
        self.repo_list = []
        print('[init]: Fetching repositories...')
        self.file_content_decoded = dict()
        self.file_content_bytes = dict()
        for repo in self.user.get_user().get_repos():
            self.repo_list.append(repo.name)
            files = repo.get_dir_contents('/')
            for file_ in files:
                if file_.name == repo.name:
                    continue
                elif '.' in file_.name and not(file_.name.startswith('.')):
                    # print(repo.name, file_.name)
                    file_name = file_.name
                    file_content = repo.get_file_contents(file_name)
                    # print(file_content.decoded_content)
                    self.file_content_bytes[file_.name] = file_content.decoded_content
                    self.file_content_decoded[file_.name] = file_content.decoded_content.decode('utf-8')
        print('Done')

    # def get_file_contents(self, repo_name, file_name, flag):
    #     for repo in self.user.get_user().get_repos():
    #         if repo.name == repo_name:
    #             files = repo.get_dir_contents('/')
    #             for file_ in files:
    #                 if file_name == file_.name:
    #                     file_content = repo.get_file_contents(file_name).decoded_content
    #                     print(file_content)
    #                     if flag == 0:
    #                         return file_content.decode('utf-8')
    #                     else:
    #                         return file_content

    def open(self, path, flags):
        if path == '/' or path == '/repos':
            pass
        else:
            path_ele = path.split('/')
            file_name = path_ele[-1]
            repo_name = path_ele[-2]
            new_file = open(file_name, "w")
            data = self.file_content_decoded[file_name]
            new_file.write(data)
            new_file.close
            # print(len(data))
            return len(data)

            


    def getattr(self, path, fh=None):
        print('[getattr]: ', path)
        full_path = self.root + path
        properties = dict(
                st_mode = S_IFDIR | 755,
                st_nlink = 2,
                st_ctime=0,
                st_mtime=0,
                st_atime=0,
                st_uid=pwd.getpwuid(os.getuid()).pw_uid,
                st_gid=pwd.getpwuid(os.getuid()).pw_gid,
                )
        # print(path)
        path_ele = path.split('/')
        # print(path_ele[-1])
        if path == '/' or path_ele[-1].startswith('.'):
            pass
        elif path == '/repos' or path_ele[-1] in self.repo_list:
            pass
        else:
            path_ele = path.split('/')
            file_name = path_ele[-1]
            repo_name = path_ele[-2]
            file_size = 4096
            if file_name not in self.file_content_decoded.keys():
                pass
            else:
                if '.' in file_name and not(file_name.startswith('.')):
                    file_size = len(self.file_content_decoded[file_name])
                properties = dict(
                        st_mode=S_IFREG | 644,
                        st_size=file_size,
                        st_nlink=1,
                        )
        return properties

    # def open(self, path, flags):
    #       print('[open]')
    #       return 0

    def read(self, path, size, offset, fh=None):
        print('[read]: ', path)
        file_content = ''
        path_ele = path.split('/')
        if path == '/' or path == '/repos':
            pass
        else:
            path = path.split('/')
            repo_name = path[-2]
            file_name = path[-1]
            # print(repo_name, file_name)
            return self.file_content_bytes[file_name]


    def readdir(self, path, fh):
        print('[readdir]: ', path)
        full_path = self.root + path
        repo_list = ['.', '..']
        path_ele = path.split('/')
        if path.startswith('.'):
            pass
        elif path == '/':
            return ['.', '..', 'repos']
        elif path == '/repos':
            return repo_list + self.repo_list
        elif path_ele[-1] in self.repo_list:
            repo_name = path_ele[-1]
            # print(repo_name)
            for item in self.user.get_user().get_repos():
                if item.name == repo_name:
                    files = item.get_dir_contents('/')
                    break
            for item in files:
                repo_list.append(item.name)
            # print(repo_list)
            return repo_list

def main(mountpoint, root):
    FUSE(gfs(root), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])


