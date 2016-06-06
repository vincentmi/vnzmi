---
layout:     post
title:      "MySQL和MSSQL 查询比较"
date:       2015-05-03 8:36:00
author:     "Vincent"
header-img:  "img/post-bg.jpg"
catalog: true
tags:
    - RD
---

   
Current Date and Time
MS: SELECT GETDATE()
MY: SELECT NOW()
Optionally: Use CURDATE() for the date only.Limiting Results

MS: SELECT TOP 10 * FROM table WHERE id = 1
MY: SELECT * FROM table WHERE id = 1 LIMIT 10Date Field Default Value

MS: DATETIME DEFAULT GETDATE()
MY: DATETIME fields cannot have a default value, i.e. "GETDATE()"

You must use your INSERT statement to specify CURDATE() for the field.
Optionally: Use datatype TIMESTAMP DEFAULT CURRENT_TIMESTAMPCharacter Length

MS: LEN()
MY: CHARACTER_LENGTH() Aliases: CHAR_LENGTH(), LENGTH()Character Replace

MS: REPLACE() works case insensitively
MY: REPLACE() works case sensitivelyTrim Functions

MS: LTRIM() and RTRIM()
MY: TRIM()String Concatenation

MS: CONCATENATION USING + (Does not automatically cast operands to compatible types)
MY: CONCAT(string, string), which accepts two or more arguments.
(Automatically casts values into types which can be concatenated)Auto Increment Field Definition

MS: tablename_id INT IDENTITY PRIMARY KEY
MY: tablename_id INTEGER AUTO_INCREMENT PRIMARY KEYGet a List of Tables

MS: SP_TABLES
MY: SHOW TABLESGet Table Properties

MS: HELP tablename
MY: DESCRIBE tablenameGet Database Version

MS: SELECT @@VERSION
MY: SELECT VERSION()Recordset Paging

MS: Recordset paging done by client side-ADO (very involved)
MY: Add to end of SQL: "LIMIT " & ((intCurrentPage-1)*intRecsPerPage) & ", " & intRecsPerPage
LIMIT: The first argument specifies the offset of the first row to return, and the second specifies the maximum number of rows to return. The offset of the initial row is 0 (not 1).Get ID of Newest Inserted Record

MS: SET NOCOUNT ON; INSERT INTO...; SELECT id=@@IDENTITY; SET NOCOUNT OFF;
MY: Two step process:
1. Execute your statement: objConn.Execute("INSERT INTO...")
2. Set objRS = objConn.Execute("SELECT LAST_INSERT_ID() AS ID")Get a Random Record

MS: SELECT TOP 1 * FROM Users ORDER BY NEWID()
MY: SELECT * FROM Users ORDER BY RAND() LIMIT 1Generate a Unique GUID

MS: SELECT NEWID()
MY: SELECT UUID()


