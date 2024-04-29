from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(200) NOT NULL,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `email` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `avatar` VARCHAR(255) NOT NULL  DEFAULT './img/default.png'
) CHARACTER SET utf8mb4 COMMENT='The User model.';
        CREATE TABLE IF NOT EXISTS `books` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(200) NOT NULL,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `description` VARCHAR(255) NOT NULL,
    `cover` VARCHAR(255) NOT NULL  DEFAULT './img/book/covers/default.png',
    `isAvailable` BOOL NOT NULL  DEFAULT 0,
    `creator_id` INT NOT NULL,
    CONSTRAINT `fk_books_user_8713072d` FOREIGN KEY (`creator_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='The Books model.';
        """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `user`;
        DROP TABLE IF EXISTS `books`;"""
