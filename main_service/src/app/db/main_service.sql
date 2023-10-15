create table info (
    id integer primary key,
    name varchar(50),
    age integer
);

create table users(
    card_number varchar(100) primary key,
    balance integer,
    info_id integer,
    card_limit integer,
    foreign key (info_id) references info(id)
);

create table user_storage (
    user_storage_id integer ,
    card_number varchar(100) primary key,
    is_active boolean
);

create table token (
    token_id integer primary key,
    card_number varchar(100),
    token integer,
    expires date,
    Foreign Key (card_number) REFERENCES users(card_number)
);

create table balance_log(
    card_number varchar(100),
    before integer,
    after integer,
    changes integer,
    datetime_utc date
)

create table common_log(
    card_number varchar(100),
    before varchar,
    after varchar,
    changes varchar,
    datetime_utc date
)

create table log_storage(
    log_storage_id integer primary key,
    balance_log_id varchar(100),
    common_log_id varchar(100)
)

create table transactions(
    transactions_id integer primary key,
    user_storage_id varchar(100),
    log_storage_id integer,
    foreign key (user_storage_id) references user_storage(card_number),
    foreign key(log_storage_id) references log_storage(log_storage_id)
)


insert into info values(3,'andrey', 30);
insert into users values('3333', 300000, 3);
insert into user_storage values(3, '3333', true);
insert into token values(4, '3333', 123, '2025-05-23');
insert into token values(5, '3333', 123, '2022-05-23');

insert into balance_log values('3333',0,100,100,'2023-05-23');
insert into balance_log values('3333',100,200,100,'2024-05-23');
insert into common_log values('3333','abc','bca','bca','2023-05-23');

INSERT into log_storage values(1,'3333','3333');
insert into transactions VALUES(1, '3333', 1);

--вывод исттории изменения баланса
select card_number, before, after, changes from (select * from transactions
join log_storage
on transactions.log_storage_id=log_storage.log_storage_id) as t, balance_log
where t.balance_log_id=balance_log.card_number;

--вывод истории изменений
select card_number, before, after, changes from (select * from transactions
join log_storage
on transactions.log_storage_id=log_storage.log_storage_id) as t, common_log
where t.common_log_id=common_log.card_number;

--вывод баланса пользователя
select balance from transactions
join user_storage
on transactions.user_storage_id=user_storage.card_number
join users
on user_storage.card_number=users.card_number;

--вывод информации о пользователе
select users.card_number, balance, users.card_limit, name, age from transactions
join user_storage
on transactions.user_storage_id=user_storage.card_number
join users
on user_storage.card_number=users.card_number
join info
on users.info_id = info.id;

--изменение баланса
update users set balance = 10 where card_number='3333';

--изменение информации
update info set name='Ivan', age=25 where id=3;

--изменение лимита
update users set card_limit=2000 where card_number='3333';

delete from transactions where transactions_id=1;
delete from log_storage where balance_log_id='3333';
delete from balance_log where before=0;

drop table transactions;
drop table log_storage;
drop table balance_log;
drop table common_log;
drop table token;
drop table user_storage;
drop table users;
drop table info;