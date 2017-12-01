#!/usr/bin/env python3

import os
import sys
import errno

from github import Github
from fuse import FUSE, FuseOSError, Operations

class lfs(Operations):
	def __init__(self, root):
		#		self.user = Github(input("Username: "), input("Password: "))
		self.user = Github('prakashdanish', 'L34rnJ4v4')

	def getattr(self, path, fh=None):
		if path == '/':
			pass
		else:
			raise fuse.FuseOSError(errno.ENOENT)

	def readdir(self, path, fh):
		repo_list = []
		print('[readdir]')
		for repo in self.user.get_user().get_repos():
			print(repo.name)
			repo_list = repo_list + [repo.name]
		return repo_list

def main(mountpoint, root):
	FUSE(lfs(root), mountpoint, nothreads=True, foreground=True)

if __name__ == '__main__':
	main(sys.argv[2], sys.argv[1])


