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
	`password` VARCHAR(32) NOT NULL,
	`page_level` int NOT NULL,
	`create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS `barbershop`.`fellow_list`;
CREATE TABLE `barbershop`.`fellow_list` (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(16) NOT NULL,
	`phone_number` VARCHAR(32) NOT NULL unique,
	`birthday` VARCHAR(32) NOT NULL,
    `password` int NOT NULL,
    card_type varchar(20) NOT NULL,
    money int not null,
    created_by varchar(20) not null,
	`create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS `barbershop`.`employee_list`;
CREATE TABLE `barbershop`.`employee_list` (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(16) NOT NULL,
	`phone_number` VARCHAR(32) NOT NULL,
	`birthday` VARCHAR(32) NOT NULL,
    `emplyee_type` varchar(20) NOT NULL,
    base_salary varchar(20) NOT NULL,
    percentage varchar(20) not null,
    `status` varchar(20) not null,
	`create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

DROP TABLE IF EXISTS `barbershop`.`fellow_histroy_list`;
CREATE TABLE `barbershop`.`fellow_history_list` (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	phone_number VARCHAR(32) NOT NULL,
    card_type varchar(20) NOT NULL,
    expend_money int,
    remain_money int not null,
    item_number varchar(20),
    reason varchar(20) not null,
	`create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);
  
insert into `barbershop`.`sell_item_list` (item_number, hairdresser, assistant, item_type, money, pay_type, fellow, `comment`) values ('1010201sd12', '杨', '李', '染发', 200, '刷卡', '13121234589', "备注");

insert into `barbershop`.`users` (`username`, `password`, `page_level`) values ('admin', 'admin', '1');

insert into fellow_list (name, phone_number, birthday, password, card_type, money, created_by) values ("Neal", "1937843398", "", "123", "5折卡", "1000", "牛");

insert into employee_list (name, phone_number, birthday, emplyee_type, base_salary, percentage, status) values ("牛", "1392239", "", "店长", "1000", "0.5", "在职");
insert into employee_list (name, phone_number, birthday, emplyee_type, base_salary, percentage, status) values ("委任为", "13922391", "", "发型师", "1000", "0.5", "在职");
insert into employee_list (name, phone_number, birthday, emplyee_type, base_salary, percentage, status) values ("手动阀手动阀", "121423", "", "助理", "1000", "0.5", "在职");