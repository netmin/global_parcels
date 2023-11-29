from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `parcel_types` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT 'Name of the parcel type'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `parcel` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL  COMMENT 'Name of the parcel',
    `weight` DOUBLE NOT NULL  COMMENT 'Weight of the parcel',
    `content_value_cents` INT NOT NULL  COMMENT 'Value of the content in cents',
    `delivery_cost_cents` INT   COMMENT 'Delivery cost in cents',
    `session_id` VARCHAR(255)   COMMENT 'ID of the users session',
    `parcel_type_id` INT NOT NULL COMMENT 'Type of the parcel',
    CONSTRAINT `fk_parcel_parcel_t_f5c54bdb` FOREIGN KEY (`parcel_type_id`) REFERENCES `parcel_types` (`id`) ON DELETE CASCADE
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
