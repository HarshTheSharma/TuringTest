EXE = chatServer
CFLAGS = -Wall
CXXFLAGS = -Wall
LDLIBS =
CC = gcc
CXX = g++

.PHONY: all
all: $(EXE)

# Implicit rules defined by Make, but you can redefine if needed
chatServer: chatServer.c
	$(CC) $(CFLAGS) chatServer.c $(LDLIBS) -o chatServer

.PHONY: clean
clean:
	rm -f $(EXE)
