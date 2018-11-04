DROP TABLE IF EXISTS `barbershop`.`sell_item_list`;
create table `barbershop`.`sell_item_list` (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	`item_number` varchar(20) unique,
    `hairdresser` varchar(100),
    `assistant` varchar(100),
    `item_type` varchar(50),
    `money` int,
    `pay_type` varchar(100),
    `fellow` varchar(100),
    `comment` varchar(200),
    `created_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS `barbershop`.`users`;
CREATE TABLE `barbershop`.`users` (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	`username` VARCHAR(16) NOT NULL,
	`password` VARCHAR(100) NOT NULL,
	`page_level` int NOT NULL,
	`comment` varchar(200),
	`created_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS `barbershop`.`fellow_types`;
CREATE TABLE `barbershop`.`fellow_types` (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	`card_type_name` VARCHAR(16) NOT NULL,
	`discount` VARCHAR(10),
	`comment` varchar(200),
	`created_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS `barbershop`.`employee_types`;
CREATE TABLE `barbershop`.`employee_types` (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	`type_name` VARCHAR(16) NOT NULL,
    `responsibility` varchar(200),
	`comment` varchar(200),
	`created_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS `barbershop`.`fellow_list`;
CREATE TABLE `barbershop`.`fellow_list` (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(16) NOT NULL,
	`phone_number` VARCHAR(32) NOT NULL unique,
	`birthday` VARCHAR(100) NOT NULL,
    `password` VARCHAR(32),
    card_type varchar(20) NOT NULL,
    money int not null,
    created_by varchar(20) not null,
	`created_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS `barbershop`.`employee_list`;
CREATE TABLE `barbershop`.`employee_list` (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(16) NOT NULL,
	`phone_number` VARCHAR(32) NOT NULL,
	`first_day` VARCHAR(100) NOT NULL,
    `employee_type` varchar(20) NOT NULL,
    base_salary varchar(20) NOT NULL,
    percentage varchar(20) not null,
    `status` varchar(20) not null,
	`created_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS `barbershop`.`fellow_money_history_list`;
CREATE TABLE `barbershop`.`fellow_money_history_list` (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	phone_number VARCHAR(32) NOT NULL,
    card_type varchar(20) NOT NULL,
    expend_money int,
    remain_money int not null,
    sell_item_number varchar(20),
    reason varchar(20) not null,
	`created_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS `barbershop`.`employee_money_histroy_list`;
CREATE TABLE `barbershop`.`employee_money_histroy_list` (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	phone_number VARCHAR(32) NOT NULL,
	name VARCHAR(32),
	percentage VARCHAR(32) not null,
    sell_item_money int,
    money int not null,
    sell_item_number varchar(20),
    reason varchar(20) not null,
	`created_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);
  
DROP TABLE IF EXISTS `barbershop`.`cash_flow`;
CREATE TABLE `barbershop`.`cash_flow` (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
    sell_item_number varchar(20),
    money int not null,
    flow_direction varchar(10) not null,
    reason varchar(20) not null,
    comment varchar(500),
	`created_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

insert into `barbershop`.`users` (`username`, `password`, `page_level`, `comment`) values ('admin', '*admin_neal_8', '1', 'hello');
insert into `barbershop`.`fellow_types` (`card_type_name`, `discount`, `comment`) values ('7折卡', '0.7', '');
insert into `barbershop`.`fellow_types` (`card_type_name`, `discount`, `comment`) values ('5折卡', '0.5', '');
insert into `barbershop`.`fellow_types` (`card_type_name`, `discount`, `comment`) values ('次卡', '0.7', '');
insert into `barbershop`.`employee_types` (`type_name`, `responsibility`, `comment`) values ('店长', '负责协调', '备注');
insert into `barbershop`.`employee_types` (`type_name`, `responsibility`, `comment`) values ('发型师', '', '备注');
insert into `barbershop`.`employee_types` (`type_name`, `responsibility`, `comment`) values ('助理', '', '备注');
insert into `barbershop`.`employee_types` (`type_name`, `responsibility`, `comment`) values ('管理员', '', '备注');
