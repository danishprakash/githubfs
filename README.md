# Github File System [GithubFS] 
A read-only virtual file system for Github using FUSE written in Python.

## Features
- List repos as directories
- List repo contents as directory contents
- Read files in a repo as files in a directory
- Copy files from a repo

## Installation & Usage
Make sure you have both the dependencies installed on your system before using this.

```bash
$ git clone https://github.com/prakashdanish/githubfs

$ cd githubfs

$ python3 gfs.py [root] [mount-point]
```

## Dependencies
- [fusepy](https://github.com/terencehonles/fusepy)
- [PyGithub](https://github.com/PyGithub/PyGithub)

## To-Do
- [x] List repositories as dirs
- [x] List repository contents as dir contents
- [x] Read file contents from a file in a repository
- [ ] Edit and commit changes from the filesystem
- [ ] Multiple account support
- [ ] Config file for storing & accessing credentials
