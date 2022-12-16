create schema attendee;
create table attendee.contact_info(
    attendee_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender ENUM('MALE','FEMALE','OTHER'),
    attendee_id, email_address VARCHAR(254) NOT NULL,
    birth_date DATE NOT NULL,
    phone VARCHAR(30) NOT NULL,
    primary key (attendee_id)
);
/*
create table user.address(
    user_id VARCHAR(50) NOT NULL,
    address_line1 VARCHAR(254),
    address_line2 VARCHAR(254),
    city VARCHAR(254),
    state VARCHAR(254),
    zipcode VARCHAR(10),
    country VARCHAR(3),
    primary key (user_id),
    foreign key (user_id) references contact_info(user_id)
);

create table user.payment(
    user_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    card_number VARCHAR(50) NOT NULL,
    cvn VARCHAR(7) NOT NULL,
    exp_month VARCHAR(2) NOT NULL,
    exp_year VARCHAR(2) NOT NULL,
    card_type VARCHAR(10) NOT NULL
)

insert into attendee.contact_info (first_name, last_name, attendee_id, email_address, gender, phone, birth_date) values ('Alicia', 'Arger', 'aarger0@fda.gov', 'aarger0@fda.gov','FEMALE', '625-965-1903', '1973-04-01');
insert into attendee.contact_info (first_name, last_name, attendee_id, email_address, gender, phone, birth_date) values ('Flo', 'Bransdon', 'fbransdon1@bbb.org', 'fbransdon1@bbb.org','MALE', '528-547-0569', '1925-01-31');
insert into attendee.contact_info (first_name, last_name, attendee_id, email_address, gender, phone, birth_date) values ('Lisbeth', 'Custy', 'lcusty2@ehow.com', 'lcusty2@ehow.com','FEMALE', '230-758-6059', '1900-05-21');
insert into attendee.contact_info (first_name, last_name, attendee_id, email_address, gender, phone, birth_date) values ('Katharina', 'Gouth', 'kgouth3@reverbnation.com', 'kgouth3@reverbnation.com','OTHER', '940-934-7059', '1931-11-07');
insert into attendee.contact_info (first_name, last_name, attendee_id, email_address, gender, phone, birth_date) values ('Dolores', 'Gogarty', 'dgogarty4@virginia.edu', 'dgogarty4@virginia.edu','MALE', '156-474-9355', '1953-03-04');
insert into attendee.contact_info (first_name, last_name, attendee_id, email_address, gender, phone, birth_date) values ('Tate', 'Sweeny', 'tsweeny5@digg.com', 'tsweeny5@digg.com','OTHER', '511-513-5905', '1925-03-29');
*/
