# aqbanking

beispiel für raifeissenbank

Mehr: http://www.loebhard.com/linux/homebanking

## einrichten
 aqhbci-tool4 adduser --tokentype=pintan -s hbci11.fiducia.de/cgi-bin/hbciservlet -b $BLZ --username=$USERNAME --customer=$USERNAME --user=$USER_ID --hbciversion=300
 
## certificate akzeptieren
 aqhbci-tool4 getsysid
 
## daten konfigurieren
 vim get_balance.sh 

## kontostand abfragen
 ./get_balance.sh
