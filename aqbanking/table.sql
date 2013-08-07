create table accounting (
    id INT(11) PRIMARY KEY auto_increment,
    blz VARCHAR(24),
    kto VARCHAR(24),
    balance DECIMAL(12,2),
    erfda DATETIME
);
