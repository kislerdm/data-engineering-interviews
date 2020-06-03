# Distributed computing

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

### What is Apache Hive Metastore? 👶

Metastore is a Hive serivce to store Hive tables and partitions metadata in any JDBC compliant relational database. It provides client access to this information by using metastore service API.

Hive metastore consists of two fundamental units:

1. A service that provides metastore access to other Apache Hive services.

2. Disk storage for the Hive metadata which is separate from HDFS storage.

There are three modes for Hive Metastore deployment:

- *Embedded Metastore* (default). The metastore service runs in the same JVM as the main HiveServer process and uses embedded *Derby* database. *Such deployment would allow only one Hive session*, hense it's not useful for production.

- *Local Metastore*. The metastore service runs in the same process as the main HiveServer process, but the metastore database runs in a separate process, and can be on a separate host. The embedded metastore service communicates with the metastore database over JDBC.

- *Remote Metastore*. The metastore service runs in its own JVM process. HiveServer and other processes communicate with it using the *Thrift network API*. The metastore service communicates with the metastore database over JDBC. The database, the HiveServer process, and the metastore service can all be on the same host, but running the HiveServer process on a separate host provides better availability and scalability. The main advantage of Remote mode over Local mode is that Remote mode does not require the administrator to share JDBC login information for the metastore database with each Hive user.

***References***:

- https://docs.cloudera.com/documentation/enterprise/5-8-x/topics/cdh_ig_hive_metastore_configure.html


### What is MapReduce, how it works? ⭐

TBD

***References***:

- link1

- link2

### Assuming that your have developed a pyspark program to process a data batch, how spark executes it? 🚀

TBD

***References***:

- link1

- link2
