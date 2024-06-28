-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 28, 2024 at 01:35 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cdrrmo`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `admin_id` int(11) NOT NULL COMMENT 'Unique id number for admin accounts.',
  `last_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Last name of admin.',
  `first_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'First name of admin.',
  `middle_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Middle name of admin.',
  `name_suffix` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'Name suffixes (e.g. Jr., Sr., and II).',
  `employee_id` varchar(13) DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'E-mail of admin account.',
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'Password of admin account.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`admin_id`, `last_name`, `first_name`, `middle_name`, `name_suffix`, `employee_id`, `email`, `password`) VALUES
(3, 'Admin', 'CDRRMO', NULL, NULL, 'CDRRMO-ADM-01', 'admin@cdrrmo.com', '$2b$12$f.g/WgSBWFaiCqTM8CnlJ.neGyJKDpDrTc2VJ7E1csyicXXffVm7.');

-- --------------------------------------------------------

--
-- Table structure for table `admin_report`
--

CREATE TABLE `admin_report` (
  `admin_id` int(11) NOT NULL,
  `report_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `category_id` int(11) NOT NULL,
  `categories` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`category_id`, `categories`) VALUES
(1, 'Medical Emergency'),
(2, 'Vehicular Accident'),
(3, 'Other Emergency');

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `report_id` int(11) NOT NULL,
  `date_time` datetime NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(13) NOT NULL,
  `location` varchar(255) NOT NULL,
  `latitude` decimal(11,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `estimate_victims` int(11) NOT NULL,
  `report_details` text NOT NULL,
  `pictures` varchar(255) DEFAULT NULL,
  `status_id` int(11) DEFAULT 1,
  `category_id` int(11) DEFAULT NULL,
  `responder_report` varchar(255) DEFAULT NULL,
  `cluster` tinyint(1) DEFAULT NULL,
  `cluster_distance` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`report_id`, `date_time`, `name`, `phone_number`, `location`, `latitude`, `longitude`, `estimate_victims`, `report_details`, `pictures`, `status_id`, `category_id`, `responder_report`, `cluster`, `cluster_distance`) VALUES
(28, '2024-06-28 09:44:10', 'Brian', '09284562914', 'Blk20 Lot46 Ph2 San Isidro Heights, Banlic, Cabuyao', 0.00000000, 0.00000000, 1, 'May mga kotseng nagbanggaan dito, sugatan yung mga pasahero', '/uploads/image_1719538983.jpeg', 3, 1, '', 0, 0.997154),
(29, '2024-06-28 14:48:53', 'Ae', '09993481154', 'CDRRMO', 14.27759450, 121.12403150, 3, 'thx sa libre po', '/uploads/image_1719557324.jpeg', 1, 3, NULL, 0, 0.156994),
(30, '2024-06-28 14:55:34', 'Ax ', '09263838373', 'CDRRMO', 14.27746840, 121.12410090, 3, 'presentation naaaa', '/uploads/image_1719557727.jpeg', 1, 2, NULL, 0, 0.156994),
(31, '2024-06-28 14:56:02', '', '09348739244', 'Cabuyao, Laguna', 14.27747030, 121.12412170, 3, 'May sunog po Dito tulong ', '/uploads/image_1719557743.jpeg', 1, 3, NULL, 0, 0.970598),
(32, '2024-06-28 14:57:06', 'Leo', '09753125100', 'Sitio', 14.27747030, 121.12412170, 3, 'May nasusunog send ng medic', '/uploads/image_1719557813.jpeg', 1, 2, NULL, 1, 0.992105),
(33, '2024-06-28 14:57:49', 'Axel', '09727272828', 'CDRRMO', 14.27746740, 121.12412640, 6, 'may nasagasaan dito, pasend ng medic', '/uploads/image_1719557848.jpeg', 1, 2, NULL, 0, 1.00262),
(34, '2024-06-28 14:57:57', 'Joe Mama', '09753125140', 'Cabuyao City, laguna', 14.27747030, 121.12412170, 1, 'My head is bleeding there\'s no one here send ambulance please', '/uploads/image_1719557856.jpeg', 1, 1, NULL, 1, 0.946837),
(35, '2024-06-28 15:41:52', 'Colin', '09171630653', 'Cabuyao City Hall', 0.00000000, 0.00000000, 1, 'A', '/uploads/image_1719560499.jpeg', 1, 2, NULL, 0, 0.156994);

-- --------------------------------------------------------

--
-- Table structure for table `status`
--

CREATE TABLE `status` (
  `status_id` int(11) NOT NULL,
  `report_status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `status`
--

INSERT INTO `status` (`status_id`, `report_status`) VALUES
(1, 'Pending'),
(2, 'Ongoing'),
(3, 'Resolved');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `admin_report`
--
ALTER TABLE `admin_report`
  ADD PRIMARY KEY (`admin_id`,`report_id`),
  ADD KEY `report_id` (`report_id`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`report_id`),
  ADD KEY `fk_status_id` (`status_id`),
  ADD KEY `fk_category_id` (`category_id`);

--
-- Indexes for table `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`status_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unique id number for admin accounts.', AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `report_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `status`
--
ALTER TABLE `status`
  MODIFY `status_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin_report`
--
ALTER TABLE `admin_report`
  ADD CONSTRAINT `admin_report_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admins` (`admin_id`),
  ADD CONSTRAINT `admin_report_ibfk_2` FOREIGN KEY (`report_id`) REFERENCES `reports` (`report_id`);

--
-- Constraints for table `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `fk_category_id` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`),
  ADD CONSTRAINT `fk_status_id` FOREIGN KEY (`status_id`) REFERENCES `status` (`status_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
