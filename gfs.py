#!/usr/bin/env python3

import os
import sys
import errno
import pwd


from stat import S_IFDIR, S_IFLNK, S_IFREG, S_ISREG
from github import Github
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from time import time, mktime, sleep

class lfs(Operations, LoggingMixIn):
	def __init__(self, root):
		self.root = root
		#		self.user = Github(input("Username: "), input("Password: "))
		self.user = Github('prakashdanish', 'L34rnJ4v4')
		self.repo_list = []
		for repo in self.user.get_user().get_repos():
			self.repo_list.append(repo.name)

	def getattr(self, path, fh=None):
		#print('[getattr]')
		full_path = self.root + path
		#print(path)
		#print('[getattr]')
		if path == '/repos' or path == '/':
			st = os.lstat(full_path)
			return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
				'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
		elif not('.' in path):
			print('in there')
			properties = dict(
					st_mode=S_IFDIR | 755,
					st_size=4096,
					st_ctime=int(time()),
					st_mtime=int(time()),
					st_atime=int(time()),
					st_uid=pwd.getpwuid(os.getuid()).pw_uid,
					st_gid=pwd.getpwuid(os.getuid()).pw_gid,
					st_nlink=0
					)
			return properties
		else:
			print('in here')
			properties = dict(
					st_mode=S_IFREG | 755,
					st_ctime=int(time()),
					st_mtime=int(time()),
					st_atime=int(time()),
					st_uid=pwd.getpwuid(os.getuid()).pw_uid,
					st_gid=pwd.getpwuid(os.getuid()).pw_gid,
					st_nlink=0,
					)
			return properties
	
#	def open(self, path, flags):
#		print('[open]')
#		return 0

	def read(self, path, size, offset, fh=None):
		file_content = ''
		path_ele = path.split('/')
		print('***[read]')
		print(path)
		if path.endswith('/') or path[1] == '.':
			print('ok')
			return file_content
		else:
			path = path.split('/')
			repo_name = path[-2]
			file_name = path[-1]
			print(repo_name, file_name)
			for item in self.user.get_user().get_repos():
				if item.name == repo_name:
					files = item.get_dir_contents('/')
					for file_ in files:
						if file_name == file_.name:
							file_content = item.get_file_contents(file_name).decoded_content
							print(len(file_content.decode('utf-8')))
							print(type(file_content.decode('utf-8')))
							return file_content






	def readdir(self, path, fh):
		full_path = self.root + path
		#print(full_path)
		repo_list = ['.', '..']
		#if os.path.isdir(full_path):
		#	dirents.extend(os.listdir(full_path))
		#for r in dirents:
		#	yield r
		print('[readdir]')
		
		if path == '/':
			repo_list = ['.', '..', 'repos']
		elif path == '/repos':
			#print(self.repo_list)
			repo_list = repo_list + self.repo_list
		else:
			path = path.split('/')
			repo_name = path[-1]
			for item in self.user.get_user().get_repos():
				if item.name == repo_name:
					files = item.get_dir_contents('/')
					break
			for item in files:
				repo_list.append(item.name)
			#print(repo_list)
		for item in repo_list:
			yield item

def main(mountpoint, root):
	FUSE(lfs(root), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
	main(sys.argv[2], sys.argv[1])


