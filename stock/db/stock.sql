/*
 Navicat MySQL Data Transfer

 Source Server         : stock
 Source Server Type    : MySQL
 Source Server Version : 80025
 Source Host           : localhost:3306
 Source Schema         : stock

 Target Server Type    : MySQL
 Target Server Version : 80025
 File Encoding         : 65001

 Date: 19/07/2021 00:52:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for plate_stocks
-- ----------------------------
DROP TABLE IF EXISTS `plate_stocks`;
CREATE TABLE `plate_stocks`  (
  `id` bigint NOT NULL,
  `plate_stock_id` bigint NULL DEFAULT NULL,
  `stock_id` bigint NULL DEFAULT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for stock_info
-- ----------------------------
DROP TABLE IF EXISTS `stock_info`;
CREATE TABLE `stock_info`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for stock_price
-- ----------------------------
DROP TABLE IF EXISTS `stock_price`;
CREATE TABLE `stock_price`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `stock_info_id` bigint NULL DEFAULT NULL,
  `time_key` datetime(0) NULL DEFAULT NULL,
  `open_price` decimal(10, 2) NULL DEFAULT NULL,
  `close_price` decimal(10, 2) NULL DEFAULT NULL,
  `high_price` decimal(10, 2) NULL DEFAULT NULL,
  `low_price` decimal(10, 2) NULL DEFAULT NULL,
  `pe_ratio` decimal(10, 2) NULL DEFAULT NULL,
  `turnover_rate` decimal(10, 2) NULL DEFAULT NULL,
  `volume` bigint NULL DEFAULT NULL,
  `turnover` decimal(10, 2) NULL DEFAULT NULL,
  `change_rate` decimal(10, 2) NULL DEFAULT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for stock_relative
-- ----------------------------
DROP TABLE IF EXISTS `stock_relative`;
CREATE TABLE `stock_relative`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `stock_info_id_from` bigint NULL DEFAULT NULL,
  `stock_info_id_to` bigint NULL DEFAULT NULL,
  `relative_strong` decimal(10, 2) NULL DEFAULT NULL,
  `key_time` datetime(0) NULL DEFAULT NULL,
  `create_time` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
