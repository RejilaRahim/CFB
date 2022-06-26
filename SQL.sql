/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 5.6.12-log : Database - cfb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`cfb` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `cfb`;

/*Table structure for table `bank` */

DROP TABLE IF EXISTS `bank`;

CREATE TABLE `bank` (
  `bankid` int(11) NOT NULL AUTO_INCREMENT,
  `accnumber` varchar(20) DEFAULT NULL,
  `cvv` varchar(20) DEFAULT NULL,
  `amount` varchar(20) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  PRIMARY KEY (`bankid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `bank` */

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_ID` int(11) NOT NULL AUTO_INCREMENT,
  `complaint` varchar(50) DEFAULT NULL,
  `reply` varchar(50) DEFAULT NULL,
  `c_date` varchar(11) DEFAULT NULL,
  `r_date` varchar(11) DEFAULT NULL,
  `user_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`complaint_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`complaint_ID`,`complaint`,`reply`,`c_date`,`r_date`,`user_ID`) values 
(1,'qwerty','asdfgh','2022-03-26','2022-03-26',4),
(2,'asdfgh','pending','2022-03-26','pending',4),
(3,'zxcvbn','pending','2022-03-26','pending',5);

/*Table structure for table `donation` */

DROP TABLE IF EXISTS `donation`;

CREATE TABLE `donation` (
  `d_ID` int(11) NOT NULL AUTO_INCREMENT,
  `donation` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `user_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`d_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `donation` */

insert  into `donation`(`d_ID`,`donation`,`status`,`date`,`user_ID`) values 
(1,'abcv','complete','2022-03-22',1),
(2,'zxc','pending','2022-03-20',4);

/*Table structure for table `donation_request` */

DROP TABLE IF EXISTS `donation_request`;

CREATE TABLE `donation_request` (
  `req_ID` int(11) NOT NULL AUTO_INCREMENT,
  `donation` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`req_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `donation_request` */

insert  into `donation_request`(`req_ID`,`donation`,`date`,`status`) values 
(1,'xcvbnm,','2022-03-22','pending'),
(2,'zxcvbnm,','2022-03-22','pending'),
(3,'qwergfff','2022-03-23','pending');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_ID` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) DEFAULT NULL,
  `password` varchar(10) DEFAULT NULL,
  `user_type` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`login_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_ID`,`user_name`,`password`,`user_type`) values 
(1,'admin','admin','admin'),
(4,'rejilarahim1997@gmail.com','abcd','user'),
(5,'rejilarahim@gmail.com','abcd','user'),
(6,'rejilarahim199@gmail.com','abcd','user'),
(7,'rejilarahim1997@gmail.com','abcd','user'),
(11,'rejilarahim17@gmail.com','abcd','user'),
(12,'rejilarahim23456@gmail.com','abcd','user');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_ID` int(11) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `post` varchar(50) DEFAULT NULL,
  `pin` int(10) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` bigint(12) DEFAULT NULL,
  `image` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_ID`,`username`,`dob`,`place`,`post`,`pin`,`email`,`phone`,`image`) values 
(4,'ASD','0000-00-00','abc','sdf',0,'rejilarahim1997@gmail.com',1234567890,'/static/Image/220326-093152.jpg'),
(5,'nimda','0000-00-00','admin','sdf',0,'rejilarahim@gmail.com',1234567890,'/static/Image/220326-093944.jpg'),
(6,'rejilarahim','0000-00-00','admin','sdf',0,'rejilarahim199@gmail.com',1234567890,'/static/Image/220403-164742.jpg'),
(7,'rejila','0000-00-00','nimda','sdf',1234,'rejilarahim1997@gmail.com',2147483647,'/static/Image/220403-165339.jpg'),
(11,'reji','2022-04-25','xcvb','sdfghjk',1234,'rejilarahim17@gmail.com',6234567890,'/static/Image/220404-142610.jpg'),
(12,'asdfghjk','2022-04-06','asxcvbn','zxcvb',12345,'rejilarahim23456@gmail.com',6234567890,'/static/Image/220404-151838.jpg');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
