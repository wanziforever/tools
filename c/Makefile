# simple Makefie for tools compile
PLATFORM = LINUX
CXX = g++
CC = gcc

TARGET  = write_test
build_root=$(shell pwd)
INCLUDE_DIR = -I.
LIB_DIR = -L.
LIBS    = -lpthread
# the source code list, add file name below for new source
SRC = \
	log.c \
	write_test.c

OBJ = $(addsuffix .o, $(basename $(SRC)))
# also can use
# OBJ = $(subst .cc, .o, $(SRC))

build_bin = $(build_root)

#
all: $(build_bin)/$(TARGET)
#
# compile the main function
$(OBJ):%o:%c
	$(CC) $(INCLUDE_DIR) -c $< -o $@

$(build_bin)/$(TARGET): $(OBJ)
	@echo "build binary..."
	$(CC) $^ -o $@ $(LIB_DIR) $(LIBS)

clean:
	rm -rf *.o
