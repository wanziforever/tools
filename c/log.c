// Log print util for tools development use
// Author wangliang8@hisense.com
//
// provide well formated log print functionality, including
// the timestamp, source file name, and the line number of
// the caller in source file.
// Note: NO MULTI-THREAD CONSIDERATION CURRENTLY
//
/// usage: debug("debuglog printing %s", variable)

#include <stdio.h>
#include <time.h>
#include <stdarg.h>
#include <string.h>
#include "log.h"

// for log the source file name and line number
static char g_source_file_name[128] = {0};
static int g_source_line_num = 0;

void getCurrentTime(char *timeb)
{
  long lt = time(0);
  struct tm *at = localtime((const long*) &lt);
  int yr = at->tm_year + 1900;
  sprintf(timeb, "%04d-%02d-%02d %02d:%02d:%02d",
          yr, at->tm_mon+1, at->tm_mday, at->tm_hour,
          at->tm_min, at->tm_sec);
  return;
}

// remove the new line suffix
void remove_new_line(char *msg)
{
  int len = strlen(msg);
  int pos = len - 1;
  while(msg[pos] == '\n') {
    msg[pos] = 0;
  }
  return;
}

#define ADD_LOG_PREFIX_STRING(buf)              \
  strcpy(buf, "+++ ");

#define ADD_LOG_SUFFIX_STRING(buf)              \
  strcat(buf, "\nEND OF REPORT +++ ");

#define ADD_LOG_TIMESTAMP_STRING(buf)           \
  char timestamp[64];                           \
  getCurrentTime(timestamp);                    \
  strcat(buf, timestamp);

#define ADD_LOG_SOURCE_INFO_STRING(buf)              \
  char source_info[128];                             \
  sprintf(source_info," FileName: %s, LineNum: %d",  \
          g_source_file_name, g_source_line_num);    \
  strcat(buf, source_info);                          \
  strcat(buf, "\n");

#define ADD_LOG_BODY_STRING(buf, body)          \
  remove_new_line(body);                        \
  strcat(buf, body);

#define LOG_SEPARATOR "\n^A\n\n"

// control which media the log will print
void my_message(char *msg)
{
  char buf[512];
  ADD_LOG_PREFIX_STRING(buf);
  ADD_LOG_TIMESTAMP_STRING(buf);
  ADD_LOG_SOURCE_INFO_STRING(buf);
  ADD_LOG_BODY_STRING(buf, msg);
  ADD_LOG_SUFFIX_STRING(buf);
  // can change to other write function
  printf("%s%s", buf, LOG_SEPARATOR);
}

// main interface for print log
void mylog(char const *fmt, ...)
{
  va_list args;
  va_start(args, fmt);
  char log_buf[256];
  vsnprintf(log_buf, 256, fmt, args);
  my_message(log_buf);
}

// main job is to get the source file and line number
// information,and set it to global variable for log
// print function use, finally return the real log
// print menthod, #define this function to with __FILE__
// and __LINE__ marco when using it in code
MYLOG log4c(char *fname, int lnum)
{
  strcpy(g_source_file_name, fname);
  g_source_line_num = lnum;
  return mylog;
}
