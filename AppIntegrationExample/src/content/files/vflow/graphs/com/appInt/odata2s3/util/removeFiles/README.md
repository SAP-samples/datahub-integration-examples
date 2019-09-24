# Remove file from S3

## Description

This is a helper graph to remove files or directories from Amazon S3 without having to install any file management software for Amazon S3. (If you already have an Amazon S3 file manager you will not need this graph.) 

The graph is composed of the following components:
- Remove File: Removes a file or directory from the configured storage service
- Terminal: Used to enter a file or directory path to be deleted and to display the result of the operation.

## Prerequisites

- For this graph to run you will need the following:
    - Configured connection to Amazon S3 with ID `APPINT_S3`
        - Remark: you can also use corresponding object store solutions from Microsoft Azure or Google Cloud Platform.

## Configure and Run the Graph

No specific configuration is required for this graph. Just run it, open the Terminal UI, and enter the path of the file or directory to be deleted. **Please note that the file or directory will be deleted without any further confirmation!**

<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>
