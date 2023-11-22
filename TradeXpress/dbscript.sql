USE mysql;
CREATE USER 'dbadmin'@'localhost' IDENTIFIED BY 'db1234';
GRANT ALL PRIVILEGES ON *.* TO 'dbadmin'@'localhost'
WITH GRANT OPTION;

CREATE USER 'dbadmin'@'%' IDENTIFIED BY 'db1234';
GRANT ALL PRIVILEGES ON *.* TO 'dbadmin'@'%'
WITH GRANT OPTION;
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin1234';
GRANT RELOAD,PROCESS ON *.* TO 'admin'@'localhost';

SELECT user, host FROM user;

CREATE DATABASE intellitrade;
