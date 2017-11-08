#define FUSE_USE_VERSION 30

#include <fuse.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>

static int s_getattr(const char *path, struct stat *st)
{
	st->st_uid = getuid();
	st->st_gid = getgid();
	st->st_atime = time(NULL);
	st->st_mtime = time(NULL);

	if(strcmp(path, "/") == 0 )
	{
		st->st_mode = S_IFDIR | 0755;
		st->st_nlink = 2;
	}
	else
	{
		st->st_mode = S_IFREG | 0644;
		st->st_nlink = 1;
		st->st_size = 1024;
	}
	return 0;
}

static int s_readdir( const char *path, void *buffer, fuse_fill_dir_t filler, off_t offset, struct fuse_file_info  *fi )
{
	filler( buffer, ".", NULL, 0 );
	filler( buffer, "..", NULL, 0 );

	return 0;
}

static struct fuse_operations operations = {
	.getattr = s_getattr,
	.readdir = s_readdir,
};

int main( int argc, char *argv[] )
{
	return fuse_main( argc, argv, &operations, NULL);
}

