import argparse
import ipaddress
from server import socket_connection
from client import client_connection

#jeg har i stor grad forklart hva de enkelte funksjonen gjør og hva gjør de parameterene i raporten

def checkport(port): # denne funksjon brukes for å sjekke gyldig portnummer, funksjon kalles via args-argumente 
    try:
        port = int(port) #konvertere port til heltal 
        if port<1024:
            print(f'you insert an invalid port number: {port}')
        elif port > 65535:
            raise ValueError#kastes en untakk ved uyildig port nummer
    except ValueError:
            raise argparse.ArgumentTypeError(f'you insert an invalid port number: {port}') #kastes en untakk ved uyildig port nummer
    return port #returenes port nummeret hvis det var gyldig

def check_positive(time): #når denne funksjon kalles sjekkes om tallet er possitiv, funksjon kalles via args-argumente
    try:
        time = int(time)
        if not time > 0:
            raise ValueError(f'The time you entered is not valid: {time}. Choose a positive integer.')
    except ValueError:
        raise argparse.ArgumentTypeError(f'The time you entered is not valid: {time}. Choose a positive integer.')
    return time #returener tallet hvis det er gldig

def check_ip(ip): #sjekker om gyldig ip adress
    try:
        val = ipaddress.ip_address(ip)
    except ValueError:
        raise argparse.ArgumentTypeError(f'{ip} is not valid Ip adress')
    return ip

def main(): #dette er hoved funksjon som kjørs når vi skriver simpleperf.py .....

    parser = argparse.ArgumentParser(description="simpleperf") #tror ikke trenger å beskrive hver enkelt av de argumentene, har nevnt de i raporten også
    parser.add_argument('-s', '--server',        action='store_true',                                                        help='connect to the server')
    parser.add_argument('-b', '--bind',          type = check_ip,                     default="127.0.0.1",                   help='The IP address')
    parser.add_argument('-f', '--format',        type=str, default='MB',              choices=['BYTES','KB', 'MB', 'GB'],    help='choose the format of data')
    parser.add_argument('-c', '--client',        action='store_true',                                                        help='the client side')
    parser.add_argument('-I','--server_ip',      type=check_ip ,                      default='127.0.0.1',                   help='IP address of the simpleperf server')
    parser.add_argument('-p','--port',           type=checkport,                      default=8088,                          help='Server port to connect to')
    parser.add_argument('-t','--time',           type=check_positive,                 default=25,                            help='time of sending data to the server')
    parser.add_argument('-i','--interval',       type=check_positive,                 default=None,                          help='interval of data transfering')
    parser.add_argument('-n','--num',            type=str,                            default=None,                          help='transfer number of bytes')
    parser.add_argument('-P','--parallel',       type=int, choices=range(1, 6),       default=None,                          help='create parallel connection, yu can choose from 1 to 5 intervals')
   
    args = parser.parse_args()

    if args.server and args.client: #denne gir oss ikke mulighet til å bruke -s og -c flagget sammen
        print('Error: you must run in server mode or client mode.')
        exit()
    elif args.server: #kjøres hvis vi bruker -s flaget og kaller en funksjon som er under
        socket_connection(args.bind, args.port, args) # bind lager socket ip og args.port lager en sockt port for å tilkobling og args parameteren tar argumenter som kommer fra kommando
    elif args.client: # hvis vi bruker -c falgget
        client_connection(args.server_ip, args.port, args) # samme her
    else:
        print('Error: you must run in server mode or client mode.')
        exit() # hvis ingen av flagget blir brukt får vi feil meldign og avslutter 


if __name__ == '__main__':
    main()
