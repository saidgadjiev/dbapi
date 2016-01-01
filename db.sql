CREATE SCHEMA IF NOT EXISTS `forumdb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `forumdb`;

-- -----------------------------------------------------
-- Table `forumdb`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`user` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`user` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(32) NULL,
  `email` VARCHAR(32) NOT NULL,
  `isAnonymous` TINYINT(1) UNSIGNED NULL DEFAULT 0,
  `about` TEXT NULL,
  `name` VARCHAR(30) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`email`),
  KEY name_email (name, email),
  KEY email_name (email, name))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`forum`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`forum` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`forum` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(64) NOT NULL,
  `user` VARCHAR(32) NOT NULL,
  `short_name` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`short_name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`thread`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`thread` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`thread` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(64) NOT NULL,
  `date` DATETIME NOT NULL,
  `message` TEXT NOT NULL,
  `forum` VARCHAR(64) NOT NULL,
  `user` VARCHAR(32) NOT NULL,
  `isDeleted` TINYINT NOT NULL DEFAULT 0,
  `isClosed` TINYINT NOT NULL DEFAULT 0,
  `slug` VARCHAR(64) NOT NULL,
  `likes` INT UNSIGNED NOT NULL DEFAULT 0,
  `dislikes` INT UNSIGNED NOT NULL DEFAULT 0,
  `points` INT NOT NULL DEFAULT 0,
  `posts` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY user_date (`user`,`date`),
  KEY (`slug`),
  KEY forum_date (`forum`,`date`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`post`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`post` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`post` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `message` TEXT NOT NULL,
  `date` DATETIME NOT NULL,
  `thread` INT UNSIGNED NOT NULL,
  `user` VARCHAR(32) NOT NULL,
  `parent` INT UNSIGNED NULL,
  `isApproved` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `isDeleted` TINYINT NOT NULL DEFAULT 0,
  `isEdited` TINYINT NOT NULL DEFAULT 0,
  `isSpam` TINYINT NOT NULL DEFAULT 0,
  `isHighlighted` TINYINT NOT NULL DEFAULT 0,
  `forum` VARCHAR(64) NOT NULL,
  `likes` INT UNSIGNED NOT NULL DEFAULT 0,
  `dislikes` INT UNSIGNED NOT NULL DEFAULT 0,
  `points` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `user_date` (`user`, `date`),
  KEY `thread_date` (`thread`,`date`),
  KEY `forum_user` (`forum`, `user`),
  KEY `forum_date` (`forum`, `date`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`subscription`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`subscription` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`subscription` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user` VARCHAR(32) NOT NULL,
  `thread` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_thread` (`user`, `thread`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`follower`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`follower` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`follower` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `follower` VARCHAR(45) NOT NULL,
  `followee` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY(`follower`),
  KEY(`followee`),
  UNIQUE KEY `f_f` (`follower`, `followee`))
ENGINE = InnoDB;