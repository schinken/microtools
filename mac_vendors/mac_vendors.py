import re
import requests
import settings
import sys
import MySQLdb

try:
    print "Loading content from %s" % (settings.ieee_url,)
    content = requests.get(settings.ieee_url).content
except Exception:
    print "Error retrieving oui.txt from ieee.org"
    sys.exit(1)

db = MySQLdb.connect(host=settings.mysql_host,
                    user=settings.mysql_user,
                    passwd=settings.mysql_pass,
                    db=settings.mysql_name)

db_cur = db.cursor()

print "Creating table %s if not exist..." % (settings.table_name,)
db_cur.execute("""CREATE TABLE IF NOT EXISTS %s (
    id INT(11) auto_increment PRIMARY KEY,
    macaddr CHAR(8),
    vendor VARCHAR(128),
    KEY macaddr (macaddr)
) ENGINE=MyISAM;""" % (settings.table_name,))

print "Removing all old entried"
db_cur.execute('TRUNCATE %s' % (settings.table_name,))


print "Parsing vendor mac addresses..."

insert = "INSERT INTO %s (macaddr, vendor) VALUES (%%s, %%s)" % (settings.table_name,)
vendors = 0
regex = re.compile('([0-9a-f]{2})-([0-9a-f]{2})-([0-9a-f]{2})\s+\(hex\)\s+(.+)$', re.I)
for line in content.split("\n"):
    m = regex.search(line)
    if m:
        macaddr = '%02s:%02s:%02s' % (m.group(1), m.group(2), m.group(3))
        vendor = m.group(4)

        db_cur.execute(insert, (macaddr, vendor))

        vendors = vendors + 1


print "Added %d vendors" % (vendors,)
