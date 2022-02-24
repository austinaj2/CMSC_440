import socket
import time
import os
import requests
import sys
import datetime
from datetime import datetime
import pprint
import webbrowser
import requests_toolbelt.utils
from requests_toolbelt.utils import dump

new = 2 # open in a new tab, if possible

#### GET ####
def get(validURL):
    # start of hostname
    after = validURL.find('://')+3
    # end of hostname, start of path
    pathStart = int(validURL.find('/', after))
    if validURL[pathStart]=='/':
        host = validURL[after:pathStart]
        path = validURL[pathStart:]
    else:
        host = validURL[after:]
        path = '/'
    port = 80

    # If there is a port given in the URL argument
    if validURL.find(':', after) != -1:
        semi = validURL.find(':', after)
        e = validURL.find('/', semi+1)
        # save port number given, as int
        if validURL[e]=='/':
            port = int(validURL[semi+1:e])
        else:
            port = int(validURL[semi+1:])
        host = host[:host.find(':')]

    # Printing values
    print('\nHost: ', host)
    print('Path: ', path)
    print('Port: ', port, '\n')

    # Connect to host through socket, TCP
    try:
        s.connect((host, port))
    except socket.gaierror:
        print('\n-- Could not resolve the host. --\n')
        sys.exit(2)
    except ConnectionRefusedError:
        print('\n-- Port', port, 'is not open for connection --\n')
        sys.exit(2)
    except OSError:
        print('\n-- The requested address (host+port) is not valid in its context. --\n')
        sys.exit(2)
    headers = {
        'host': host,
        'time': str(datetime.now()),
        'user-agent': 'VCU-CMSC491',
        'user-name': 'Andre'
    }

    # print socket to ensure they match...
    # print('\n', s, '\n')

    # send get request
    request = 'GET '+path+' HTTP/1.0\r\nHost: '+host+'\r\nTime: '+str(datetime.now())+'\r\nUser-Agent: VCU-CMSC491\r\nUser-name: Andre\r\n\r\n'
    s.send(request.encode())
    print('-- GET request --\n')

    # print HTTP request
    print(request)

    # storing response
    try:
        receive = s.recv(10000)
    except:
        print('-- Nothing more to display... Goodbye! --')
        sys.exit(2)
    response = receive.decode()
    
    # define filename to received file
    filename = 'new'

    # split header and data
    headers =  response.split('\r\n\r\n')[0]
    # print(headers)
    try:
        data = response.split('\r\n\r\n')[1]
    except:
        try:
            headers = headers.split('\r\n\r\n')[0]
            data = headers.split('\r\n\r\n')[1]
        except:
            headers = headers.split('\n\n')[0]
            resp = response.find('\n\n')
            data = response[resp+2:]

    # parse header, print necessary fields
    code = 0
    # print response code
    if 'HTTP/' in headers:
        name = headers.find('HTTP/')+9
        end = headers.find(' ', name)
        code = int(headers[name:end])
        print('Response Code:', code)
    # print server type
    if 'Server' in headers:
        name = headers.find('Server:')+8
        end = headers.find('\n', name)
        print('Server:', headers[name:end])
    # if 200-level response given
    if code>=200 and code<300:
        if 'Last-Modified' in headers:
            name = headers.find('Last-Modified:')+15
            end = headers.find('\n', name)
            print('Last-Modified:', headers[name:end])
        # print number of bytes
        cont = len(data)
        print('Content-Length:', cont)
        print('')
        # if there is html data
        if '<' in response:
            with open(filename+'.html', 'wb') as f:
                print('File opened...')
                print('-- receiving data --')
                # write response to file
                f.write(receive)              
                f.close()
                print('File created and closed...\n')
                # in the case a file is retrieve, open it in browser
                webbrowser.open(filename+'.html')
        # if no html data
        else:
            with open(filename, 'wb') as f:
                print('File opened...')
                print('-- receiving data --')
                f.write(receive)
                f.close()
                print('File created and closed...\n')
    # if 300-level response given
    elif code>=300 and code<400:
        if 'Location' in headers:
                name = headers.find('Location:')+10
                end = headers.find('\n', name)
                print('Location:', headers[name:end])
    
    #print response header
    print('')
    print(headers,'\n')
    
    # # print data
    # print('DATA')
    # print(data,'\n')

    s.settimeout(16)
    s.close()

