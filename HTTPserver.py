import socket
import sys
import os

# read in, handle command line arguments
try:
    port = sys.argv[1]
except:
    print('\n-- ERR: - arg 1, No argument found. --\n(Enter a port for connection)\n')
    sys.exit(2)
if int(port) < 0 or int(port) > 65536:
    print('\n-- ERR: - arg 1, Please enter a valid port. --\n(only ports 10000-11000 are open for use!) --\n')
    sys.exit(2)
# define port and host
validPort = int(port)
host = ''

# create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, validPort))
sock.listen(1)
print('Socket: listening on port', validPort, '...\n')

while True:
    try:
        # wait for connection
        c, addr = sock.accept()
        print("CONNECTION FROM:", str(addr), '\n')

        # initial request
        init_req = c.recv(1024).decode()

        if init_req[0:3]=='PUT':
            print('-- PUT request --\n')
            # print IP:port:request
            ip_addr = socket.gethostbyname(socket.gethostname())
            print(ip_addr+':'+port+':'+init_req[0:3])

            # print request
            print('\n', init_req, '\n')

            recv_sz = 0

            # incoming file information
            file_data = c.recv(1024)
            data_resp = file_data.decode()

            # parse incoming file data
            filename = data_resp.split(' ')[0]
            one = data_resp.find(' ')
            two = data_resp.find('HTTP/')
            i = data_resp[one:two]

            # base buffer
            recv_sz = int(i)
        
            # create reasonable buffer for file based on received file size
            buffer = 1024
            while recv_sz>buffer:
                buffer+=1024

            # send response (for file data)
            # c.send(('Thank you for the information, retreiving file now...').encode())

            # receive incoming file
            data = c.recv(buffer)
            with open(os.path.join('', filename.split('.')[0]+'[recv].html'), 'wb') as f:
                    f.write(data)
            try:
                new_f = open(filename.split('.')[0]+'[recv].html')
            except FileNotFoundError:
                print('\n-- 606 FAILED File NOT Created --\n')
                c.send(('\n-- 606 FAILED File NOT Created --\n').encode())
                sys.exit(2)
            # except KeyboardInterrupt:
            #     c.close()
            #     sock.close()
            #     yes = False
            #     sys.exit(2)
            #     break
            # send response to client, confirming successful file transfer
            if os.path.getsize(filename.split('.')[0]+'[recv].html')<=0:
                c.send(('\n-- 606 FAILED File NOT Created --\n').encode())
            else:
                c.send(('\n-- 200 OK File Created --\n').encode())
            f.close()


        if init_req[0:3]=='GET':
            print('-- GET request --\n')
            # print IP:port:request
            ip_addr = socket.gethostbyname(socket.gethostname())
            print(ip_addr+':'+port+':'+init_req[0:3])

            # print request
            print('\n', init_req, '\n')

            # parsing request for path
            req_line = init_req.split('\n')[0]
            path = req_line.split(' ')[1]

            # ensure desired file exists
            try:
                f = open(path[1:])
            except FileNotFoundError:
                if path=='/':
                    print('-- Please specify the desired file --')
                    c.send(('-- Please specify the desired file --').encode())
                    break
                    sys.exit(2)
                else:
                    print('\n-- ERR: -arg 1,  404 File Not Found --\n')
                    c.send(('\n-- ERR: -arg 1,  404 File Not Found --\n').encode())
                    sys.exit(2)
            with open(path[1:], 'rb') as f:
                while True:
                # read the bytes from the file
                    read = f.read(os.path.getsize(path[1:]))
                    if not read:
                        # file transmitting is done
                        break
                    c.sendall(read)
    except KeyboardInterrupt:
        try:
            c.close()
            sock.close()
            print('-- Process halted by user... --')
            False
            break
        except:
            c.close()
            print('-- Process halted by user... --')
            sys.exit(2)
            break
sock.close()