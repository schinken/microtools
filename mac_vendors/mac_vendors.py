import re
import requests
import sys

tablename = 'mac_vendors'
path = 'http://standards.ieee.org/develop/regauth/oui/oui.txt'

def unsafe_escape(sql_value):
    sql_value = sql_value.replace("'", "\'")
    return sql_value

try:
    content = requests.get(path).content
except Exception:
    print "Error retrieving oui.txt from ieee.org"
    sys.exit(0)

regex = re.compile('([0-9a-f]{2})-([0-9a-f]{2})-([0-9a-f]{2})\s+\(hex\)\s+(.*)$', re.I)
for line in content.split("\n"):
    m = regex.search(line)
    if m:
        macaddr = '%02s:%02s:%02s' % (m.group(1), m.group(2), m.group(3))
        vendor = m.group(4)

        print "INSERT INTO %s (macaddr, vendor) VALUES ('%s', '%s');" % (tablename, unsafe_escape(macaddr), unsafe_escape(vendor))
