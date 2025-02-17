CREATE TABLE IF NOT EXISTS Outgoing (
    Recipient_Name VARCHAR(255),
    Amount INT,
    Date DATE
);

CREATE TABLE IF NOT EXISTS Incoming (
    Transaction_ID VARCHAR(255),
    Sender_Name VARCHAR(255),
    Amount INT,
    Date DATE
);

CREATE TABLE IF NOT EXISTS Code_Payments (
    Transaction_ID VARCHAR(255),
    Code_number INT,
    Code_name VARCHAR(255),
    Amount INT,
    Date DATE
);

CREATE TABLE IF NOT EXISTS Bank_Deposits (
    Amount INT,
    Date DATE
);

CREATE TABLE IF NOT EXISTS Airtime (
    Transaction_ID VARCHAR(255),
    Amount INT,
    Date DATE
);

CREATE TABLE IF NOT EXISTS Cash_Power (
    Transaction_ID VARCHAR(255),
    Amount INT,
    Token VARCHAR(255),
    Date DATE
);

CREATE TABLE IF NOT EXISTS Withdrawals (
    Transaction_ID VARCHAR(255),
    Amount INT,
    Date DATE,
    Agent VARCHAR(255),
    Agent_Number VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Bundle_Purchases (
    Amount INT,
    Date DATE,
    Transaction_ID VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Third_party (
    Transaction_ID VARCHAR(255),
    Third_party_name VARCHAR(255),
    Amount INT,
    Date DATE
);

