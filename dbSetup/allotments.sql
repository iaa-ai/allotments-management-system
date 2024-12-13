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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `allotments`
--

LOCK TABLES `allotments` WRITE;
/*!40000 ALTER TABLE `allotments` DISABLE KEYS */;
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
  `Email_Address` varchar(100) DEFAULT NULL,
  `Mobile_Cell_Phone_Number` varchar(20) DEFAULT NULL,
  `Other_Details` text,
  PRIMARY KEY (`Department_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rentals`
--

LOCK TABLES `rentals` WRITE;
/*!40000 ALTER TABLE `rentals` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `residents`
--

LOCK TABLES `residents` WRITE;
/*!40000 ALTER TABLE `residents` DISABLE KEYS */;
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
  `Managers_Name` varchar(100) DEFAULT NULL,
  `Mobile_Cell_Phone_Number` varchar(20) DEFAULT NULL,
  `Other_Details` text,
  PRIMARY KEY (`Site_ID`),
  KEY `Department_ID` (`Department_ID`),
  CONSTRAINT `sites_ibfk_1` FOREIGN KEY (`Department_ID`) REFERENCES `departments` (`department_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sites`
--

LOCK TABLES `sites` WRITE;
/*!40000 ALTER TABLE `sites` DISABLE KEYS */;
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

-- Dump completed on 2024-12-13 12:19:31
