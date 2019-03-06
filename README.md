# file-monitor
RESTful Server to manage and monitor files

## Monitor and manage files in a given directory
Read the information of the files in a directory (name, path, creation date/time, modification
date/time and size)
2. Import the data into a PostgreSQL/MySQL/MongoDB databases. The result should be one
table or collection to store this information.
3. Monitor the directory to see if there are new files or changes in existing ones. (could use
cronjobs, infinite loops with parallel threads or any other solution)
4. Archive the oldest files (more than 5 days). Consider having a new field in the
database table or move the files to another directory.
5. Develop an small web API with two endpoints to: get a JSON object with the avaiable files
and get a JSON object with archived files.
