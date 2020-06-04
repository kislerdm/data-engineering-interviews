# Databases

<table>
   <tr>
      <td>⚠️</td>
      <td>
         The answers here are given by the community. Be careful and double check the answers before using them. <br>
         If you see an error, please create a PR with a fix.
      </td>
   </tr>
</table>

**Legend**: 👶 easy ‍⭐️ medium 🚀 expert

<!-- content -->

### Name types of join methods RDBMS (e.g. postres) supports? ‍⭐️

As of today, postgres supports three join methods:

- nested loops
- hash join
- merge join

TBD

***References***:

- https://severalnines.com/database-blog/overview-join-methods-postgresql

### What is 'nested loops join'? 👶

It's a basic approach databse engine takes to join two tables: for every value (external loop) of the "left" table's join key column, the engine loops (inner loop) over the values of the "right" table's join key column and selects the matching rows. This approach is basic and has the time complexity of O(n<sub>left</sub><sup>2</sup> + n<sub>right</sub><sup>2</sup>), where n<sub>left</sub> = number of "left" table's rows, n<sub>right</sub> = number of the "right" table's rows.

***References***:

- https://use-the-index-luke.com/sql/join/nested-loops-join-n1-problem

- https://www.youtube.com/watch?v=WfuLUE7lccs

### What is 'hash join'? ⭐️

Hash join is an optimizaton approach database engine may take to speed up a process of tables join. In this case, a in-memory hash table(s) is being generated using the values of the "left" table's join key column(s). The hash table values are used afterward to find matching rows of the "right" table. The hash join approach is faster compared to the nested loops join, it however has a limitation: whole hash table must fit into memory of the database machine. Another pro of hash join is, one doesn't need to index join key columns. The time complexity of such algorithm is O(n<sub>left</sub> + n<sub>right</sub>), where n<sub>left</sub> = number of "left" table's rows, n<sub>right</sub> = number of the "right" table's rows.

**!The join method can only be selected by optimizer, if '=' operator is used as the join condition!**

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

A window function performs a calculation across a set of table rows that are somehow related to the current row. This is comparable to the type of calculation that can be done with an aggregate function. But unlike regular aggregate functions, use of a window function does not cause rows to become grouped into a single output row — the rows retain their separate identities. Behind the scenes, the window function is able to access more than just the current row of the query result.

***References***:

- https://mode.com/sql-tutorial/sql-window-functions/

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
