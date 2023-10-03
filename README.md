# git_repo_exporter

## Overview
The git_repo_exporter is a tool for monitoring commits on local repositories. It exposes the results as metrics in Prometheus format over HTTP.

## Exposed port
The application exposes Prometheus metrics over HTTP, and by default, it listens on port 8085.

## Volumes
A volume **must** be configured in order to monitor your localhost repositories. If you don't mount a directory, it will monitor the directory inside the container with no host machine folders and files.
The volume to mount the git repositories dir is **/repos/**.
For example
>/home/user/repos/:/repos/

You can configure the speedtest interval by specifying the following parameter:

https://github.com/SebaViana/git_repo_exporter/blob/4e452a257e37f55ae2f5a0da47a3aba5cf16a0b8/default.yml#L1

This parameter should be added to a mounted volume in the location /app/custom.yml.
