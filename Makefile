COMPILER = gcc
FILESYSTEM_FILES = sfs.c

build: $(FILESYSTEM_FILES)
	$(COMPILER) $(FILESYSTEM_FILES) -o sfs `pkg-config fuse --cflags --libs`
	echo 'To Mount: ./sfs -f [mount point]'

clean:
	rm sfs
