-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 10, 2024 at 08:32 AM
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
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'E-mail of admin account.',
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'Password of admin account.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`admin_id`, `last_name`, `first_name`, `middle_name`, `name_suffix`, `email`, `password`) VALUES
(3, 'Admin', 'CDRRMO', NULL, NULL, 'admin@cdrrmo.com', '$2b$12$f.g/WgSBWFaiCqTM8CnlJ.neGyJKDpDrTc2VJ7E1csyicXXffVm7.');

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
  `cluster_distance` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`report_id`, `date_time`, `name`, `phone_number`, `location`, `latitude`, `longitude`, `estimate_victims`, `report_details`, `pictures`, `status_id`, `category_id`, `responder_report`, `cluster_distance`) VALUES
(3, '2024-05-10 00:26:01', 'Pasasadaba, Brian Cyber R.', '0949-593-1396', 'San Isidro Heights, Banlic, Cabuyao, Laguna', 14.23554500, 121.13740000, 3, 'Several family members fainted due to heatstroke, pls send help', NULL, 1, 1, NULL, NULL),
(5, '2024-05-10 12:27:13', 'Pasasadaba Brian Cyber R', '0949-593-1396', 'San Isidro Heights, Banlic, Cabuyao, Laguna', 14.23554500, 121.13740000, 21, 'my mother slipped and fell on the floor, she is bleeding and unresponsive please send help', NULL, 1, 1, NULL, NULL),
(6, '2024-05-10 12:32:44', 'Pasasadaba Brian Cyber R', '0949-593-1396', 'San Isidro Heights, Banlic, Cabuyao, Laguna', 14.23554500, 121.13740000, 3, 'there is a fire in the neighborhood, some people are still trapped send help immediately', NULL, 1, 3, NULL, NULL),
(7, '2024-05-10 12:37:12', 'Juan Reyes', '0912-345-6789', 'San Isidro Heights, Banlic, Cabuyao, Laguna', 14.23564700, 121.13735200, 4, 'a car got into a collision with a motorbike here, send responders', NULL, 1, 1, NULL, NULL),
(9, '2024-05-10 14:01:59', 'John R Doe', '0949-593-1396', 'San Isidro Heights, Banlic, Cabuyao, Laguna', 14.23554500, 121.13740000, 1, 'my brother is tripped and fell, his head is now bleeding profusely, we need an ambulance', NULL, 1, 1, NULL, NULL);

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
  MODIFY `report_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

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
