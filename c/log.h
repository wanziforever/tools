// Log print util for tools development use
// Author wangliang8@hisense.com
//
// provide well formated log print functionality, including
// the timestamp, source file name, and the line number of
// the caller in source file.
// Note: NO MULTI-THREAD CONSIDERATION CURRENTLY
//
// usage: debug("debuglog printing %s", variable)

#ifndef TOOL_LOG_H__
#define TOOL_LOG_H__

#define false -1
#define true 0

#define debug (log4c(__FILE__, __LINE__))

typedef void (*MYLOG)(char const*, ...);

MYLOG log4c(char *fname, int lnum);

#endif
