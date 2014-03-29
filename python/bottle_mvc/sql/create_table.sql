CREATE TABLE iplist (
	id INT(4) NOT NULL AUTO_INCREMENT,
	ipaddress VARCHAR(255),
	hostname VARCHAR(255),
	macaddress VARCHAR(255),
	vlan INT(4),
	purpose VARCHAR(255),
	regdate DATETIME,
	PRIMARY KEY (`id`)
) DEFAULT CHARACTER SET = utf8
