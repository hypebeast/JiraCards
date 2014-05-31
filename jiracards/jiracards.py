from cement.core import backend, foundation, controller, handler
import requests
from requests.auth import HTTPBasicAuth
from jinja2 import Environment, FileSystemLoader, Template
import codecs
import sys, os
from os.path import expanduser
from template import DEFAULT_TEMPLATE

APP_NAME = 'jira-cards'

BOARD_API = '/rest/greenhopper/1.0/xboard/work/allData.json?rapidViewId='
ISSUE_API = '/rest/api/2/issue/'
ISSUE_TYPE_API = '/rest/api/2/issuetype/'

DEFAULT_CONFIG_FILE="""[jira-cards]
jira = http://jira.example.de
user = testuser
password = password
output = cards.html
board = 1
template = mytemplate.html
issueTypes = Story,Bug,Aufgabe,Sub-task,Analyse,Technische Story
default_issue_color = #00FF00
color_story = #00FF00
color_bug = #FF0000
color_aufgabe = #00FF00
color_sub_task = #00FF00
color_analyse = #0000FF
color_technische_story = #0000FF
"""


def getBoardIssues(jira_url, boardId, user="", password=""):
    if user == "":
        r = requests.get(jira_url + BOARD_API + boardId)
    else:
        r = requests.get(jira_url + BOARD_API + boardId, auth=HTTPBasicAuth(user, password))
    data = r.json()
    return data['issuesData']['issues']

def compileTemplate(tickets, template=""):
    # Check if a template was specified
    if template != "" and os.path.exists(template):
        templateFolder = os.path.dirname(os.path.realpath(template))
        env = Environment(loader=FileSystemLoader(templateFolder))
        template = env.get_template(os.path.basename(template))
        return template.render(tickets=tickets)
    else: # Use the default template
        template = Template(DEFAULT_TEMPLATE)
        return template.render(tickets=tickets)

def setIssuesColor(tickets, colors, defaultColor):
    for ticket in tickets:
        if 'typeName' in ticket:
            issueType = ticket['typeName'].lower().strip().replace(' ', '_').replace('-', '_')
            if issueType in colors:
                ticket['cardcolor'] = colors[issueType]
            else:
                ticket['cardcolor'] = defaultColor

def getColors(config, section, issueTypes, colors):
    for issueType in issueTypes:
        issueType = issueType.lower().strip().replace(' ', '_').replace('-', '_')
        colorKey = 'color_' + issueType
        if has_key(config, section, colorKey):
            colors[issueType] = config.get(section, colorKey)

def has_key(config, section, key):
    keys = config.keys(section)
    if key in keys:
        return True

    return False

