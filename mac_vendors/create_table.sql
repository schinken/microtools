CREATE TABLE IF NOT EXISTS mac_vendors (
    id INT(11) auto_increment PRIMARY KEY,
    macaddr CHAR(8),
    vendor VARCHAR(64),
    PRIMARY KEY  (id),
    KEY macaddr (macaddr)
) ENGINE=MyISAM;

TRUNCATE mac_vendors;

