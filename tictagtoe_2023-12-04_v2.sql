CREATE DATABASE  IF NOT EXISTS `tictagtoe` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `tictagtoe`;
-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: tictagtoe
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `DataId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Type` int NOT NULL,
  `MemId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `TagId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `TargetId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Content` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `CreateTime` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`DataId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hashtag`
--

DROP TABLE IF EXISTS `hashtag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hashtag` (
  `TagId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `TagName` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `TagType` int NOT NULL,
  `Owner` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Status` int NOT NULL,
  `Description` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `CreateTime` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`TagId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hashtag`
--

LOCK TABLES `hashtag` WRITE;
/*!40000 ALTER TABLE `hashtag` DISABLE KEYS */;
INSERT INTO `hashtag` VALUES ('H1685088000','CYCU',4,'M1685006880',1,'中原大學的英文縮寫','2023-05-26-16:00'),('H1685088060','CYIM',4,'M1685006880',1,'中原大學資管系的英文縮寫','2023-05-26-16:01'),('H1685088120','112專題',4,'M1685006880',1,'112年的畢業專題','2023-05-26-16:02'),('H1685088180','專題研究',4,'M1685006880',1,'專題競賽研究新創','2023-05-26-16:03'),('H1685088240','創意專題',4,'M1685006880',1,'具有相當創意的專題','2023-05-26-16:04'),('H1692541200','冷靜',6,'M1685006880',1,'冷靜','2023-08-20-22:20'),('H1693012456','沉著',6,'M1685006880',1,'沉著','2023-08-26-09:14:16');
/*!40000 ALTER TABLE `hashtag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hashtag_relationship`
--

DROP TABLE IF EXISTS `hashtag_relationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hashtag_relationship` (
  `TagId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ObjId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `RelationshipType` int NOT NULL,
  `Status` int NOT NULL,
  `CreateTime` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`TagId`,`ObjId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hashtag_relationship`
--

LOCK TABLES `hashtag_relationship` WRITE;
/*!40000 ALTER TABLE `hashtag_relationship` DISABLE KEYS */;
INSERT INTO `hashtag_relationship` VALUES ('H1685088000','P1685088420',2,1,'2023-05-26-16:07'),('H1685088000','T1685089800',1,1,'2023-05-26-16:30'),('H1685088000','T1685089920',1,1,'2023-05-26-16:32'),('H1685088060','P1685088420',2,1,'2023-05-26-16:07'),('H1685088060','T1685089800',1,1,'2023-05-26-16:30'),('H1685088060','T1685089860',1,1,'2023-05-26-16:31'),('H1685088060','T1685089920',1,1,'2023-05-26-16:32'),('H1685088120','P1685088420',2,1,'2023-05-26-16:07'),('H1685088120','T1685089920',1,1,'2023-05-26-16:32'),('H1685088180','P1685088540',2,1,'2023-05-26-16:09'),('H1685088180','T1685089920',1,1,'2023-05-26-16:32'),('H1685088240','P1685088540',2,1,'2023-05-26-16:09'),('H1685088240','T1685089920',1,1,'2023-05-26-16:32');
/*!40000 ALTER TABLE `hashtag_relationship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `img_target`
--

DROP TABLE IF EXISTS `img_target`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `img_target` (
  `TargetId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `TargetName` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ObjName` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Type` int NOT NULL,
  `Description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `CreateTime` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ImagePath` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`TargetId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `img_target`
--

LOCK TABLES `img_target` WRITE;
/*!40000 ALTER TABLE `img_target` DISABLE KEYS */;
INSERT INTO `img_target` VALUES ('T1685089800','中原資管教室','中原資管教室',2,'位於中原大學的資管樓1樓','2023-05-26-16:30','../static/img/uploads/info_manage_building.jpg'),('T1685089850','tictagtoe','tictagtoe_icon',3,'專題題目','2023-06-11-01:06','../../img/tictagtoe.jpg'),('T1685089860','水壺','水壺',3,'一個由中原大學送的紀念水壺','2023-05-26-16:31','../static/img/uploads/kettle.jpg'),('T1685089920','M1685006880','M1685006880',1,'一位使用者','2023-05-26-16:32','../../img/user.jpg');
/*!40000 ALTER TABLE `img_target` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `MemId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `MemName` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Email` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Status` int NOT NULL,
  `CreateTime` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ImagePath` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `MemAtId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Password` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`MemId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES ('2','Abc','abc',1,'2023-11-30','','@Abc','1234'),('3','Aa','ac@gmail.com',1,'2023-11-30','','@Aa','123'),('4','','',1,'2023-11-30','','@',''),('M1685006880','zhisen123','a123@gmail.com',1,'2023-05-25','../static/img/uploads/冠貓.png','@zhisen','a123'),('M1698637922','test','test@gmail.com',1,'2023-10-30-11:52:02','../static/img/uploads/IMG_3746.JPG','@test','test');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_account_link`
--

DROP TABLE IF EXISTS `member_account_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_account_link` (
  `MemId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `SocialId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `SocialMedia` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Status` int NOT NULL,
  `CreateTime` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`MemId`,`SocialId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_account_link`
--

LOCK TABLES `member_account_link` WRITE;
/*!40000 ALTER TABLE `member_account_link` DISABLE KEYS */;
/*!40000 ALTER TABLE `member_account_link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_img_target`
--

DROP TABLE IF EXISTS `member_img_target`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_img_target` (
  `TargetId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `MemId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `RelationshipType` int NOT NULL,
  `status` int NOT NULL,
  `CreateTime` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`TargetId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_img_target`
--

LOCK TABLES `member_img_target` WRITE;
/*!40000 ALTER TABLE `member_img_target` DISABLE KEYS */;
/*!40000 ALTER TABLE `member_img_target` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_relationship`
--

DROP TABLE IF EXISTS `member_relationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_relationship` (
  `MemId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ObjId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Status` int NOT NULL,
  `CreateTime` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`MemId`,`ObjId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_relationship`
--

LOCK TABLES `member_relationship` WRITE;
/*!40000 ALTER TABLE `member_relationship` DISABLE KEYS */;
INSERT INTO `member_relationship` VALUES ('M1685006880','M1698637922',1,'2023-10-30'),('M1698637922','M1685006880',1,'2023-10-30');
/*!40000 ALTER TABLE `member_relationship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_social_link`
--

DROP TABLE IF EXISTS `member_social_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_social_link` (
  `MemId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `SocialLink` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `CreateTime` datetime NOT NULL,
  PRIMARY KEY (`MemId`,`SocialLink`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_social_link`
--

LOCK TABLES `member_social_link` WRITE;
/*!40000 ALTER TABLE `member_social_link` DISABLE KEYS */;
INSERT INTO `member_social_link` VALUES ('M1685006880','https://twitter.com/','2023-09-08 09:06:40'),('M1685006880','https://www.facebook.com/','2023-08-20 00:37:00'),('M1685006880','https://www.instagram.com/','2023-08-26 09:05:11');
/*!40000 ALTER TABLE `member_social_link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post` (
  `DataId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Title` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Content` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `PostType` int NOT NULL,
  `Owner` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Status` int NOT NULL,
  `CreateTime` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Hashtag` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `MemAtId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`DataId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES ('P1685088420','資管專題1','專題 我們的專題將帶你進入無限可能的世界！我們的團隊充滿熱情和創意，致力於解決實際問題和創新科技。無論是與人工智慧或者數位行銷相關，我們將為你帶來前所未有的啟發與驚喜。跟隨我們的腳步，一起探索未知的領域吧！?',5,'M1685006880',1,'2023-05-26-16:07:20','#CYCU #CYIM #112','桃園中壢',NULL),('P1685088540','資管專題2','這次我們的研究充滿了無限的想像力和創造力。我們將挑戰傳統，探索新領域，為世界帶來全新的視野和驚喜。準備好迎接我們帶來的創新嗎？一起開啟這場奇幻之旅吧！✨',5,'M1685006880',1,'2023-05-26-16:09:30','#專題研究 #創意專題','台北信義',NULL);
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post_extra_file`
--

DROP TABLE IF EXISTS `post_extra_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post_extra_file` (
  `DataId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `PostId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `FilePath` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `FileType` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`DataId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post_extra_file`
--

LOCK TABLES `post_extra_file` WRITE;
/*!40000 ALTER TABLE `post_extra_file` DISABLE KEYS */;
/*!40000 ALTER TABLE `post_extra_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_admin`
--

DROP TABLE IF EXISTS `sys_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_admin` (
  `MemId` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Account` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Password` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Permissions` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `CreateTime` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`MemId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_admin`
--

LOCK TABLES `sys_admin` WRITE;
/*!40000 ALTER TABLE `sys_admin` DISABLE KEYS */;
INSERT INTO `sys_admin` VALUES ('M1685006123','admin@gmail.com','admin','admin','admin','2023-05-25');
/*!40000 ALTER TABLE `sys_admin` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-04 17:46:57
