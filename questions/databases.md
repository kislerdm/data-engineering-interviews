# Databases

<!-- content -->

### Name types of join methods RDBMS (e.g. postres) supports? 🚀

TBD

***References***:

- https://severalnines.com/database-blog/overview-join-methods-postgresql

### What is 'nested loops join'? 👶

It&#39;s a basic approach databse engine takes to join two tables: for every value (external loop) of the &#39;left&#39; table&#39;s join key column, the engine loops (inner loop) over the values of the &#39;right&#39; table&#39;s join key column and selects the matching rows. This approach is basic and has the time complexity of O(n**2).

***References***:

- https://use-the-index-luke.com/sql/join/nested-loops-join-n1-problem

- https://www.youtube.com/watch?v=WfuLUE7lccs

### What is 'hash join'? ⭐️

Hash join is an optimizaton approach database engine may take to speed up a process of tables join. In this case, a in-memory hash table(s) is being generated using the values of the &#39;left&#39; table&#39;s join key column(s). The hash table values are used afterward to find matching rows of the &#39;right&#39; table. The hash join approach is faster compared to the nested loops join, it however has a limitation: whole hash table must fit into memory of the database machine. Another pro of hash join is, one doesn&#39;t need to index join key columns. The time complexity of such algorithm is O(n_left &#43; n_right), where n_left = number of &#39;left&#39; table&#39;s rows,  n_right = number of &#39;right&#39; table&#39;s rows.

***References***:

- https://use-the-index-luke.com/sql/join/hash-join-partial-objects

- https://www.youtube.com/watch?v=mlokdBiaMek

### When hash join may be selected by optimizer? 🚀

TBD

***References***:

- link1

### What's the difference between transactional and analytics databases? 👶

TBD

***References***:

- link1

### What's the difference between star and snowflake schema? 👶

TBD

***References***:

- link1

### Exlapin data normalization process? Why data are being normalized and denormalized in database? What's preferable for analytics db? 👶

TBD

***References***:

- link1

### What is window function? ⭐️

TBD

***References***:

- link1

### How to set dist keys in redshift? What strategies do you know? ⭐️

TBD

***References***:

- link1

### When would you use left join and when left outer join? 👶

TBD

***References***:

- link1

### What is WAL in postgres? Why it is being used? 🚀

TBD

***References***:

- link1

### What is table size limitation for postgres? 🚀

TBD

***References***:

- link1