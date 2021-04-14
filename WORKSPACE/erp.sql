-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema erp
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema erp
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `erp` DEFAULT CHARACTER SET utf8mb4 ;
USE `erp` ;

-- -----------------------------------------------------
-- Table `erp`.`analysis_config`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`analysis_config` (
  `analysis_config_id` INT(11) NOT NULL AUTO_INCREMENT,
  `config_name` VARCHAR(100) NOT NULL,
  `config_value` TEXT NOT NULL,
  `updated_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `updated_by` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`analysis_config_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`eng_level`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`eng_level` (
  `eng_level_id` INT(11) NOT NULL AUTO_INCREMENT,
  `level` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`eng_level_id`),
  UNIQUE INDEX `level_UNIQUE` (`level` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`eng_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`eng_type` (
  `eng_type_id` INT(11) NOT NULL AUTO_INCREMENT,
  `eng_type_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`eng_type_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`final_date`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`final_date` (
  `final_date_id` INT(11) NOT NULL AUTO_INCREMENT,
  `date` DATETIME NOT NULL,
  `updated_date` DATETIME NOT NULL,
  `updated_by` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`final_date_id`),
  UNIQUE INDEX `date_UNIQUE` (`date` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`holiday`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`holiday` (
  `holiday_id` INT(11) NOT NULL AUTO_INCREMENT,
  `date` DATETIME NOT NULL,
  PRIMARY KEY (`holiday_id`),
  UNIQUE INDEX `date_UNIQUE` (`date` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`sheet_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`sheet_type` (
  `sheet_type_id` INT(11) NOT NULL AUTO_INCREMENT,
  `sheet_type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`sheet_type_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`sheet`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`sheet` (
  `sheet_id` INT(11) NOT NULL AUTO_INCREMENT,
  `sheet_type_id` INT(11) NOT NULL,
  `sheet_name` VARCHAR(100) NOT NULL,
  `latest_modified` DATETIME NOT NULL,
  `updated_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  `updated_by` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`sheet_id`),
  UNIQUE INDEX `sheet_name_UNIQUE` (`sheet_name` ASC) ,
  INDEX `sheet_type_id_idx` (`sheet_type_id` ASC) ,
  CONSTRAINT `sheet_type_id`
    FOREIGN KEY (`sheet_type_id`)
    REFERENCES `erp`.`sheet_type` (`sheet_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`log` (
  `log_id` INT(11) NOT NULL AUTO_INCREMENT,
  `sheet_id` INT(11) NOT NULL,
  `old_value` MEDIUMTEXT NULL DEFAULT NULL,
  `new_value` MEDIUMTEXT NULL DEFAULT NULL,
  `updated_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  `updated_by` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`log_id`),
  INDEX `log_sheet_id_idx` (`sheet_id` ASC) ,
  CONSTRAINT `log_sheet_id`
    FOREIGN KEY (`sheet_id`)
    REFERENCES `erp`.`sheet` (`sheet_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`team`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`team` (
  `team_id` INT(11) NOT NULL AUTO_INCREMENT,
  `team_name` VARCHAR(45) NOT NULL,
  `team_lead_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`team_id`),
  UNIQUE INDEX `name_UNIQUE` (`team_name` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`user` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(45) NOT NULL,
  `full_name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `other_name` VARCHAR(200) NULL DEFAULT NULL,
  `is_active` INT(11) NOT NULL,
  `updated_by` VARCHAR(45) NOT NULL,
  `updated_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `eng_level_id` INT(11) NULL DEFAULT NULL,
  `eng_type_id` INT(11) NULL DEFAULT NULL,
  `team_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) ,
  UNIQUE INDEX `user_name_UNIQUE` (`user_name` ASC) ,
  INDEX `user_eng_level_id_idx` (`eng_level_id` ASC) ,
  INDEX `user_eng_type_id_idx` (`eng_type_id` ASC) ,
  INDEX `user_team_id_idx` (`team_id` ASC) ,
  CONSTRAINT `user_eng_level_id`
    FOREIGN KEY (`eng_level_id`)
    REFERENCES `erp`.`eng_level` (`eng_level_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user_eng_type_id`
    FOREIGN KEY (`eng_type_id`)
    REFERENCES `erp`.`eng_type` (`eng_type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user_team_id`
    FOREIGN KEY (`team_id`)
    REFERENCES `erp`.`team` (`team_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`project_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`project_user` (
  `project_user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `sheet_id` INT(11) NULL DEFAULT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`project_user_id`),
  INDEX `project_sheet_id_idx` (`sheet_id` ASC) ,
  INDEX `project_user_idx_idx` (`user_id` ASC) ,
  CONSTRAINT `project_sheet_id`
    FOREIGN KEY (`sheet_id`)
    REFERENCES `erp`.`sheet` (`sheet_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `project_user_idx`
    FOREIGN KEY (`user_id`)
    REFERENCES `erp`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`task`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`task` (
  `task_id` INT(11) NOT NULL AUTO_INCREMENT,
  `sheet_id` INT(11) NOT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  `sibling_id` INT(11) NULL DEFAULT NULL,
  `parent_id` INT(11) NULL DEFAULT NULL,
  `self_id` INT(11) NOT NULL,
  `task_name` TEXT NOT NULL,
  `date` DATETIME NULL DEFAULT NULL,
  `start_date` DATETIME NULL DEFAULT NULL,
  `end_date` DATETIME NULL DEFAULT NULL,
  `duration` VARCHAR(45) NULL DEFAULT NULL,
  `complete` INT(11) NULL DEFAULT NULL,
  `predecessors` INT(11) NULL DEFAULT NULL,
  `comment` TEXT NULL DEFAULT NULL,
  `actual_end_date` DATETIME NULL DEFAULT NULL,
  `status` TEXT NULL DEFAULT NULL,
  `is_children` TINYINT(4) NOT NULL,
  `allocation` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`task_id`),
  INDEX `task_sheet_id_idx` (`sheet_id` ASC) ,
  INDEX `task_user_id_idx` (`user_id` ASC) ,
  CONSTRAINT `task_sheet_id`
    FOREIGN KEY (`sheet_id`)
    REFERENCES `erp`.`sheet` (`sheet_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `task_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `erp`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`task_final`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`task_final` (
  `task_final_id` INT(11) NOT NULL AUTO_INCREMENT,
  `sheet_id` INT(11) NOT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  `final_date_id` INT(11) NULL DEFAULT NULL,
  `self_id` INT(11) NOT NULL,
  `parent_id` INT(11) NULL DEFAULT NULL,
  `sibling_id` INT(11) NULL DEFAULT NULL,
  `task_name` TEXT NOT NULL,
  `start_date` DATETIME NULL DEFAULT NULL,
  `end_date` DATETIME NULL DEFAULT NULL,
  `duration` VARCHAR(45) NULL DEFAULT NULL,
  `complete` INT(11) NULL DEFAULT NULL,
  `predecessors` INT(11) NULL DEFAULT NULL,
  `comment` VARCHAR(45) NULL DEFAULT NULL,
  `actual_end_date` DATETIME NULL DEFAULT NULL,
  `status` TEXT NULL DEFAULT NULL,
  `is_children` TINYINT(4) NOT NULL,
  `allocation` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`task_final_id`),
  INDEX `task_final_sheet_id_idx` (`sheet_id` ASC) ,
  INDEX `task_final_user_id_idx` (`user_id` ASC) ,
  INDEX `task_final_date_idx` (`final_date_id` ASC) ,
  CONSTRAINT `task_final_date_id`
    FOREIGN KEY (`final_date_id`)
    REFERENCES `erp`.`final_date` (`final_date_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `task_final_sheet_id`
    FOREIGN KEY (`sheet_id`)
    REFERENCES `erp`.`sheet` (`sheet_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `task_final_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `erp`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `erp`.`time_off`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `erp`.`time_off` (
  `time_off_id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NULL DEFAULT NULL,
  `department` VARCHAR(100) NOT NULL,
  `type` VARCHAR(100) NOT NULL,
  `start_date` DATETIME NOT NULL,
  `end_date` DATETIME NOT NULL,
  `date` DATETIME NULL DEFAULT NULL,
  `work_days` INT(11) NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  `updated_date` DATETIME NULL DEFAULT NULL,
  `updated_by` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`time_off_id`),
  INDEX `time_off_user_id_idx` (`user_id` ASC) ,
  CONSTRAINT `time_off_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `erp`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
