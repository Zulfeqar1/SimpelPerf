import socket
import time
import threading

def connect_client(server_ip, port): #disse parameteren brukes for å koble til serveren, hele funksjon har hovedmål til å koble til server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #her lages en TCP tilkobling 
        s.connect((server_ip, port)) # tilkobling skjer her med serveren ip og port som server lytter på 
        print("-------------------------------------------------")
        print(f"a client connected to {server_ip}: {port}")
        print("-------------------------------------------------")
        return s # returener socket tilkoblingen hvis alt gikk bra
    except ConnectionRefusedError:
        print("Error: failed to connect to server")
        exit() # hvis det gikk ikke bra med tilkobling sendes feil meldign og avslutets socket
             
#hoved formål med dette funksjon er å sende data i bestmet intervaller, denne funksjon kalles ved args-argumenter via client_connection()
def run_interval(server_ip,port,timer,format,args): #parameteren har jeg forkalrt i raporten men ip og port har jeg nevnt her også 
    #parameter timer sier lengden på intervaller som bestemmes av kommandi linje, format bestmmer data typen og foramt kaller fra convert funksjon
    s=connect_client(server_ip, port)
    total_send = 0
    start_time = time.time() #denne brukes for å ta eller starte tiden, nåværende tiden
    current_start_time = start_time
    interval_count = 0
    prev_total_send = 0
    data = bytearray(1000) #vi sender data på størelsen 1000 bytes 
    print(f'ID               INTERVAL        TRANSFER           BANDWITH')

    while time.time() - start_time-1 <=timer: # denn løkken vil kjøres så lenge vi er under --time argumentet og sender mya data på 1000 bytes
        byte_send = s.send(data)
        total_send += byte_send 
        current_time = time.time()
        if current_time - current_start_time >= args.interval: #sjekker om det har gått nok tid, og hvis det har gåt nok tid lik interval da skrives det ut intervalen
            interval_count += args.interval
            interval_send = total_send - prev_total_send
            print(f'{server_ip}:{port}     {interval_count-args.interval}-{interval_count}           {convert(interval_send,format)}        {round(interval_send/args.interval/1000000*8, 2)} Mbps')
            prev_total_send = total_send
            current_start_time = current_time #tror ikke det er viktig å forkalre hva de enkelte setningen gjør
            #beskriver bare de kodet som jeg synes er viktig hvis det mangeler noe forkalring har jeg forklart alt i raporten
    print(f'-----------------------------------------------------------------------------------------------------------------')
    print(f'{server_ip}:{port}     0.0-{timer:.2f}           {convert(total_send,format)}         {round((total_send*8)/(timer*1000000)):.2f} Mbps')#skrives ut den totalt. 
    last(s) # denne funksjon kalles her for å si bye til server og avslutte socket

#denne funksjon kalles når brukerne ønsker å sende bestemt mengde data. og kaller på connect_client() funksjon for å koble til server
def run_num(args):
    s=connect_client(args.server_ip,args.port)
    #denne delen av koden vil konvertere num som kommer fra kommando til antal bytes og ønsket data typen
    size_str = args.num.upper() #gjør num argumente som kommer inn til stor bokstav for å ungå feil
    if size_str[-2:] in ['KB', 'MB']: # hvis argumente kommer med MB eller KB vil dette trekke ut tallet før disse ved hjelp av size_str[-2:] 
        size_num = int(size_str[:-2]) #tallet som ble trukket ut lagres 
        unit = size_str[-2:] #KB eller MB lagres her 
        if unit == 'KB':
            bytes_out = size_num * 1000
        elif unit == 'MB':
            bytes_out = size_num * 1000 * 1000 #til hit i koden, konverteres data 
        elif size_str[-1:] == 'B': #eller hvis argumente er bare en streng altså B-bytes, vil det [-1:] trekke ut tallet som forrige gang 
            size_num = int(size_str[:-1]) #tallet lagres 
            unit = 'B' #strengen lagres her 
            bytes_out = size_num 
    else:
        raise ValueError("the --num format is missing, use -n X[B,MB,KB]") #ved feil input vil det sendes en feil melding

    #i den resten av koden sender vi den bestemte data mengden 
    total_send_bytes = 0
    start_time = time.time()
    data = bytearray(1000)
    while total_send_bytes < bytes_out: #denne løkken vil sende data på 1000 bytes så lengde det er data, og hvis det er ikke noe data stoppes 
        sendt_data = s.send(data)
        if sendt_data == 0:
            break
        total_send_bytes += sendt_data
        total_time = time.time() - start_time #finner ut den totale tiden som ble brukt
    print(f'ID                 INTERVAL          TRANSFER     BANDWITH')
    print(f'{args.server_ip}:{args.port}     0.0-{total_time:.2f}           {size_str}         {round(total_send_bytes/args.time/1000000*8,2)} Mbps') #tror ikke det er viktig å si akkurat hva denne gjør
    last(s) #kalles denne funksjon helt sist og avlutte tilkoblingen. funkjsjon last() forklarer jeg nede.

