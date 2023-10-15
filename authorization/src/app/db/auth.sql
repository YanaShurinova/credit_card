create table users(
    user_id int,
    login varchar(50),
    password varchar(50)
);

create table tokens (
    token_id integer primary key,
    user_id integer,
    token varchar(100),
    expires datetime,
    Foreign Key (user_id) REFERENCES users(user_id)
);


insert into users values(1, 'admin', 'password');

insert into tokens values(1, 1, '123', '2023-05-23T10:10:10');
insert into tokens values(2, 1, '321', '2022-05-23T10:10:10');

select user_id from users where login='admin' and password='password';

select * from users 
join tokens
on users.user_id=tokens.user_id


delete from tokens where token_id=1;


drop table tokens;

drop table users;