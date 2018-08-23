DROP database IF EXISTS `ALERT`;              /* if the database exists, it will be drop*/
CREATE database ALERT;
use ALERT;


/*create the table ZIT*/

DROP TABLE IF EXISTS `ZIT`;        /* if the table exists, it will be drop*/
CREATE TABLE `ZIT`(
    `ID` int not null auto_increment primary key,
    `lco_id` int UNIQUE,	/**/
    `objectId` varchar(40),	/**/
    `magpsf`   DOUBLE,		/**/	
    `sigmapsf`	DOUBLE,		/**/
    `figurepath` varchar(80),    /**/
    `filter` varchar(2),       /*filter*/
    `ra` DOUBLE,           /*Right Ascension of target*/
    `dec` DOUBLE,          /*Declination of target*/
    `jd` DOUBLE,    /*Julian Date*/
    `wall_time` varchar(80) 	/**/

);


/*grant the privilege to somebody*/

GRANT ALL PRIVILEGES ON ALERT.* TO 'ALERT'@'localhost' identified by '1234';
GRANT select ON ALERT.* TO 'read'@'localhost' identified by'1234';
FLUSH PRIVILEGES;               /*refresh the user */
