/* Run this script in SSMS while connected to the 'master' database.
   It creates the 'N7' database container and a dedicated user.
*/

-- 1. Create Database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'LeavesAppDB')
BEGIN
    CREATE DATABASE [LeavesAppDB]
    COLLATE SQL_Latin1_General_CP1_CI_AS;
END
GO

USE [LeavesAppDB];
GO

-- 2. Create Application User (Security Best Practice)
-- Don't use 'sa' in your FastAPI app; use a restricted user.
IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'LeavesAppUser')
BEGIN
    CREATE LOGIN [LeavesAppUser] WITH PASSWORD = 'YourStrongPassword123!', CHECK_POLICY = ON;
END
GO

IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'LeavesAppUser')
BEGIN
    CREATE USER [LeavesAppUser] FOR LOGIN [LeavesAppUser];
    ALTER ROLE [db_owner] ADD MEMBER [LeavesAppUser]; -- Permissions to create tables
END
GO