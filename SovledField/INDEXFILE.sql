DROP database IF EXISTS `INDEXFILE`;              /* if the database exists, it will be drop*/
CREATE database INDEXFILE;
use INDEXFILE;

/*create the table targets*/

DROP TABLE IF EXISTS `INDEXFILE`;           /* if the table exists, it will be drop*/
CREATE TABLE `INDEXFILE`(

`ID` int not null auto_increment primary key,
`FILENAME` varchar(80) UNIQUE,
`FILEPATH` varchar(80),
`INDEX` varchar(20),  
`RA,DEC (deg)` varchar(60),         
`(RA H:M:S, Dec D:M:S)` varchar(60) 

);


GRANT ALL PRIVILEGES ON INDEXFILE.* TO 'TAT'@'localhost' identified by '1234';
GRANT select ON INDEXFILE.* TO 'read'@'localhost' identified by'1234';
FLUSH PRIVILEGES; 






