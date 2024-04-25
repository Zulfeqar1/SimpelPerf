import socket
import time
import threading

#ved hjlep av denne funksjon vil server lage en socket forbindelse med bestemt port og ip. 
#ved hjelp av bind kobles server siden til denne TCP socket 
#ved hjelp av listen lytte eller venter på klient 
def socket_connection(bind, port, args):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #oppretes TCP tilokbling her
    s.bind((bind, port))
    s.listen()
    print(f'-----------------------------------------------------')
    print('A simpleperf server is listening on port ',args.port)
    print(f'-----------------------------------------------------')
    data_size = 1000
    
    while True: #vile kjøres hele tiden til det kommer noe intrup fra tastatur
        clientsocket, address = s.accept() #aksepterer klienten som tilkobles 
        threading.Thread(target=handle_cleint, args=(clientsocket, address, data_size, args.format.upper(), args)).start() #starter tråde
        #som i klinet siden, denne vil lage ny tråden og kalles på handle_cleint. jeg har forklart dette i klient siden


#denne funksjon vil håndtere klient tilkoblingene som tar 5 parametere, jeg har beskrevet dette funskon godt i raporten min også
# clientsocket håndterer klienten som blir tilkobles til server
#adress tar inn ip og port nummeret til klient
#data_size mengden av data som skal mottas om gangen og jeg vet at det er 1000 bytes 
#format hvilket data typen 
#args argumenter som kommer fra kommando linjen
def handle_cleint(clientsocket, address, data_size, format, args):
    print(f'A simpleperf client with {address[0]}:{address[1]} is connect with {args.bind}:{args.port}')
    start_time = time.time()
    total_bytes = 0

    while True: #er altid på og mottar data fra klient så lenge det er data
        data = clientsocket.recv(data_size)
        if len(data) <= 0:
          break
        
        if  "good bye" in data.decode("utf-8"): # sender tilbake en respons til kleint etter recievd by melding, her først mottar data
            clientsocket.sendall(bytes("Good bye!", "utf-8"))
            break #stopper tilkoblingen
        

        total_bytes += len(data)

    time_elapsed = time.time() - start_time #total tiden som ble brukt for opperaajosn 
    clientsocket.close()

    #dette har jeg forklart godt på klient siden
    total_bytes_per_sec = total_bytes
    units = {'BYTES': 1, 'KB': 1000, 'MB': 1000000, 'GB': 1000000000}
    factor = units[format.upper()]

    #bregner båndbredde her
    total_bytes_per_sec = total_bytes_per_sec / 1000000
    bandwidth = (total_bytes_per_sec * 8 ) / time_elapsed 
    data_in = format

    print(f'ID                  INTERVAL            RECEIVD                        Rate')
    print(f'{address[0]}:{address[1]}     0.0-{time_elapsed:.2f}            {total_bytes_per_sec:.2f}:{data_in}                      {(bandwidth):.2f} Mbps')
   