# define an application base controller
class AppBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = 'jira-cards reads tickets from a Jira board and creates nice cards that can be printed.'
        arguments_override_config = True
        config_defaults = dict(
            jira='',
            user='',
            password='',
            output='cards.html',
            board='1',
            config='config',
            issueTypes=['Story', 'Bug', 'Aufgabe', 'Sub-task', 'Analyse','Technische Story'],
            default_issue_color='#00FF00',
            color_story='#0000FF',
            color_bug='#FF0000',
            color_aufgabe='#00FF00',
            color_sub_task='#00FF00',
            color_analyse='#0000FF',
            color_technische_story='#0000FF',
            )
        arguments = [
            (['-j', '--jira'], dict(action='store', help='Jira URL', dest='jira')),
            (['-u', '--user'], dict(action='store', help='Jira username', dest='user')),
            (['-p', '--password'], dict(action='store', help='Jira password', dest='password')),
            (['-o', '--output'], dict(action='store', help='Output filename', dest='output')),
            (['-b', '--board'], dict(action='store', help='Jira board ID to get the tickets', dest='board')),
            (['-t', '--template'], dict(action='store', help='Template filename. The template file must be located in the template folder.', dest='template')),
            (['-c', '--config'], dict(action='store', help='Config file', dest='config'))
            ]

    @controller.expose(hide=False, aliases=['gen'], help='Read issues from a Jira Board and creates a card for every found issue')
    def default(self):
        jira = self.app.config.get('controller.base', 'jira')
        user = self.app.config.get('controller.base', 'user')
        password = self.app.config.get('controller.base', 'password')
        outputFile = self.app.config.get('controller.base', 'output')
        board = self.app.config.get('controller.base', 'board')
        config = self.app.config.get('controller.base', 'config')
        issueTypes = self.app.config.get('controller.base', 'issueTypes')
        defaultIssueColor = self.app.config.get('controller.base', 'default_issue_color')
        template = None

        # Set options from config file
        if has_key(self.app.config, 'jira-cards', 'jira'):
            jira = self.app.config.get('jira-cards', 'jira')
        if has_key(self.app.config, 'jira-cards', 'user'):
            user = self.app.config.get('jira-cards', 'user')
        if has_key(self.app.config, 'jira-cards', 'password'):
            password = self.app.config.get('jira-cards', 'password')
        if has_key(self.app.config, 'jira-cards', 'output'):
            outputFile = self.app.config.get('jira-cards', 'output')
        if has_key(self.app.config, 'jira-cards', 'board'):
            board = self.app.config.get('jira-cards', 'board')
        if has_key(self.app.config, 'jira-cards', 'template'):
            template = self.app.config.get('jira-cards', 'template')
        if has_key(self.app.config, 'jira-cards', 'issueTypes'):
            issueTypes = [x.strip() for x in self.app.config.get('jira-cards', 'issueTypes').split(',')]
        if has_key(self.app.config, 'jira-cards', 'issueTypes'):
            defaultIssueColor = self.app.config.get('jira-cards', 'default_issue_color')

        # Set options from command line arguments
        if self.app.pargs.jira:
            jira = self.app.pargs.jira
        if self.app.pargs.user:
            user = self.app.pargs.user
        if self.app.pargs.password:
            password = self.app.pargs.password
        if self.app.pargs.output:
            outputFile = self.app.pargs.output
        if self.app.pargs.board:
            board = self.app.pargs.board
        if self.app.pargs.template:
            template = self.app.pargs.template
        if self.app.pargs.config:
            config = self.app.pargs.config

        colors = {}
        getColors(self.app.config, 'controller.base', issueTypes, colors)
        getColors(self.app.config, 'jira-cards', issueTypes, colors)

        if not jira:
            self.app.log.info('No JIRA URL specified. Please, provide a Jira URL.')
            sys.exit(1)

        self.app.log.info('Retrieving Jira issues')
        issues = getBoardIssues(jira, board, user, password)

        # Set color for every issue
        setIssuesColor(issues, colors, defaultIssueColor)

        self.app.log.info('Generating cards')
        if template:
            output = compileTemplate(issues, template)
        else:
            output = compileTemplate(issues)

        with codecs.open(outputFile, 'w', 'utf-8-sig') as file:
            file.write(output)

        self.app.log.info('Done! All cards generated.')

    @controller.expose(help='Create cards for the specified Jira issues')
    def tickets(self):
        pass

    @controller.expose(help='Prints the default template to stdout')
    def show(self):
        print DEFAULT_TEMPLATE

    @controller.expose(help='Prints the available template data to stdout')
    def tempdata(self):
        pass


class MyApp(foundation.CementApp):
    class Meta:
        label = APP_NAME
        base_controller = AppBaseController

def main():
    # create the app
    app = MyApp()

    try:
        # Create default config file if it doesn't exists
        home = expanduser('~')
        configDir = os.path.join(home, '.' + APP_NAME)
        if not os.path.exists(configDir):
            os.makedirs(configDir)

        configFile = os.path.join(configDir, 'config')
        if not os.path.exists(configFile):
            with open(configFile, 'w') as f:
                f.write(DEFAULT_CONFIG_FILE)

        # setup the application
        app.setup()

        # run the application
        app.run()
    finally:
        # close the app
        app.close()
