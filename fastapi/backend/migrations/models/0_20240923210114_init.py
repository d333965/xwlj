from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `legym_customer` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `manager` VARCHAR(20) NOT NULL,
    `username` VARCHAR(20) NOT NULL,
    `password` VARCHAR(20) NOT NULL,
    `schoolName` VARCHAR(20) NOT NULL,
    `runType` VARCHAR(20) NOT NULL,
    `total_goals` DOUBLE NOT NULL  DEFAULT 0,
    `day_goals` DOUBLE NOT NULL  DEFAULT 0,
    `day_in_week` INT NOT NULL  DEFAULT 5,
    `rounds` INT NOT NULL  DEFAULT 0,
    `begin_state` BOOL NOT NULL  DEFAULT 1,
    `runTime` VARCHAR(20) NOT NULL,
    `is_run` BOOL NOT NULL  DEFAULT 0,
    `complete_goals` DOUBLE NOT NULL  DEFAULT 0
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `manager` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `manager` VARCHAR(20) NOT NULL,
    `password` VARCHAR(20) NOT NULL,
    `create_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `score` DOUBLE NOT NULL  DEFAULT 0,
    `is_admin` BOOL NOT NULL  DEFAULT 0
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
