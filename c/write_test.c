#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include "log.h"

const int MAX_FILE_ERROR_RETRY_TIME = 2000;
const int WRITE_INTERVAL = 1; // second
// content which is used to disk
char content[] =
  "wangliangwangliangwangliangwangliangwangliangwangliangwang"
  "wangliangwangliangwangliangwangliangwangliangwangliangwang";

void usage()
{
  printf("write_test <file_path>\n");
}

int main(int argc, char *argv[])
{
  int test_fd = 0;
  if (argc != 2) {
    usage();
    return false;
  }

  test_fd = open(argv[1],  O_RDWR|O_CREAT, S_IRUSR|S_IWUSR);
  if (!test_fd) {
    mylog("Fail to open file %s\n",argv[1]);
    return false;
  }
    
  int len = 0;
  int retry = 0;
  // write content to file, and sleep 1 second in the middle
  // of every write, 3 times retry for write fail case.
  do {
    lseek64(test_fd, 0, SEEK_END);
    debug("succeed to lseek file\n");
    if ((len = write(test_fd, content, sizeof(content))) !=
        sizeof(content)) {
      retry += 1;
      debug("Fail to write file to disk for try 1\n");
    }
    debug("succeed to write data to disk\n");
    retry = 0;
    sleep(WRITE_INTERVAL);
  } while(retry < MAX_FILE_ERROR_RETRY_TIME);
  close(test_fd);
  debug("program exit\n");
}

