#!/bin/bash

#############################################################################
# Configuration

# Database Credentials
SQL_HOST="violet"
SQL_USER="bank"
SQL_PASS="lollolol"
SQL_NAME="mydb"

# Files
AQBANKING_CLI="/usr/bin/aqbanking-cli"
PINFILE="/tmp/pinfile"
CTX_FILE="/tmp/tmp.ctx"
SNMP_FILE="/tmp/account_balance.snmp"

# HBCI Credentials
USER=""
PIN=""

# Account credentials
BLZ=""
KTO=""

#############################################################################
# HBCI Magic

# Create temporary pinfile
echo "PIN_${BLZ}_${USER} = \"$PIN\"" > $PINFILE

# request account balance from bank
$AQBANKING_CLI -n -P $PINFILE request -b $BLZ -a $KTO -c $CTX_FILE --balance 2> /dev/null

# retrieve balance from CTX file
BALANCE=`$AQBANKING_CLI listbal -b $BLZ -a $KTO -c $CTX_FILE 2> /dev/null | awk '{print $10}'`

# Context-File, Pinfile is not needed anymore
rm -f $CTX_FILE
rm -f $PINFILE

echo $BALANCE

# check if number is numeric
if echo $BALANCE | egrep -v -q '^[0-9]+\.[0-9]+$'; then
    echo "$BALANCE is not a number"
    exit 1
fi

#############################################################################
# Store dat shit

echo $BALANCE > $SNMP_FILE

exort MYSQL_PWD="$SQL_PASS"
echo "INSERT INTO accounting (blz, kto, balance, erfda) VALUE ('$BLZ', '$KTO', $BALANCE, NOW())" | \
        mysql -h "$SQL_HOST" -u "$SQL_USER" "$SQL_NAME"

unset MYSQL_PWD

exit 0;
