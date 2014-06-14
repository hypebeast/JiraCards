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
default_issue_color = #007F00
color_story = #007F00
color_bug = #FF0000
color_aufgabe = #007F00
color_sub_task = #007F00
color_analyse = #3366FF
color_technische_story = #007F00
"""


def getBoardIssues(jira_url, boardId, user="", password=""):
    if user == "":
        r = requests.get(jira_url + BOARD_API + boardId)
    else:
        r = requests.get(jira_url + BOARD_API + boardId, auth=HTTPBasicAuth(user, password))
    data = r.json()

    issues = []
    for rawIssue in data['issuesData']['issues']:
        issue = Issue()
        issue.key = rawIssue['key']
        issue.summary = rawIssue['summary']
        issue.typeName = rawIssue['typeName']
        issues.append(issue)

    return issues

def getIssues(jira_url, issues, user="", password=""):
    result = []
    for issue in issues:
        result.append(getIssue(jira_url, issue, user, password))
    return result

def getIssue(jira_url, issue, user="", password=""):
    if user == "":
        r = requests.get(jira_url + ISSUE_API + issue)
    else:
        r = requests.get(jira_url + ISSUE_API + issue, auth=HTTPBasicAuth(user, password))
    data = r.json()
    issue = Issue()
    issue.key = data['key']
    issue.summary = data['fields']['summary']
    issue.typeName = data['fields']['issuetype']['name']
    return issue

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

def setColorForIssueTypes(tickets, colors, defaultColor):
    for ticket in tickets:
        if ticket.typeName != '':
            issueType = ticket.typeName.lower().strip().replace(' ', '_').replace('-', '_')
            if issueType in colors:
                ticket.cardcolor = colors[issueType]
            else:
                ticket.cardcolor = defaultColor

def setColor(tickets, color):
    for ticket in tickets:
        ticket.cardcolor = color

def setProjectColor(tickets, project, color):
    for ticket in tickets:
        if ticket.key.startswith(project):
            ticket.cardcolor = color

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


class Issue:
    def __init__(self):
        self.key = ""
        self.summary = ""
        self.typeName = ""
        self.cardcolor = ""


# define an application base controller
class AppBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = 'jira-cards reads tickets from a Jira board and creates nice cards that can be printed out.'
        arguments_override_config = True
        config_defaults = dict(
            jira='',
            user='',
            password='',
            output='cards.html',
            board='1',
            config='config',
            issueTypes=['Story', 'Bug', 'Aufgabe', 'Sub-task', 'Analyse','Technische Story'],
            default_issue_color='#007F00',
            color_story='#007F00',
            color_bug='#FF0000',
            color_aufgabe='#007F00',
            color_sub_task='#007F00',
            color_analyse='#3366FF',
            color_technische_story='#007F00',
            )
        arguments = [
            (['-j', '--jira'], dict(action='store', help='Jira URL', dest='jira')),
            (['-u', '--user'], dict(action='store', help='Jira username', dest='user')),
            (['-p', '--password'], dict(action='store', help='Jira password', dest='password')),
            (['-o', '--output'], dict(action='store', help='Output filename', dest='output')),
            (['-b', '--board'], dict(action='store', help='Jira board ID to get the tickets', dest='board')),
            (['-t', '--template'], dict(action='store', help='Template filename. The template file must be located in the template folder.', dest='template')),
            (['-c', '--config'], dict(action='store', help='Config file', dest='config')),
            (['--color'], dict(action='store', help='Card color (overrides the color definitions from the config file)', dest='color')),
            (['--project-color'], dict(action='store', help='Card color for issues from a project specified with the --project option', dest='projectcolor')),
            (['--project'], dict(action='store', help='Cards form this project will be generated with the color from the --project-color option', dest='project')),
            (['issues'], dict(nargs='*', help='Issue keys for the issues command'))
            ]

    def readConfig(self):
        # Set options from the default config
        self.jira = self.app.config.get('controller.base', 'jira')
        self.user = self.app.config.get('controller.base', 'user')
        self.password = self.app.config.get('controller.base', 'password')
        self.outputFile = self.app.config.get('controller.base', 'output')
        self.board = self.app.config.get('controller.base', 'board')
        self.config = self.app.config.get('controller.base', 'config')
        self.issueTypes = self.app.config.get('controller.base', 'issueTypes')
        self.defaultIssueColor = self.app.config.get('controller.base', 'default_issue_color')
        self.colors = {}
        self.template = None

        # Set options from the config file
        if has_key(self.app.config, 'jira-cards', 'jira'):
            self.jira = self.app.config.get('jira-cards', 'jira')
        if has_key(self.app.config, 'jira-cards', 'user'):
            self.user = self.app.config.get('jira-cards', 'user')
        if has_key(self.app.config, 'jira-cards', 'password'):
            self.password = self.app.config.get('jira-cards', 'password')
        if has_key(self.app.config, 'jira-cards', 'output'):
            self.outputFile = self.app.config.get('jira-cards', 'output')
        if has_key(self.app.config, 'jira-cards', 'board'):
            self.board = self.app.config.get('jira-cards', 'board')
        if has_key(self.app.config, 'jira-cards', 'template'):
            self.template = self.app.config.get('jira-cards', 'template')
        if has_key(self.app.config, 'jira-cards', 'issueTypes'):
            self.issueTypes = [x.strip() for x in self.app.config.get('jira-cards', 'issueTypes').split(',')]
        if has_key(self.app.config, 'jira-cards', 'issueTypes'):
            self.defaultIssueColor = self.app.config.get('jira-cards', 'default_issue_color')

        # Set options from command line arguments
        if self.app.pargs.jira:
            self.jira = self.app.pargs.jira
        if self.app.pargs.user:
            self.user = self.app.pargs.user
        if self.app.pargs.password:
            self.password = self.app.pargs.password
        if self.app.pargs.output:
            self.outputFile = self.app.pargs.output
        if self.app.pargs.board:
            self.board = self.app.pargs.board
        if self.app.pargs.template:
            self.template = self.app.pargs.template
        if self.app.pargs.config:
            self.config = self.app.pargs.config

        # Get the card colors from the config and set the color to the appropriate issue type
        getColors(self.app.config, 'controller.base', self.issueTypes, self.colors)
        getColors(self.app.config, 'jira-cards', self.issueTypes, self.colors)

    def generateCards(self, issues):
        if self.template:
            output = compileTemplate(issues, self.template)
        else:
            output = compileTemplate(issues)

        with codecs.open(self.outputFile, 'w', 'utf-8-sig') as file:
            file.write(output)

    @controller.expose(hide=False, aliases=['generate'], help='Read issues from a Jira Board and creates a card for every found issue')
    def default(self):
        self.readConfig()

        if not self.jira:
            self.app.log.info('No JIRA URL specified. Please, provide a Jira URL.')
            sys.exit(1)

        self.app.log.info('Getting Jira issues')
        issues = getBoardIssues(self.jira, self.board, self.user, self.password)

        self.app.log.info("Found " + str(len(issues)) + " issues")

        # Set color for every issue type
        setColorForIssueTypes(issues, self.colors, self.defaultIssueColor)

        if self.app.pargs.color:
            setColor(issues, self.app.pargs.color)

        if self.app.pargs.projectcolor and self.app.pargs.project:
            setProjectColor(issues, self.app.pargs.project, self.app.pargs.projectcolor)

        self.app.log.info('Generating cards')
        self.generateCards(issues)
        self.app.log.info('Done! All cards generated.')

    @controller.expose(help='Create cards for the specified Jira issues')
    def issues(self):
        self.readConfig()

        if not self.jira:
            self.app.log.info('No JIRA URL specified. Please, provide a Jira URL.')
            sys.exit(1)

        self.app.log.info('Getting Jira issues')
        issues = getIssues(self.jira, self.app.pargs.issues, self.user, self.password)

        # Set color for every issue type
        setColorForIssueTypes(issues, self.colors, self.defaultIssueColor)

        if self.app.pargs.color:
            setColor(issues, self.app.pargs.color)

        if self.app.pargs.projectcolor and self.app.pargs.project:
            setProjectColor(issues, self.app.pargs.project, self.app.pargs.projectcolor)

        self.app.log.info('Generating cards')
        self.generateCards(issues)
        self.app.log.info('Done! All cards generated.')

    @controller.expose(help='Prints the default template to stdout')
    def printtemplate(self):
        print DEFAULT_TEMPLATE

    # @controller.expose(help='Prints the available template data to stdout')
    # def printdata(self):
    #     pass


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

if __name__ == '__main__':
    main()
