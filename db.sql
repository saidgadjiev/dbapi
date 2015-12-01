CREATE SCHEMA IF NOT EXISTS `forumdb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `forumdb`;

-- -----------------------------------------------------
-- Table `forumdb`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`user` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`user` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NULL,
  `email` VARCHAR(255) NOT NULL,
  `isAnonymous` TINYINT(1) UNSIGNED NULL DEFAULT 0,
  `about` TEXT NULL,
  `name` VARCHAR(255) NULL,
  PRIMARY KEY (`id`, `email`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  INDEX `reverse` (`email` ASC, `id` ASC),
  UNIQUE INDEX `id_desc` (`id` DESC, `email` ASC),
  INDEX `reverse_desc` (`email` ASC, `id` DESC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`forum`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`forum` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`forum` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(145) NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  `short_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`, `name`, `short_name`),
  INDEX `fk_Forums_Users1_idx` (`user` ASC),
  UNIQUE INDEX `short_name_UNIQUE` (`short_name` ASC, `id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`thread`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`thread` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`thread` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(145) NOT NULL,
  `date` DATETIME NOT NULL,
  `message` TEXT NOT NULL,
  `forum` VARCHAR(45) NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  `isDeleted` TINYINT NOT NULL DEFAULT 0,
  `isClosed` TINYINT NOT NULL DEFAULT 0,
  `slug` VARCHAR(65) NOT NULL,
  `likes` INT UNSIGNED NOT NULL DEFAULT 0,
  `dislikes` INT UNSIGNED NOT NULL DEFAULT 0,
  `points` INT NOT NULL DEFAULT 0,
  `posts` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`, `user`, `forum`),
  INDEX `fk_Threads_Forums1_idx` (`forum` ASC),
  INDEX `fk_Threads_Users1_idx` (`user` ASC),
  INDEX `date_order` (`date` ASC, `id` ASC),
  INDEX `date_order_rev` (`date` DESC, `id` ASC))
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
  `user` VARCHAR(45) NOT NULL,
  `parent` INT UNSIGNED NULL,
  `isApproved` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `isDeleted` TINYINT NOT NULL DEFAULT 0,
  `isEdited` TINYINT NOT NULL DEFAULT 0,
  `isSpam` TINYINT NOT NULL DEFAULT 0,
  `isHighlighted` TINYINT NOT NULL DEFAULT 0,
  `forum` VARCHAR(45) NOT NULL,
  `likes` INT UNSIGNED NOT NULL DEFAULT 0,
  `dislikes` INT UNSIGNED NOT NULL DEFAULT 0,
  `points` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`, `thread`, `user`, `forum`),
  INDEX `fk_Posts_Threads1_idx` (`thread` ASC),
  INDEX `fk_Posts_Users1_idx` (`user` ASC),
  INDEX `fk_Posts_Posts1_idx` (`parent` ASC),
  INDEX `fk_Posts_Forums1_idx` (`forum` ASC),
  INDEX `date_ordering` (`date` DESC, `id` ASC),
  INDEX `date_order_rev` (`date` DESC, `id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `forumdb`.`subscription`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `forumdb`.`subscription` ;

CREATE TABLE IF NOT EXISTS `forumdb`.`subscription` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user` VARCHAR(45) NOT NULL,
  `thread` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_Subscriprions_Users1_idx` (`user` ASC),
  INDEX `fk_Subscriprions_Threads1_idx` (`thread` ASC),
  UNIQUE INDEX `subscription` (`user` ASC, `thread` ASC))
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
  UNIQUE INDEX `main` (`follower`, `followee`))
ENGINE = InnoDB;
