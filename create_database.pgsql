create database dataset;

create table manufacturers (
    id serial primary key,
    mpn varchar(50),
    manufacturer_root_name varchar(50)
);

insert into manufacturers(mpn,manufacturer_root_name) VALUES ('abb-11-01','ABB');
insert into manufacturers(mpn,manufacturer_root_name) VALUES ('abb-11-02','ABB');
insert into manufacturers(mpn,manufacturer_root_name) VALUES ('abb-11-03','ABB');
insert into manufacturers(mpn,manufacturer_root_name) VALUES ('abb-11-04','ABB');
insert into manufacturers(mpn,manufacturer_root_name) VALUES ('abb-11-05','ABB');
insert into manufacturers(mpn,manufacturer_root_name) VALUES ('abb-11-06','ABB');
insert into manufacturers(mpn,manufacturer_root_name) VALUES ('abb-11-07','ABB');
insert into manufacturers(mpn,manufacturer_root_name) VALUES ('abb-11-08','ABB');
insert into manufacturers(mpn,manufacturer_root_name) VALUES ('abb-11-09','ABB');
insert into manufacturers(mpn,manufacturer_root_name) VALUES ('abb-11-10','ABB');