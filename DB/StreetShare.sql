CREATE DATABASE IF NOT EXISTS `streetshare`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `streetshare`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `transactions`;
DROP TABLE IF EXISTS `requests`;
DROP TABLE IF EXISTS `tools`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `roles`;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_roles_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) DEFAULT NULL,
  `last_name` VARCHAR(255) DEFAULT NULL,
  `display_name` VARCHAR(255) DEFAULT NULL,
  `hashed_pw` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) DEFAULT NULL,
  `phone` VARCHAR(255) DEFAULT NULL,
  `street` VARCHAR(255) DEFAULT NULL,
  `house_nr` VARCHAR(50) DEFAULT NULL,
  `zip` VARCHAR(50) DEFAULT NULL,
  `role_id` INT DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `city` VARCHAR(50) DEFAULT NULL,
  `country` VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_users_email` (`email`),
  UNIQUE KEY `uk_users_display_name` (`display_name`),
  KEY `idx_users_role_id` (`role_id`),
  CONSTRAINT `fk_users_role`
    FOREIGN KEY (`role_id`)
    REFERENCES `roles` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `tools` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` VARCHAR(500) NOT NULL,
  `base_price` DECIMAL(10,2) DEFAULT NULL,
  `deposit` DECIMAL(10,2) DEFAULT NULL,
  `tool_condition` VARCHAR(255) DEFAULT NULL,
  `tool_image` MEDIUMBLOB NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` INT DEFAULT NULL,
  `deleted` INT NOT NULL DEFAULT 0,
  `deleted_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tools_created_by` (`created_by`),
  CONSTRAINT `fk_tools_creator`
    FOREIGN KEY (`created_by`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `requests` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tool_id` INT DEFAULT NULL,
  `borrower_id` INT DEFAULT NULL,
  `to_respond_id` INT DEFAULT NULL,
  `lender_id` INT DEFAULT NULL,
  `start_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `message` TEXT NOT NULL,
  `status` VARCHAR(50) NOT NULL DEFAULT 'Ausstehend',
  PRIMARY KEY (`id`),
  KEY `idx_requests_tool_id` (`tool_id`),
  KEY `idx_requests_borrower_id` (`borrower_id`),
  KEY `idx_requests_to_respond_id` (`to_respond_id`),
  KEY `idx_requests_lender_id` (`lender_id`),
  CONSTRAINT `fk_requests_tool`
    FOREIGN KEY (`tool_id`)
    REFERENCES `tools` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_requests_borrower`
    FOREIGN KEY (`borrower_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_requests_to_respond`
    FOREIGN KEY (`to_respond_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_requests_lender`
    FOREIGN KEY (`lender_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `transactions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tool_id` INT DEFAULT NULL,
  `request_id` INT DEFAULT NULL,
  `borrower_id` INT DEFAULT NULL,
  `lender_id` INT DEFAULT NULL,
  `start_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `picture_before` BLOB DEFAULT NULL,
  `picture_after` BLOB DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_transactions_request_id` (`request_id`),
  KEY `idx_transactions_tool_id` (`tool_id`),
  KEY `idx_transactions_borrower_id` (`borrower_id`),
  KEY `idx_transactions_lender_id` (`lender_id`),
  CONSTRAINT `fk_transactions_tool`
    FOREIGN KEY (`tool_id`)
    REFERENCES `tools` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_transactions_request`
    FOREIGN KEY (`request_id`)
    REFERENCES `requests` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_transactions_borrower`
    FOREIGN KEY (`borrower_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL,
  CONSTRAINT `fk_transactions_lender`
    FOREIGN KEY (`lender_id`)
    REFERENCES `users` (`id`)
    ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `roles` (`id`, `name`) VALUES
  (1, 'Admin'),
  (2, 'User');

-- Default admin credentials match docker-compose.yml:
-- email: admin@streetshare.at
-- display_name: admin
-- password: admin123
INSERT INTO `users` (
  `id`,
  `first_name`,
  `last_name`,
  `display_name`,
  `hashed_pw`,
  `email`,
  `phone`,
  `street`,
  `house_nr`,
  `zip`,
  `role_id`,
  `city`,
  `country`
) VALUES (
  1,
  'StreetShare',
  'Admin',
  'admin',
  '$2b$12$piiNNwLsWCKt8K4stqd/ResDRBBo/GoYMFJHUIYUjwYwZDs9Yj9rK',
  'admin@streetshare.at',
  '+4366011111111',
  'Adminhausen',
  '1',
  '8000',
  1,
  'Admin',
  'Österreich'
);