#### PUT ####
def put():
    # make sure there is a 2nd argument, url
    try: 
        url = sys.argv[2]
    except:
        print('\n-- ERR: - arg 2, No argument found. --\n')
        sys.exit(2)

    # make sure there is a 3rd argument, a file is specified for transmission
    try:
        pathfile = sys.argv[3]
    except:
        print('\n-- ERR: - arg 3, Please specify and file to transmit. --\n')
        sys.exit(2)

    # ensuring the first argument is the PUT command
    # if command != 'put' or command[0:7]=='http://' or command[0:8]=='https://' :
    #     print('\n-- ERR: - arg 1, Please enter a valid argument! --\n')
    #     sys.exit(2)
    # ensuring the second argument is a valid url
    if url[0:7]=='http://' or url[0:8]=='https://':
        validURL = url
    else:
        print('\n-- ERR: -arg 2, Please enter a valid URL! --\n(must begin with "http://" or "https://")\n')
        sys.exit(2)
    # ensuring the 3rd argument is valid
    if pathfile.find('.')==-1 | pathfile.find('/')==-1:
        print('\n-- ERR: -arg 3, Please enter a valid filename, or path/filename. --\n')
        sys.exit(2)

    # start of hostname
    after = validURL.find('://')+3
    # end of hostname, start of path
    pathStart = int(validURL.find('/', after))
    if validURL[pathStart]=='/':
        host = validURL[after:pathStart]
    else:
        host = validURL[after:]
    # default port
    port = 10101
    if validURL.find(':', after) != -1:
        semi = validURL.find(':', after)
        e = validURL.find('/', semi+1)
        # save port number given, as int
        if validURL[e]=='/':
            port = int(validURL[semi+1:e])
        else:
            port = int(validURL[semi+1:])
        # trim hostname
        host = host[:host.find(':')]
    last = -1
    for i in range(0, len(pathfile)):
        if pathfile[i]=='/':
            last = i
    if last!=-1:
        filename = pathfile[last+1:]
        path = pathfile[0:last+1]
    else:
        filename = pathfile
        path = '/'

    try:
        filesize = os.path.getsize(filename)
    except FileNotFoundError:
        print('\n-- ERR: -arg 3,  FILE NOT FOUND. --\n')
        sys.exit(2)

    
    # ensure desired file exists
    try:
        f = open(filename)
    except FileNotFoundError:
        print('\n-- ERR: -arg 3,  FILE NOT FOUND. --\n')
        sys.exit(2)

    # Printing values
    print('\nHost: ', host)
    print('Path: ', pathfile)
    print('Port: ', port, '\n')    

    # ensure an argument is given
    try:
        s.connect((host, port))
    except socket.gaierror:
        print('\n-- Could not resolve the host. --\n')
        sys.exit(2)
    except ConnectionRefusedError:
        print('\n-- Port', port, 'is not open for connection --\n')
        sys.exit(2)
    except OSError:
        print('\n-- The requested address (host+port) is not valid in its context. --\n')
        sys.exit(2)
    headers = {
        'host': host,
        'time': str(datetime.now()),
        'user-agent': 'VCU-CMSC491',
        'user-name': 'Andre',
    }

    # send put request
    request = 'PUT /'+filename+' HTTP/1.0\r\nHost: '+host+'\r\nTime: '+str(datetime.now())+'\r\nUser-Agent: VCU-CMSC491\r\nUser-name: Andre\r\n\r\n'
    try:
        s.send(request.encode())
    except requests.exceptions.Timeout as err:
        print(err, '\n') 
    
    print('-- PUT request --\n')
    # print HTTP request
    print(request, '\n')

    # set buffer for reading file
    buffer = 1024
    while filesize>buffer:
        buffer+=1024

    # send the filename and filesize
    s.send((filename+' '+str(filesize)).encode())

    # receive confirmation file data was sent
    # print(s.recv(1024).decode(), '\n')

    # open file and read to server
    with open(filename, 'rb') as f:
        while True:
        # read the bytes from the file
            read = f.read(buffer)
            if not read:
                # file transmitting is done
                break
            s.sendall(read)
    
    # response from server that file was received successfully
    response = s.recv(2048).decode()
    # split header and data
    headers =  response.split('\r\n\r\n')[0]
    # print(headers)
    try:
        data = response.split('\r\n\r\n')[1]
    except:
        try:
            headers = headers.split('\r\n\r\n')[0]
            data = headers.split('\r\n\r\n')[1]
        except:
            headers = headers.split('\n\n')[0]
            resp = response.find('\n\n')
            data = response[resp+2:]

    # print response code
    if 'HTTP/' in headers:
        name = headers.find('HTTP/')+9
        end = headers.find(' ', name)
        code = int(headers[name:end])
        print('Response Code:', code)
    # print server type
    if 'Server' in headers:
        name = headers.find('Server:')+8
        end = headers.find('\n', name)
        print('Server:', headers[name:end])
    print('')
    print(headers, '\n')

    # # storing response
    # try: 
    #     receive = s.recv(10000)
    #     response = receive.decode()
    # except:
    #     print('No response from the server')
    #     sys.exit(2)
    # print(response)
    # print socket to ensure they match...
    # t=time.time()
    # try:
    #     r = requests.put(validURL, data=open(filename, 'rb'), headers=headers)
    # except requests.exceptions.Timeout as err:
    #     print(err, '\n') 
    #     sys.exit(2) 
    # data = dump.dump_all(r)
    # print('\n-- PUT request: --\n')
    # print(data.decode('utf-8'), '\n')
    # print('Response Code:', r)
    # if 'server' in r.headers:
    #     print('Server:', r.headers['server'], '\n')
    # # print HTTP response header
    # print('Response header:\n', r.headers, '\n')
    s.settimeout(16)
    s.close()

# ensure an argument is given
try:
    arg = sys.argv[1]
except:
    print('\n-- ERR: - arg 1, No argument found. --\n')
    sys.exit(2)
# creating a socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('-- Socket created, successfully. --')
except:
    print('-- Failed to create socket. --')

if len(sys.argv)>3:
    print('\n-- ERR: - arg x, Too many arguments! --\n(must begin with \'http://\', \'https://\', or a PUT command)\n')
    sys.exit(2)
#validate first argument given
# if it's a url...
if arg[0:7]=='http://' or arg[0:8]=='https://':
    validURL = arg
    get(validURL)
# if it's a PUT command
elif arg.lower()=='put':
    put()

# anything else
else:
    print('\n-- ERR: - arg 1, Please enter a valid argument! --\n(must begin with \'http://\', \'https://\', or a PUT command)\n')
    sys.exit(2)

