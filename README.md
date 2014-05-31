# JIRA-CARDS

JiraCards prints agile cards for your physical board from Jira. The issues are read from a Jira Agile Board or individual issues can be provided to create single cards.

## Overview

JiraCards makes it super easy to generate physical cards from digital Jira issues. By default it fetches Jira issues from a given Jira Agile Board and generates for every found issue on the board a physical card. The generated cards are written to a HTML file. This HTML file can be used to print the cards.

The cards produced are clear and readable and a custom template can be provided to easily create custom looking cards.

JiraCards uses the Jira REST API to get all the relevant data from Jira. You can provide a username and password for authentication. BasicAuth is used for authentication.

On an A4 page 6 cards are rendered. The cards can then be easily guillotined out and then used on your physical board.

## Installation

### Using pip

To install JiraCards:

    $ sudo pip install jira-cards

### From source

First, get the latest source code:

    $ git clone https://github.com/hypebeast/JiraCards.git

Install it:

    $ cd JiraCards
    $ python setup.py install

## Configuration

JiraCards reads the configuration from the following place:

    $ ~/.jira-cards/config

The configuration file is created during the first startup of JiraCards. If you want to create the config file with the default options just execute the program:

    $ jira-cards -h

### Use another config file

If you want to use a different configuration file, you can call JiraCards with *--config* option:

    $ jira-cards --config my_config

### Configuration Options

The following options are available:

  * **jira**: The URL of your Jira instance.
  * **user**: The username you want to use for authentication.
  * **password**: The password you want to use for authentication.
  * **output**: The name of the output file.
  * **board**: The Jira Board ID.
  * **template**: The filename of the custom template. If no template is provided, the default template is used.
  * **issueTypes**: The available issue types. T
  * **default_issue_color**: The default color for a issue.
  * **color_**:

## Usage

To list all available commands and options:

    $ jira-cards -h

If you want to generate cards from your JIRA Agile Board with ID 19, execute the following command:

    $ jira-cards

### Available Commands

For an overview about all commands run JiraCards with the help options:

    $ jira-cards -h

The following commands are available:

  * **gen**: This the default command. If JiraCards is called without a command this command will be executed. It reads Jira issues from the specified board and generates 
  * **show**: Prints the default template to stdout. The default template can be used to create a custom template.

### Command Line Options

For an overview about all commands run JiraCards with the help options:

    $ jira-cards -h

TODO

## Custom Template

It's possible to create a custom template in order to create different looking cards. To provide a custom 

### Available 
