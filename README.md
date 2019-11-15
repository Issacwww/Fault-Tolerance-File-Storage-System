## Simple Fault Tolerance File Storage System

### Summary

This project is a prototype for Simple Fault Tolerance File Storage System, implemented in Python and Socket, it provides some functions: User connection, Upload files, Read file content and read file list.

The system has two main components: Directory server and Storage node, for the fault tolerance, some backup nodes are created to protect the Main node to provide service. 

![image-20191115161030422](/Users/ssuchao/Library/Application Support/typora-user-images/image-20191115161030422.png)

### Usage

**Bootstrap the Directory Server:**

We first start up the Directory node as well as its backup nodes, by running `python backup2.py` at a terminal under the `src/directory`

**Bootstrap the Storage node:**

 Similarly, start up the Storage node by running `python backup2.py` at another terminal under the `src/s1` , for more storage node, simply duplicate another.

**Client**:

At third terminal, running this command , the arguments of actions are listed 

- Connect:  `{uid} c`, This command could build a connection with directory server.
- Upload: ` {uid} a {list of filenames} `: this command could add a list of files (separated by space)  to the server , if you input the fie already uploaded, this operation will be considered as update the file.
- Read: `  {uid} r {filename} ` read one file at a time, the content of the file will returned
- List files (directory server): ` {uid} d`, list the files of this user,
- List files (storage node): ` {uid} d`, it share same function with previous  one, but it will return the list from storage node instead of directory server

### Performance Testing

`test.sh` is used to test the performance of the system, after bootstrapping the directory server and storage nodes, you could run it test.

List one of my test result belo (100 clients with killing process of storage node 2 and recovery )![metrics](/Users/ssuchao/Code/Python/FTFS/testres/50client-2-with-kill/metrics.jpg)