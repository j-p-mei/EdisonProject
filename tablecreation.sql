--create database carddatabase

create table Card(
    CardID  integer, 
    CardName varchar(100),
    SetName varchar(100),
    ProductID integer,
    SKUID integer,
    Condition integer,
    Edition integer,
    Language integer
)

create table CardPrice(
    CardID  integer, 
    PriceDate date,
    Price double
)

