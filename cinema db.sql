create table movies(
	m_id int primary key,
	m_name varchar(50),
	description varchar(150)
);

create table cinemas(
	c_id int primary key,
	c_name varchar(20),
	address varchar(50)
);

create table cin_hall(
	ch_id int primary key,
	c_id int references cinemas(c_id) on delete cascade
);

create table schedule(
	sch_id int primary key, 
	sch_time int,
	m_id int references movies(m_id) on delete cascade,
	ch_id int references cin_hall(ch_id) on delete cascade
);

create table seats(
	s_id serial primary key,
	s_num int,
	status boolean,
	sch_id int references schedule(sch_id) on delete cascade
);

create table users(
	user_id serial primary key,
	user_name varchar(20),
	user_pass varchar(25)
);

create table orders(
	order_id serial primary key,
	myorder varchar(150),
	user_id int references users(user_id) on delete cascade
);

create table price(
	time_id int primary key,
	kids int not null,
	students int not null,
	adults int not null
);

insert into movies(m_id, m_name, description)
values 
(1, 'Гудбай, мой бай', 'Казахстанский фильм вот'),
(2, 'Fantastic Beasts', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'),
(3, 'Ralph 2', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'), 
(4, 'Businessmen', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'),
(5, 'Bohemian Rhapsody', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'),
insert into movies(m_id, m_name, description) values
(6, 'Spider-Man: Into the Spider-Verse', '«Человек-паук: Через вселенные» — американский анимационный фильм, основанный на персонаже Marvel Comics Майлзе Моралесе, произведенный Columbia Pictures и Sony Pictures Animation и распространенный Sony Pictures Releasing.'),
(7, 'Aquaman', '«Человек-паук: Через вселенные» — американский анимационный фильм, основанный на персонаже Marvel Comics Майлзе Моралесе, произведенный Columbia Pictures и Sony Pictures Animation и распространенный Sony Pictures Releasing.'),
(8, 'The Departed', 'Два лучших выпускника полицейской академии оказались по разные стороны баррикады: один из них — агент мафии в рядах правоохранительных органов, другой — «крот», внедрённый в мафию.'),
(9, 'Bumblebee', '«Ба́мблби» — американский научно-фантастический боевик. Это спин-офф и приквел фильма Трансформеры сюжет которого закручен вокруг автобота Бамблби. Режиссёр — Трэвис Найт. Премьера фильма в России состоялась 13 декабря 2018 года.'),
(10, 'Ready Player One', 'Действие фильма происходит в 2045 году, мир погружается в хаос и находится на грани коллапса. Люди ищут спасения в игре OASIS — огромной вселенной виртуальной реальности. Ее создатель, гениальный и эксцентричный Джеймс Холлидэй, оставляет уникальное завещание.'),
(11, 'Deadpool 2', 'Единственный и неповторимый болтливый наемник — вернулся! Ещё более масштабный, ещё более разрушительный и даже ещё более голозадый, чем прежде! Когда в его жизнь врывается суперсолдат с убийственной миссией, Дэдпул вынужден задуматься о дружбе, семье и о том, что на самом деле значит быть героем');


insert into cinemas(c_id, c_name, address)
values
(1, 'Illusion', 'Maxima'),
(2, 'Chaplin', 'Mega Park'),
(3, 'Bekmambetov', 'Globus');

insert into cin_hall(ch_id, c_id)
values (1, 1), (2, 1), (3, 1),
	   (4, 2), (5, 2), (6, 2),
	   (7, 3), (8, 3), (9, 3);
	   
insert into schedule(sch_id, sch_time, m_id, ch_id)
values
(1, 10, 1, 1), (2, 13, 2, 1), (3, 16, 3, 1), (4, 20, 4, 1), (5, 22, 1, 1),
(6, 10, 3, 2), (7, 13, 4, 2), (8, 16, 1, 2), (9, 20, 5, 2), (10, 22, 2, 2),
(11, 10, 2, 3), (12, 13, 1, 3), (13, 16, 4, 3), (14, 20, 5, 3), (15, 22, 3, 3),

(16, 10, 5, 4), (17, 13, 4, 4), (18, 16, 3, 4), (19, 20, 2, 4), (20, 22, 1, 4),
(21, 10, 5, 5), (22, 13, 3, 5), (23, 16, 2, 5), (24, 20, 1, 5), (25, 22, 4, 5),
(26, 10, 4, 6), (27, 13, 2, 6), (28, 16, 3, 6), (29, 20, 1, 6), (30, 22, 5, 6),

(31, 10, 1, 7), (32, 13, 5, 7), (33, 16, 3, 7), (34, 20, 4, 7), (35, 22, 2, 7),
(36, 10, 1, 8), (37, 13, 4, 8), (38, 16, 5, 8), (39, 20, 2, 8), (40, 22, 3, 8),
(41, 10, 5, 9), (42, 13, 3, 9), (43, 16, 2, 9), (44, 20, 1, 9), (45, 22, 4, 9);


insert into users(user_name, user_pass)
values ('admin', 'otboga');

ALTER TABLE orders ALTER COLUMN myorder TYPE text;
ALTER TABLE movies ALTER COLUMN description TYPE text;
ALTER TABLE movies ALTER COLUMN m_name TYPE varchar(150);