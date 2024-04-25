Simpleperf

Simpleperf er en Python-verktøy som brukes for å måle nettverk ytelse. Denne verktøy kan kjøres på to moduser -serever og -client. Dette verktøy er bra for å teste tilkobling ytelse mellom to data maskiner. Det som kjer under brukt av denne verktøy er at server skal alltid vente på en eller flere klient, og klienten vil sende så mye data som det er mulig på 1000 bytes størrelse. 

Brukt

For å få tilgang til disse må du kjøre simpleperf.py. Brukerne har tilgang til noe argparser argumenter som på den måte kan bestemme sitt ønske. I server siden kan du velge fritt mellom disse argumentene

			Python3 simpleperf.py -s -b <ip-adress> -p <port> -f<format> 
 
I klient siden er det noe en vist argumenter som du kan bruk som, --parallell for å starte flertråding tilkobling, i kommandoen kan vi få tilgang til parallell ved å skrive -P X, der x er antall tråde du ønsker å starte. --num brukes for å velge mengden data brukerne ønsker å sende mye, denne argument kan skrives i kommando -n X[B,MB,KB], der x er mengden data du vil sende og deretter kan du velge typen av data du ønsker. –format for spesifere på hvilket format data skal være. Formatten kan du bruke ved å skrive i kommandoen -f [BYTES, MB, KB, GB], på den måte får du det ønskde data. For å kjøre klinet som er satt normal er det denne kommando vi bruker.

    Python3 simpleperf.py -c -I<server_ip>  -p<server-port>

Det er viktig at når vi kjører simpleperf.py server skal være på og både server og klient skal ha samme ip og port ellers får ikke noe tilkoblingen.

Installasjon

Dette verktøy krever python3 og terminal, deretter kan du Last ned simpleperf jeg har kodet og kjør server modus på en data og klient på en andre. Du kan kjøre både server og klient på en data, men da må du bruke local-host ip adressen


