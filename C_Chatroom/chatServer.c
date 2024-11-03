#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <sys/types.h>
#include <string.h>
#include <netdb.h>

#define SERVER_PORT "5432"
#define MAX_LINE 256
#define MAX_PENDING 5

/*
 * Create, bind and passive open a socket on a local interface for the provided service.
 * Argument matches the second argument to getaddrinfo(3).
 *
 * Returns a passively opened socket or -1 on error. Caller is responsible for calling
 * accept and closing the socket.
 */
int bind_and_listen( const char *service );

/*
 * Return the maximum socket descriptor set in the argument.
 * This is a helper function that might be useful to you.
 */
int find_max_fd(const fd_set *fs);

int main(void){
	// all_sockets stores all active sockets. Any socket connected to the server should
	// be included in the set. A socket that disconnects should be removed from the set.
	// The server's main socket should always remain in the set.
	fd_set all_sockets;
	FD_ZERO(&all_sockets);

	// call_set is a temporary used for each select call. Sockets will get removed from
	// the set by select to indicate each socket's availability.
	fd_set call_set;
	FD_ZERO(&call_set);

	// listen_socket is the fd on which the program can accept() new connections
	int listen_socket = bind_and_listen(SERVER_PORT);
	FD_SET(listen_socket, &all_sockets);

	// max_socket should always contain the socket fd with the largest value, just one
	// for now.
	int max_socket = listen_socket;

	while(1) {
		// Initializing necessary fd_sets
		call_set = all_sockets;

		// Calculating the number of sockets using SELECT
		int num_s = select(max_socket+1, &call_set, NULL, NULL, NULL);

		// Error checking
		if( num_s < 0 ){
			perror("ERROR in select() call");
			return -1;
		}
		
		// Check each potential socket.
		// Skip standard IN/OUT/ERROR -> start at 3.
		for( int s = 3; s <= max_socket; ++s ){
			// Skip sockets that aren't ready
			if( !FD_ISSET(s, &call_set) )
				continue;

			// A new connection is ready
			if(s == listen_socket){
			 	// Creating and initializing a new socket
				int newSocket = accept(s, NULL, NULL);

				// Error Checking for the new connected socket
				if (newSocket < 0) {
					perror("Error in accepting Socket");
					close(s);
					exit(1);
				} else {
					// Adding the new connected socket to all_sockets file descriptor
					FD_SET(newSocket, &all_sockets);

					// Printing that a new socket with its number has connected
					printf("Socket %d connected\n", newSocket);

					// Changing the max_socket if the new one is greater than it
					// Ask professor about this
					max_socket = find_max_fd(&all_sockets);
					printf("Max Socket: Socket #%d\n", max_socket);
				}
 			}
			// A connected socket is ready
			else {
				// Creating buffer and input for client input
				char clientInput[MAX_LINE];

				// Receiving data from the already connected client
				// and printing what they enter into terminal
				if (recv(s, clientInput, MAX_LINE, 0) > 0) {
					printf("Socket %d sent: %s", s, clientInput);
				} else {
					// Nothing is sent so assuming client closed its connection
					// Printing that the socket closed
					printf("Socket %d closed\n", s);

					// Closing the socket
					close(s);

					// Removing the socket from the all_sockets file descriptor
					FD_CLR(s, &all_sockets);

					// Updating the new max socket
					max_socket = find_max_fd(&all_sockets);
					printf("Max Socket: Socket #%d\n", max_socket);
				}
			}
		}
	}
}

int find_max_fd(const fd_set *fs) {
	int ret = 0;
	for(int i = FD_SETSIZE-1; i>=0 && ret==0; --i){
		if( FD_ISSET(i, fs) ){
			ret = i;
		}
	}
	return ret;
}

int bind_and_listen( const char *service ) {
	struct addrinfo hints;
	struct addrinfo *rp, *result;
	int s;

	/* Build address data structure */
	memset( &hints, 0, sizeof( struct addrinfo ) );
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = AI_PASSIVE;
	hints.ai_protocol = 0;

	/* Get local address info */
	if ( ( s = getaddrinfo( NULL, service, &hints, &result ) ) != 0 ) {
		fprintf( stderr, "stream-talk-server: getaddrinfo: %s\n", gai_strerror( s ) );
		return -1;
	}

	/* Iterate through the address list and try to perform passive open */
	for ( rp = result; rp != NULL; rp = rp->ai_next ) {
		if ( ( s = socket( rp->ai_family, rp->ai_socktype, rp->ai_protocol ) ) == -1 ) {
			continue;
		}

		if ( !bind( s, rp->ai_addr, rp->ai_addrlen ) ) {
			break;
		}

		close( s );
	}
	if ( rp == NULL ) {
		perror( "stream-talk-server: bind" );
		return -1;
	}
	if ( listen( s, MAX_PENDING ) == -1 ) {
		perror( "stream-talk-server: listen" );
		close( s );
		return -1;
	}
	freeaddrinfo( result );

	return s;
}
