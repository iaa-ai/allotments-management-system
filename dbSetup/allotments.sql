-- MySQL dump 10.13  Distrib 8.0.13, for Win64 (x86_64)
--
-- Host: localhost    Database: allotments
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `allotments`
--

DROP TABLE IF EXISTS `allotments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `allotments` (
  `Allotment_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Site_ID` int(11) NOT NULL,
  `Allotment_Location` varchar(200) DEFAULT NULL,
  `Size` decimal(10,2) DEFAULT NULL,
  `Annual_Rental` decimal(10,2) DEFAULT NULL,
  `Other_Details` text,
  PRIMARY KEY (`Allotment_ID`),
  KEY `Site_ID` (`Site_ID`),
  CONSTRAINT `allotments_ibfk_1` FOREIGN KEY (`Site_ID`) REFERENCES `sites` (`site_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `allotments`
--

LOCK TABLES `allotments` WRITE;
/*!40000 ALTER TABLE `allotments` DISABLE KEYS */;
INSERT INTO `allotments` VALUES (1,14,'7996 Charles Extensions Suite 062\nNorth Michael, NV 08831',86.00,663.11,'They ago provide gas race including hour.'),(2,2,'4606 Underwood Turnpike\nEast Andrewton, VA 60862',142.10,2452.31,'Really media become you more control might.'),(3,14,'697 Jessica Groves Apt. 951\nWest Christineburgh, AL 71750',68.57,913.29,'Fine day begin bag.'),(4,21,'00437 Laura Creek Apt. 586\nEast Zacharymouth, UT 01944',57.31,1750.36,'Imagine popular difficult point customer husband.'),(5,20,'98130 Andrews Brook Suite 046\nTammyhaven, WV 63287',193.40,1340.73,'Bank early day across whom a magazine.'),(6,12,'0549 Campos Ridge\nRachaelbury, AS 57565',171.50,573.06,'Identify become old.'),(7,9,'Unit 9006 Box 2813\nDPO AE 05673',166.48,2680.98,'Those reduce today field seven.'),(8,16,'61645 Richard Key Suite 676\nClaytonhaven, OR 74112',87.80,2574.77,'Old firm sing true opportunity on somebody.'),(9,9,'535 Matthew Radial Apt. 907\nSouth John, SC 62289',161.49,1705.64,'Mention sound same type summer.'),(10,16,'1801 Chad Loaf\nAmyshire, MH 48377',155.05,2451.27,'Owner role interesting science situation opportunity then reflect.'),(11,5,'34607 Francisco Mill\nHowellhaven, WY 85983',79.47,2836.80,'Into up focus hope.'),(12,20,'Unit 8760 Box 8525\nDPO AE 13650',194.02,933.15,'Easy start power.'),(13,23,'212 Bailey Squares Suite 028\nNew Laurenbury, GA 11472',198.97,2023.14,'Senior senior computer support baby while.'),(14,10,'75603 Gutierrez Estates\nEast Rebeccatown, FM 53768',133.39,1643.76,'Notice security or seek drop can continue.'),(15,19,'49691 Benjamin Orchard Apt. 000\nLake Steventown, OK 61367',104.44,2954.42,'Pass relate from popular sign.'),(16,22,'446 Mathews Ports\nNavarromouth, MP 23797',142.49,1789.26,'Seat I reflect thought citizen break.'),(17,9,'135 Martinez Mountain Suite 322\nMillerland, PR 87715',121.85,1119.40,'Physical practice star apply dark.'),(18,19,'4890 Diaz Creek\nWalkerbury, SD 99212',96.14,2263.09,'Reveal current create wall subject theory any.'),(19,21,'6970 Chad Grove Suite 299\nEast Tamara, WI 48906',73.63,1714.23,'Standard year over owner cause cut child.'),(20,17,'63146 Hunt Ridge Suite 996\nSouth Kristinaview, AS 71341',158.97,1716.70,'Compare next who fund.'),(21,22,'9729 Michael Place\nHollytown, WI 60064',141.26,2231.06,'Key true throw.'),(22,11,'7508 Sarah Shoals Apt. 844\nEast Angela, ID 60574',148.68,1275.28,'Heavy newspaper day home coach kind these.'),(23,23,'576 Cruz Courts\nNorth Robertstad, MP 43118',74.56,1325.61,'Development so director address no.'),(24,1,'2737 Nicole Branch Apt. 145\nGreenville, CA 71664',186.61,1210.19,'Company protect reflect also morning national consider.'),(25,21,'886 Stephen Extension\nNorth Shawnside, TX 67578',137.10,2890.96,'Both hard operation into fine attorney.');
/*!40000 ALTER TABLE `allotments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `departments` (
  `Department_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Managers_Name` varchar(100) NOT NULL,
  `Email_Address` varchar(100) NOT NULL,
  `Mobile_Cell_Phone_Number` varchar(20) NOT NULL,
  `Other_Details` text,
  PRIMARY KEY (`Department_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'Alan Graham','nathan66@example.org','+63409984545','Film unit since everybody include rock you.'),(2,'James Reilly','trevinoandrew@example.org','+63135236779','Your break suggest machine act call.'),(3,'Brian Wang','grayrhonda@example.net','+63628603900','Sort leave Mr training take foreign painting.'),(4,'Juan Stewart','gtorres@example.org','+63281829184','Bill society this into law why source as.'),(5,'Alexander Harrison','armstrongamanda@example.org','+63406445826','Likely official if PM race.'),(6,'Sherry Hinton MD','dfowler@example.com','+63794879480','Poor under administration such.'),(7,'Robert Smith','gallen@example.org','+63851243210','Few operation computer husband cell attack once.'),(8,'Jesse Newman','andrewcruz@example.org','+63881063835','Environmental and new sound.'),(9,'Jessica Ford','george14@example.com','+63269367135','Gun late memory toward every drive.'),(10,'Gregory Daniels','adamsbarbara@example.net','+63282413207','Management whole matter.'),(11,'Emily Ingram','haynesadrian@example.net','+63215203641','Although director sense.'),(12,'Edward Hernandez','brianrowland@example.net','+63618006325','Attorney character standard since everybody that eat.'),(13,'Frank Hudson','stevenobrien@example.com','+63498540111','Floor hot nothing company number recently.'),(14,'Maria Jefferson','christophervincent@example.com','+63556809106','Environment modern range firm ago.'),(15,'Kristie Shaw','tammy61@example.org','+63457732064','Author treat choose recent final safe idea.'),(16,'Alan Nelson','rossbrandon@example.org','+63188899612','Couple song offer several policy.'),(17,'Jason Walls','ochapman@example.com','+63818152458','However sort fall medical wrong later interest.'),(18,'Nichole Rodriguez','kcoleman@example.net','+63922613884','Million space story.'),(19,'Mary King','francisrachel@example.net','+63456072933','Sister charge listen where large arrive.'),(20,'Vanessa Kelley','marquezjeffrey@example.com','+63898721835','Energy week technology sell firm police.'),(21,'Monique Young','johnsonsamantha@example.net','+63273063905','Box must alone better.'),(22,'Diane Taylor','jessica80@example.org','+63181858997','Either key series.'),(23,'Elizabeth Thompson','rickycampbell@example.net','+63336088906','Natural herself reflect discussion environmental.'),(24,'William Rogers','tylerwhite@example.com','+63005931866','Grow discuss listen.'),(25,'Tina Burke','jenniferdiaz@example.com','+63319593681','System court easy role.'),(26,'tester name','test@example.net','+63734527069','Test');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rentals`
--

DROP TABLE IF EXISTS `rentals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `rentals` (
  `Rental_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Allotment_ID` int(11) NOT NULL,
  `Resident_ID` int(11) NOT NULL,
  `Date_Rented_From` date DEFAULT NULL,
  `Date_Rented_To` date DEFAULT NULL,
  `Other_Details` text,
  PRIMARY KEY (`Rental_ID`),
  KEY `Allotment_ID` (`Allotment_ID`),
  KEY `Resident_ID` (`Resident_ID`),
  CONSTRAINT `rentals_ibfk_1` FOREIGN KEY (`Allotment_ID`) REFERENCES `allotments` (`allotment_id`) ON DELETE CASCADE,
  CONSTRAINT `rentals_ibfk_2` FOREIGN KEY (`Resident_ID`) REFERENCES `residents` (`resident_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rentals`
--

LOCK TABLES `rentals` WRITE;
/*!40000 ALTER TABLE `rentals` DISABLE KEYS */;
INSERT INTO `rentals` VALUES (1,20,15,'2024-04-20','2024-05-07','Represent who he.'),(2,13,21,'2024-09-22','2024-02-12','Seek during special project.'),(3,1,4,'2024-07-14','2024-10-21','Well product Congress chair material deal question.'),(4,1,19,'2024-03-20','2024-05-20','Building thus become.'),(5,7,24,'2024-02-01','2024-02-17','Common read simply per.'),(6,19,2,'2024-11-10','2024-09-30','Word chair money particular.'),(7,10,2,'2024-07-19','2024-09-14','Follow democratic company resource gas.'),(8,10,7,'2024-11-22','2024-06-03','Nor effect early leave address.'),(9,13,1,'2024-03-25','2024-10-30','Hand choice section.'),(10,8,22,'2024-11-26','2024-05-24','Yeah catch education both class only decision.'),(11,19,14,'2024-03-23','2024-02-18','Environment different down level spring success increase.'),(12,12,16,'2024-07-24','2024-09-11','Include city form save alone sing whether.'),(13,15,18,'2024-11-07','2024-01-03','Always research consider relate sound.'),(14,4,22,'2024-08-22','2024-02-15','Ability mouth scientist middle item rest.'),(15,25,9,'2024-11-07','2024-08-17','Available author use.'),(16,4,7,'2024-11-17','2024-05-20','Gas magazine outside play former.'),(17,19,3,'2024-10-11','2024-04-29','Pass represent appear far.'),(18,6,11,'2024-06-07','2024-07-11','Worker once or.'),(19,17,7,'2024-04-03','2024-05-31','Ahead team chance significant.'),(20,19,3,'2024-12-06','2024-08-11','Their start six alone without follow.'),(21,7,16,'2024-11-24','2024-08-25','Let prove quite.'),(22,14,15,'2024-11-11','2024-06-25','Person explain hand police control whole.'),(23,14,4,'2024-07-06','2024-01-13','Upon professor author hospital tell whatever large.'),(24,14,5,'2024-07-28','2024-01-31','Respond gun nothing development player herself least.'),(25,15,21,'2024-02-29','2024-08-11','Turn section trip window perhaps when.');
/*!40000 ALTER TABLE `rentals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `residents`
--

DROP TABLE IF EXISTS `residents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `residents` (
  `Resident_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Resident_Details` varchar(200) DEFAULT NULL,
  `Date_First_Registered` date DEFAULT NULL,
  `Date_Of_Birth` date DEFAULT NULL,
  `Gender` enum('Male','Female') DEFAULT NULL,
  `On_Waiting_List_YN` tinyint(1) DEFAULT NULL,
  `Other_Details` text,
  PRIMARY KEY (`Resident_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `residents`
--

LOCK TABLES `residents` WRITE;
/*!40000 ALTER TABLE `residents` DISABLE KEYS */;
INSERT INTO `residents` VALUES (1,'Amanda Watson','2023-06-02','1997-02-17','Male',1,'Believe field measure onto memory.'),(2,'Jacob Washington','2021-12-31','1998-11-02','Male',0,'Century ahead and tend.'),(3,'Yolanda Jennings','2022-01-04','1976-09-06','Female',0,'Necessary stay care task marriage itself into.'),(4,'Amanda Salazar','2024-10-03','1952-09-27','Male',1,'Their these artist bed book his.'),(5,'Renee Wilson','2020-07-09','1963-10-16','Male',1,'Science public though dinner.'),(6,'Brandi Jackson','2022-03-22','1943-07-02','Male',1,'Less I authority product local.'),(7,'Bryan Kline','2021-08-11','1938-08-18','Female',1,'Act any may enough later research.'),(8,'Vanessa Jennings','2020-08-16','1984-04-16','Female',1,'Particularly authority last notice.'),(9,'Dawn Stewart','2021-04-18','1971-02-10','Female',0,'Technology establish medical.'),(10,'Wayne Castillo','2020-01-28','1972-03-17','Female',1,'Piece baby short.'),(11,'Robyn Fuller','2024-02-05','1951-05-06','Male',1,'Allow table information should direction science second.'),(12,'Timothy Guerra','2022-08-09','1989-10-02','Male',1,'Power site board avoid.'),(13,'Curtis Ramirez','2022-10-17','1964-12-19','Male',1,'Agency set our scientist want.'),(14,'Lynn Hall','2022-03-24','1973-04-16','Male',1,'Risk baby interest traditional bring all be.'),(15,'Kelsey Keith','2022-07-07','1938-04-05','Male',1,'Oil big various there.'),(16,'Justin Campbell','2021-03-27','1940-02-16','Male',0,'Range hot still sister military fast thus argue.'),(17,'Samuel Jones','2021-07-09','1996-03-16','Male',1,'Him song wonder shake eight.'),(18,'Kristin Smith','2020-07-28','1963-05-14','Male',1,'Finish green security number office also.'),(19,'Christy Wallace','2021-03-26','1963-07-24','Female',1,'Hold look follow cause.'),(20,'Arthur Hansen','2020-05-25','1977-11-08','Male',0,'Watch four real woman.'),(21,'Tiffany Rose','2021-10-06','1937-05-04','Female',1,'Second century take.'),(22,'Nathan Anderson','2023-12-28','1945-09-11','Female',1,'Very make seat your their.'),(23,'Edward Marshall','2022-09-04','1979-03-14','Female',1,'Unit book executive.'),(24,'Craig Martin','2022-05-03','1942-01-06','Male',1,'Audience gun community almost eye under.'),(25,'Kelly Taylor','2021-12-12','1950-10-28','Male',0,'Minute during test price talk I draw.');
/*!40000 ALTER TABLE `residents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sites`
--

DROP TABLE IF EXISTS `sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `sites` (
  `Site_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Department_ID` int(11) NOT NULL,
  `Other_Details` text,
  PRIMARY KEY (`Site_ID`),
  KEY `Department_ID` (`Department_ID`),
  CONSTRAINT `sites_ibfk_1` FOREIGN KEY (`Department_ID`) REFERENCES `departments` (`department_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sites`
--

LOCK TABLES `sites` WRITE;
/*!40000 ALTER TABLE `sites` DISABLE KEYS */;
INSERT INTO `sites` VALUES (1,9,'Off assume they ball particular threat fly.'),(2,18,'Oil above wait learn.'),(3,22,'Institution check us different main certain country hair.'),(4,16,'Wind understand main mean meeting.'),(5,14,'Make ready item system.'),(6,19,'Although bar capital near me person case material.'),(7,24,'Time success check purpose son director.'),(8,9,'Phone improve expect institution sea training fall.'),(9,15,'Set someone out mind bed physical.'),(10,13,'Old way everybody language seven.'),(11,19,'Put generation old usually.'),(12,7,'Animal manager prove design until expert.'),(13,9,'Method choose tell area candidate somebody first face.'),(14,7,'Run crime address on past daughter.'),(15,3,'Lose mention she program.'),(16,15,'Long report fire person page place color.'),(17,17,'Huge exactly inside every find someone.'),(18,24,'Once stay close worker ability.'),(19,13,'Along no world improve.'),(20,4,'Fine table big generation.'),(21,20,'Allow structure choose sort lay agreement.'),(22,5,'Democrat somebody over south stuff both.'),(23,14,'Population out without word special.'),(24,5,'While its continue region.'),(25,15,'Seat number statement give throw difficult.'),(26,24,'Sample update.'),(27,1,NULL);
/*!40000 ALTER TABLE `sites` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-14 11:01:09
