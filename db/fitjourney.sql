-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 03, 2024 at 07:06 AM
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
-- Database: `fitjourney`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(60) NOT NULL,
  `admin_username` varchar(60) NOT NULL,
  `admin_password` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_name`, `admin_username`, `admin_password`) VALUES
(1, 'Inco John benedict', 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `exercise_types`
--

CREATE TABLE `exercise_types` (
  `id` int(11) NOT NULL,
  `workout_type_id` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `exercise_types`
--

INSERT INTO `exercise_types` (`id`, `workout_type_id`, `name`) VALUES
(1, 1, 'Bench Press'),
(2, 1, 'Push-ups'),
(3, 1, 'Chest Fly'),
(4, 1, 'Incline Press'),
(5, 2, 'Pull-ups'),
(6, 2, 'Deadlifts'),
(7, 2, 'Lat Pulldowns'),
(8, 2, 'Rows'),
(9, 3, 'Squats'),
(10, 3, 'Leg Press'),
(11, 5, 'Lunges'),
(12, 3, 'Leg Curls'),
(13, 4, 'Bicep Curls'),
(14, 4, 'Tricep Dips'),
(15, 4, 'Barbell Curl'),
(16, 4, 'Hammer Curl'),
(17, 5, 'Running'),
(18, 5, 'Cycling'),
(19, 5, 'Swimming'),
(20, 5, 'Jump Rope');

-- --------------------------------------------------------

--
-- Table structure for table `logs`
--

CREATE TABLE `logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `date_logged` datetime DEFAULT current_timestamp(),
  `workout_type` varchar(50) NOT NULL,
  `exercise_type` varchar(100) NOT NULL,
  `duration` float NOT NULL,
  `calories` float NOT NULL,
  `fitness_goal` varchar(255) DEFAULT NULL,
  `weight` float NOT NULL,
  `height` float NOT NULL,
  `reps` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `logs`
--

INSERT INTO `logs` (`id`, `user_id`, `date_logged`, `workout_type`, `exercise_type`, `duration`, `calories`, `fitness_goal`, `weight`, `height`, `reps`) VALUES
(3, 1, '2024-11-21 13:03:41', 'Back', 'Deadlifts', 20, 162, 'Stay Fit', 50, 170, 20),
(4, 1, '2024-11-21 13:04:57', 'Back', 'Deadlifts', 20, 162, 'Stay Fit', 49, 170, 20),
(11, 3, '2024-12-03 14:02:56', 'Legs', 'Leg Curls', 5, 35.5, 'Build Muscle', 5, 5, 5),
(12, 3, '2024-12-03 14:03:27', 'Arms', 'Barbell Curl', 6, 30.6, 'Build Muscle', 7, 8, 6);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'juan', 'juan'),
(3, 'joshua', 'joshua'),
(7, 'spiderman', 'superman'),
(8, 'chacka', 'chacka');

-- --------------------------------------------------------

--
-- Table structure for table `workout_types`
--

CREATE TABLE `workout_types` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `workout_types`
--

INSERT INTO `workout_types` (`id`, `name`) VALUES
(1, 'Chest'),
(2, 'Back to back'),
(3, 'Legs'),
(4, 'Arms'),
(5, 'Cardio');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `exercise_types`
--
ALTER TABLE `exercise_types`
  ADD PRIMARY KEY (`id`),
  ADD KEY `exercise_types_ibfk_1` (`workout_type_id`);

--
-- Indexes for table `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `workout_types`
--
ALTER TABLE `workout_types`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `exercise_types`
--
ALTER TABLE `exercise_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `logs`
--
ALTER TABLE `logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `workout_types`
--
ALTER TABLE `workout_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `exercise_types`
--
ALTER TABLE `exercise_types`
  ADD CONSTRAINT `exercise_types_ibfk_1` FOREIGN KEY (`workout_type_id`) REFERENCES `workout_types` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `logs`
--
ALTER TABLE `logs`
  ADD CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