#denn funksjon sender data i prallell tråd tilkobling, hver tråd tar tilkobler til server ved hjelp av args.server_ip, port, ved å bruke paralel_send_data funksjon 
def run_parallel(args): 
    threads = [] #her lages et tøm liste og legges på liste for hver nye tråd som starter
    for i in range(args.parallel): #tar inn antall tråd ønskes fra kommando linje
        t = threading.Thread(target=paralel_send_data, args=(args.server_ip,args.port,args.time,args.format)) #hver tråd kaller på funksjonen som indikerer parameterene
        threads.append(t)
        t.start() # her starter alle trådene etter at de ble lagd til listen
    for t in threads: #denne delen av koden venter på at alle trådene gjør ferdig sitt kjøring ved å kalle på join()
        t.join()
#denne funksjon er en del av run_parallel, og hver tråd vil bruke denne funksjon for å joine til server, ved connect_client(server_ip,port)
def paralel_send_data(server_ip,port,timer,format): # parameteren har jeg forklart men timer indikeres fra kommandi linje at hvor lenge skal være tilkoblingen og på hvilket format
    s= connect_client(server_ip,port)
    start_time = time.time()
    data = bytearray(1000)
    bytes_send = 0
    while time.time() - start_time < timer: #løkken kjøres så lenge den er under args-timen
        try:
            s.send(data)
            bytes_send += len(data)
        except OSError as e: #hvis det oppstår feil under sending vil vil ved try og except fange her
            print(f"Error sending data: {e}")
            break
    data=bytes_send*8
    data_mbp=data/timer
    data_mbps=data_mbp/1000000  #dette er måten jeg for delte båndbredde på 
    print(f'ID                 INTERVAL           TRANSFER          BANDWITH')
    print(f'{server_ip}:{port}     0.0-{timer:.2f}           {convert(bytes_send,format)}          {round(data_mbps,2)} Mbps')
    last(s) # kalles funksjon for å avslutte socket

#hvis det blir ikke kalt neo argument ville jeg kjøre dette
def run_default(args): #prameteren tar inn argument som kommer fra kommandoen, og tilkobles til srver ved connect_client(args.server_ip,args.port)
    s=connect_client(args.server_ip,args.port)
    total_send = 0
    start_time = time.time()
    print(f'ID                 INTERVAL        TRANSFER          BANDWITH')
    data = bytearray(1000) #vi sender mye data på 1000 bytes 

    while time.time() - start_time < args.time: #løkke som kjøres så lenge den er under argument tiden
        byte_send = s.send(data)
        total_send += byte_send       
               
    print(f'{args.server_ip}:{args.port}     0.0-{args.time}           {convert(total_send,args.format)}        {round(total_send/args.time/1000000*8, 2)} Mbps')
    last(s) #kalles dette funksjon og avsluttes


#denn funksjon kalles ofte, og det den gjør er å konvertere data typen til ønsket data og kan velges i kommandoen ved args-parser
def convert(total_bytes, format): # tototal_bytes er det den antsll biten som skal konverteres, format ville si på hvilket typen vil foramteres
    units = {'BYTES': 1, 'KB': 1000, 'MB': 1000000, 'GB': 1000000000} #tar inn enhetene som skal konverteres til 
    factor = units[format] # her henter factor hvilket unit skal den total_bytes vises i, eksmepel hvsi vi ønsker KB henter faktor KB enheten her som er 1000 
    total_size = total_bytes / factor #i denne linje deler vi total data som vi ønsker å konvertere og deler vi på factor
    return f'{total_size:.2f} {format}' #her returnerer vi totale størelsen med to desimaler, og ønskede enhet.

#denne funksjon kalles når klinet er ferdig med å sende sin data, altså det er siste ting klinet vil gjør
def last(s):#i denen funkson vil klient sende en by message til server og få en respons tilbake
    try:
        s.sendall(b'good bye')
        response = s.recv(1024).decode("utf-8")
        if response == "Good bye!": #dett er resposn fra server
            print(response)
        else:
            print("Error: Did not receive expected acknowledgment message from server.")
    except Exception as e:
        print(f'Error: {str(e)}') #hvis vi ikke fått respons skriver ut en feil melding
    finally:
        s.close() #avslutter socket

#hver gang vi skal kjøre klient vil klienten kjøre dette funksjon. denne funksjon inneholde 4 type args. og noe av dem blir kalt fra kommando kjøres dem.
def client_connection(server_ip,port, args=None): #denne funksjon tar inn tre parameter og en valgfri args-argument 
        try:
            if args and args.interval:
                run_interval(args.server_ip,args.port,args.time,args.format,args)
            elif args and args.num:
                run_num(args)
            elif args and args.parallel:
                run_parallel(args)
            else:
                not args
                run_default(args) #hvis det blir ingen args-argument og da klinet kjøres på denne modusen altså normal
        except Exception as e:
            print(f'enable to connect to the server: {e}') #vi får en feil melding hvis tilkoblingene ikke vellykes