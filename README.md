# MARS Project

## Yahav Gabay

Write in python using the watchdog library that implements this tool, a client that listens to the folder where the files arrive.
For each file that arrives, do the following steps:
If the file is the first half, save in Redis the common name of the two halves as the key and the content will be the
full name of the file, and continue.
If the file is the second half, extract the name of the first file from Redis and send both files to the fastAPI server,
and delete both files from the folder.
Understand how to scan files that are already in the folder before running the client. (since watchdog listens to new
files that arrive in the folder and not to existing ones).
If the second half of the file has not arrived after a minute, delete it from Redis and the folder (find out which is
the correct and most effective method).
Required logs: files arrived/present, files sent successfully, errors.
Read about the difference between multiprocess and multithreading, think about which method will work better in our case
and implement it.