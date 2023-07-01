---
layout:     post
title:      "MySQL InnoDB表的限制"
date:       2013-03-08 17:18:00
author:     "Vincent"
image:  "img/post-bg.jpg"
catalog: true
tags:
    - MySQL
---

- 一个表不能包含超过1000列。 
- 内部最大键长度是3500字节，但MySQL自己限制这个到1024字节。 

- 除了VARCHAR, BLOB和TEXT列，最大行长度稍微小于数据库页的一半。即，最大行长度大约8000字节。LONGBLOB和LONGTEXT列必须小于4GB, 总的行长度，页包括BLOB和TEXT列，必须小于4GB。InnoDB在行中存储VARCHAR，BLOB或TEXT列的前768字节，余下的存储的分散的页面中。 

- 虽然InnoDB内部地支持行尺寸大于65535，你不能定义一个包含VARCHAR列的，合并尺寸大于65535的行。 

```sh
mysql>  CREATE TABLE t (a VARCHAR(8000), b VARCHAR(10000),
> c VARCHAR(10000), d VARCHAR(10000), e VARCHAR(10000), VARCHAR(10000), g VARCHAR(10000));
> ERROR 1118 (42000): Row size too large. The maximum row size for the
> used table type, not counting BLOBs, is 65535. You have to change some columns to TEXT or BLOBs
```

- 在一些更老的操作系统上，数据文件必须小于2GB。 

- InnoDB日志文件的合并尺寸必须小于4GB。 

- 最小的表空间尺寸是10MB。最大的表空间尺寸是4,000,000,000个数据库页（64TB）。这也是一个表的最大尺寸。 

- InnoDB表不支持FULLTEXT索引。 

- ANALYZE TABLE通过对每个索引树做八次随机深入并相应地更新索引集估值，这样来计数集。注意，因为这是仅有的估值，反复运行ANALYZE TABLE会产生不同数。这使得 ANALYZE TABLE 在 InnoDB 表上很快，不是百分百准确，因为它没有考虑所有的行。 

MySQL 不仅在汇合优化中使用索引集估值。如果一些汇合没有以正确的方式优化，你可以试一下 ANALYZE TABLE 。很少有情况，ANALYZE TABLE 没有产生对你特定的表足够好的值，你可以使用 FORCE INDEX 在你查询中来强制使用特定索引，或者设置 max_seeks_for_key               来确保MySQL在表扫描之上运行索引查找。请参阅5.3.3节，“服务器系统变量”。请参阅A.6节，“优化器相关的问题”。 

- 在Windows上，InnoDB总是内部地用小写字母存储数据库和表名字。要把数据库以二进制形式从Unix 移到Windows，或者从Windows移到Unix，你应该让所有数据库和表的名字都是小写。 

- 警告: 不要在MySQL数据库内的把MySQL系统表从MyISAM转为InnoDB表！这是一个不被支持的操作。如果你这么做了，MySQL直到你从备份恢复旧系统表，或用mysql_install_db脚本重建系统表才重启动。 

- InnoDB在表内不保留行的内部计数。（因为多版本化，这可能确实有些复杂）。要处理一个SELECT COUNT(*)               FROM t语句，InnoDB必须扫描表的一个索引，如果这个索引不在缓冲池中，扫描需要花一些时间。要获得快速计数，你不得不使用一个自己创建的计数器表，并让你的应用按照它做的插入和删除来更新它。如果你的表格不经常改变，使用MySQL查询缓存时一个好的解决方案。如果大致的行数就足够了，则SHOW               TABLE STATUS也可被使用。请参阅15.2.11节，“InnoDB性能调节提示”。 

- 对于AUTO_INCREMENT列，你必须总是为表定义一个索引，并且索引必须包含AUTO_INCREMENT列。在MyISAM表中，AUTO_INCREMENT列可能时多列索引的一部分。 

- 当你重启MySQL服务器之时，InnoDB可能为一个AUTO_INCREMENT列重使用一个旧值（即，一个被赋给一个老的已回滚的事务的值）。 

- 当一个AUTO_INCREMENT列用完值，InnoDB限制一个BIGINT到－9223372036854775808以及BIGINT               UNSIGNED到1。尽管如此，BIGINT值有由64位，所以注意到，如果你要一秒输入100万个行，在BIGINT到达它上限之前，可能还需要将近30万年。用所有其它整数类型列，产生一个重复键错误。这类似于MyISAM如何工作的，因为它主要是一般MySQL行为，并不特别关于任何存储引擎。 

- DELETE FROM tbl_name不重新生成表，但取而代之地删除所有行，一个接一个地删除。 

- TRUNCATE tbl_name为InnoDB而被映射到DELETE FROM tbl_name并且不重置AUTO_INCREMENT计数器。 

- SHOW TABLE STATUS不能给出关于InnoDB表准确的统计数据，除了被表保留的物理尺寸。行计数仅是在SQL优化中粗略的估计。 

- 在MySQL 5.1中，如果innodb_table_locks=1(1是默认值） MySQL LOCK TABLES操作在每一个表上获取两个锁定。除了在MySQL层的表锁定，它也获得一个InnoDB表锁定。旧版的MySQL不获取InnoDB表锁定，旧行为可以通过设置innodb_table_locks=0 来选择。如果没有InnoDB表锁定被获得，即使表的一些记录被其它事务锁定，LOCK TABLES完成。  

- 所有被一个事务持有的InnoDB锁定在该事务被提交或中止之时被释放。因此在AUTOCOMMIT=1模式，在InnoDB表上调用是没有太多意义的，因为被需求的InnoDB表锁定可能会被立即释放。 

- 有时，在事务的过程中锁定更多的表可能是有用的。不幸地，MySQL中的LOCK TABLES执行一个暗地的COMMIT和UNLOCK TABLES。LOCK TABLES的一个InnoDB变量已经被计划， 该计划在事务的中间被执行。 

- 为建立复制从服务器的LOAD               TABLE FROM MASTER语句对InnoDB表不起作用。一个工作区在主服务器上更换表为MyISAM的，然后做负载，之后更换主服务器表回到InnoDB中。 

- 在InnoDB中默认数据库页的大小是16KB。通过编译代码，你可以在8KB到64KB之间来设置这个值。你不得不更新在univ.i源文件中的UNIV_PAGE_SIZE和UNIV_PAGE_SIZE_SHIFT的值。 

- 在MySQL 5.1中，触发器不被级联的外键行为激活。 




