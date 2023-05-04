CREATE TABLE `plan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `udid_apple` varchar(50) NOT NULL,
  `type_of_device` varchar(50) NOT NULL,
  `telegram_id` varchar(50) DEFAULT NULL,
  `purchase_date` date DEFAULT NULL,
  `date_update` date DEFAULT NULL,
  `wait` date NOT NULL DEFAULT '1970-01-01',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;