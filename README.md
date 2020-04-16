# Google Sheet Log

## Name
go - keyword to run program

## Synopsis
```
go <command> [-options] [<args>]
```
## Description
Log messages from terminal to Google Sheets.

Using Git-like commands, the user will be able to log, pull, and interact with message logs. The logs are currently being stored in a Google Sheet but may be moved to a locally- or cloud-stored SQL database. Using bash, the user can execute different commands to interact with the log.

Current version tracks date, time, project, and message.

## Options

**\-p**
Identify is a specific project by project name

**-l**
Identify a specific log by log id


## Commands
**new**
- Create a new log using the most recent logged project.
- Create a new log using with a specific project name using the **-p** option.

**last**
- Get the most recent log.
- Get the most recent log of the specified project using the **-p** option.

**del**
- Delete the most recent log.
- Delete the most recent log of a specified project using the **-p** option.
- Delete the specific log using the **-l** option.


## Examples
```
$ go new "This is my log message with quotes"
$ go new This is also my log message without quotes
```
