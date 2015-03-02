# aqbanking

beispiel für raifeissenbank

Mehr: http://www.loebhard.com/linux/homebanking

## warning

Wenn vorher schon ein Zugang eingerichtet war, sollte man vorher das ~/.aqbanking-Verzeichnis löschen, da sonst aqhbci-tool4 getsysid mit "133: Ambiguous customer specification" antwortet. Vorallem dann, wenn die geänderten Login-Daten auf das gleiche Konto zeigen

## Setup
 aqhbci-tool4 adduser --tokentype=pintan -s hbci11.fiducia.de/cgi-bin/hbciservlet -b $BLZ --username=$USERNAME --customer=$USERNAME --user=$USER_ID --hbciversion=300
 
#### Zertifikat akzeptieren
 aqhbci-tool4 getsysid
 
#### daten konfigurieren
 vim get_balance.sh 

## kontostand abfragen
 ./get_balance.sh
