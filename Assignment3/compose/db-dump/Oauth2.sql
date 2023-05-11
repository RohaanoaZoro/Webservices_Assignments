
CREATE DATABASE IF NOT EXISTS `Oauth2`;
USE `Oauth2`;


DROP TABLE IF EXISTS `Application`;
CREATE TABLE `Application` (
  `ApplicationId` varchar(45) NOT NULL,
  `ApplicationName` varchar(45) NOT NULL,
  PRIMARY KEY (`ApplicationId`),
  UNIQUE KEY `ApplicationId_UNIQUE` (`ApplicationId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

LOCK TABLES `Application` WRITE;
INSERT INTO `Application` VALUES ('8bd2d864-8d5f-4ec0-95ad-5bb271217658','Url shortner');
UNLOCK TABLES;

DROP TABLE IF EXISTS `Client`;
CREATE TABLE `Client` (
  `ClientId` varchar(45) NOT NULL,
  `ClientSecret` varchar(45) NOT NULL,
  `ApplicationId` varchar(45) NOT NULL,
  PRIMARY KEY (`ClientId`),
  UNIQUE KEY `ClientId_UNIQUE` (`ClientId`),
  UNIQUE KEY `ClientSecret_UNIQUE` (`ClientSecret`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


LOCK TABLES `Client` WRITE;
INSERT INTO `Client` VALUES ('167348','b2f5faf0-7e99-42d1-a5cb-6a5f96988e13','8bd2d864-8d5f-4ec0-95ad-5bb271217658');
UNLOCK TABLES;

DROP TABLE IF EXISTS `JWTKeys`;
CREATE TABLE `JWTKeys` (
  `ApplicationId` varchar(45) NOT NULL,
  `JWTKey` varchar(45) NOT NULL,
  PRIMARY KEY (`ApplicationId`),
  UNIQUE KEY `JWTKey_UNIQUE` (`JWTKey`),
  UNIQUE KEY `ApplicationId_UNIQUE` (`ApplicationId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

LOCK TABLES `JWTKeys` WRITE;
INSERT INTO `JWTKeys` VALUES ('8bd2d864-8d5f-4ec0-95ad-5bb271217658','2a4fd97a-8735-424b-9a68-a63556d3586d');
UNLOCK TABLES;

DROP TABLE IF EXISTS `Sessions`;
CREATE TABLE `Sessions` (
  `SessionId` varchar(45) NOT NULL,
  `ClientId` varchar(45) NOT NULL,
  `Token` varchar(350) NOT NULL,
  `SessionStartTime` varchar(45) DEFAULT NULL,
  `SessionDuration` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`SessionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

LOCK TABLES `Sessions` WRITE;
UNLOCK TABLES;

DROP TABLE IF EXISTS `Users`;

CREATE TABLE `Users` (
  `ClientId` varchar(45) NOT NULL,
  `email` varchar(350) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`ClientId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

LOCK TABLES `Users` WRITE;

UNLOCK TABLES;
