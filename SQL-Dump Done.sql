-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: smartwarehousejr
-- ------------------------------------------------------
-- Server version	8.0.31

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
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `location` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `zone` varchar(50) NOT NULL,
  `shelf` varchar(50) NOT NULL,
  `aisle` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `zone` (`zone`,`shelf`,`aisle`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` VALUES (1,'A','1','1'),(2,'A','1','2'),(3,'A','2','1'),(4,'B','1','1'),(5,'B','1','2');
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pickorderitems`
--

DROP TABLE IF EXISTS `pickorderitems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pickorderitems` (
  `pickOrd_ID` int NOT NULL,
  `product_ID` int NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`pickOrd_ID`,`product_ID`),
  KEY `product_ID` (`product_ID`),
  CONSTRAINT `pickorderitems_ibfk_1` FOREIGN KEY (`pickOrd_ID`) REFERENCES `pickorders` (`pickOrd_ID`),
  CONSTRAINT `pickorderitems_ibfk_2` FOREIGN KEY (`product_ID`) REFERENCES `products` (`product_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pickorderitems`
--

LOCK TABLES `pickorderitems` WRITE;
/*!40000 ALTER TABLE `pickorderitems` DISABLE KEYS */;
INSERT INTO `pickorderitems` VALUES (1,1,10),(1,3,50),(2,2,5),(2,4,2),(3,5,100),(4,1,5);
/*!40000 ALTER TABLE `pickorderitems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pickorders`
--

DROP TABLE IF EXISTS `pickorders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pickorders` (
  `pickOrd_ID` int NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_ID` int DEFAULT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'Created',
  `priority` varchar(20) NOT NULL,
  PRIMARY KEY (`pickOrd_ID`),
  KEY `user_ID` (`user_ID`),
  CONSTRAINT `pickorders_ibfk_1` FOREIGN KEY (`user_ID`) REFERENCES `users` (`user_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pickorders`
--

LOCK TABLES `pickorders` WRITE;
/*!40000 ALTER TABLE `pickorders` DISABLE KEYS */;
INSERT INTO `pickorders` VALUES (1,'2026-03-06 12:53:22',1,'Done','High'),(2,'2026-03-06 12:53:22',2,'In Progress','Medium'),(3,'2026-03-06 12:53:22',3,'Created','Low'),(4,'2026-03-06 12:53:22',1,'Created','High');
/*!40000 ALTER TABLE `pickorders` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_user_before_insert` BEFORE INSERT ON `pickorders` FOR EACH ROW BEGIN
    DECLARE v_user_id INT;
    
    -- If no user is assigned when creating the order
    IF NEW.user_ID IS NULL THEN
		-- Select the user with the fewest non-completed orders
        SELECT u.user_ID
        INTO v_user_id
        FROM Users u
        LEFT JOIN PickOrders po
            ON po.user_ID = u.user_ID
            AND po.status <> 'Done'
        GROUP BY u.user_ID
        ORDER BY COUNT(po.pickOrd_ID) ASC
        LIMIT 1;
        
        -- Assign that user to the new order
        SET NEW.user_ID = v_user_id;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_ID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `article_num` varchar(20) NOT NULL,
  `type` varchar(50) NOT NULL,
  `stock_quantity` int NOT NULL DEFAULT '0',
  `location_ID` int NOT NULL,
  PRIMARY KEY (`product_ID`),
  UNIQUE KEY `article_num` (`article_num`),
  KEY `location_ID` (`location_ID`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`location_ID`) REFERENCES `location` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Screwdriver','ART001','Tool',50,1),(2,'Hammer','ART002','Tool',20,2),(3,'Nails','ART003','Hardware',200,3),(4,'Drill','ART004','Tool',3,4),(5,'Screws','ART005','Hardware',2,5);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_ID` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(50) NOT NULL,
  `lastname` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`user_ID`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'John','Smith','john.smith@email.com'),(2,'Emily','Johnson','emily.j@email.com'),(3,'Michael','Brown','michael.b@email.com');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'smartwarehousejr'
--

--
-- Dumping routines for database 'smartwarehousejr'
--
/*!50003 DROP FUNCTION IF EXISTS `product_stock` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `product_stock`(p_product_id INT) RETURNS int
    READS SQL DATA
    DETERMINISTIC
BEGIN
	DECLARE v_stock INT;
    
    -- Retrieve stock_quantity for the given product ID
    SELECT stock_quantity
    INTO v_stock
    FROM Products
    WHERE product_ID = p_product_id;
    
    -- Return the stock value, or 0 if NULL
    RETURN IFNULL(v_stock, 0);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-06 12:59:36
