import discord
import asyncio
import csv
import os.path
from cmds.bot import Bot

client = Bot.client


class project_manager(object):
    def __init__(self):
        self.name = 'project'
        self.project_list = self.read_projects()
        self.project_names = [string.lower() for string in self.project_list.keys()]

    @asyncio.coroutine
    def do_command(self, message):
        text = message.content.lower().split(' ', 2)[1]
        if text == 'add' and ('Suppirts' in [role.name for role in message.author.roles] or 'Souppirts' in [role.name for role in message.author.roles]):
            project_name = message.content.split(' ', 2)[2]
            if project_name.lower() not in self.project_names:
                self.project_list.update({project_name: Project(project_name,[message.author.id])})
                self.write_projects()
                self.project_names.append(project_name.lower())
                text_out = project_name + ' has been added'
            elif project_name.lower() in self.project_names:
                text_out = 'Project already exists!'
            yield from client.send_message(message.channel, text_out)

        elif text == 'delete':
            project_name = message.content.split(' ', 2)[2]
            if ('Suppirts' in [role.name for role in message.author.roles] or 'Souppirts' in [role.name for role in message.author.roles]):
                if project_name.lower() in self.project_names:
                    yield from client.send_message(message.channel,'Do you really want to delete this project? Y/N')
                    msg = 'placeholder'
                    while not (msg.lower() == 'y' or msg.lower() == 'n'):
                        msg = yield from client.wait_for_message(author=message.author)
                        msg = msg.content
                        if not (msg.lower() == 'y' or msg.lower() == 'n'):
                            yield from client.send_message(message.channel,'Please answer Y or N.')
                    if msg.lower() == 'y':
                        self.project_list.pop(project_name.lower())
                        self.write_projects()
                        self.project_names.remove(project_name.lower())
                        print(self.project_names)
                        print(self.project_list)

                        yield from client.send_message(message.channel,'Project deleted.')
                    elif msg.lower() == 'n':
                        yield from client.send_message(message.channel,'Project was not deleted.')

                else:
                    yield from client.send_message(message.channel,'Project not found.')
            elif not ('Suppirts' in [role.name for role in message.author.roles] or 'Souppirts' in [role.name for role in message.author.roles]):
                yield from client.send_message(message.channel,'You must be a mod to do this.')

        elif text == 'list':
            all_projects = 'Our current projects:\n'
            for project in self.project_list:
                all_projects += ' - ' + self.project_list[project].name + '\n'
            yield from client.send_message(message.channel, all_projects)

        elif text == 'participants':
            yield from client.send_message(message.channel,'no')

        elif text == 'join':
            project_name = message.content.split(' ', 2)[2].lower()
            print(project_name)
            print(self.project_names)
            if project_name in self.project_names:
                if message.author.id not in self.project_list[project_name].participants:
                    self.project_list[project_name].participants.append(message.author.id)
                    self.write_projects()
                    text_out = 'You have joined the project ' + project_name + '.'
                    yield from client.send_message(message.channel,text_out)
                else:
                    yield from client.send_message(message.channel, 'You\'re already in this project!')
            else:
                yield from client.send_message(message.channel,'Project not found.')

        elif text == 'leave':
            project_name = message.content.split(' ', 2)[2].lower()
            if project_name in self.project_names:
                if message.author.id not in self.project_list[project_name].participants:
                    text_out = 'You aren\'t even in this project!'
                    yield from client.send_message(message.channel,text_out)
                else:
                    self.project_list[project_name].participants.remove(message.author.id)
                    self.write_projects()
                    yield from client.send_message(message.channel, 'You have left this project.')
            else:
                yield from client.send_message(message.channel,'Project not found.')

    def read_projects(self):
        project_list = dict()
        with open('projects.csv', newline='') as file:
            projects = csv.reader(file)
            try:
                for row in projects:
                    project_name = row[0]
                    participants = row[1::]
                    new_project = Project(project_name,participants)
                    project_list.update({project_name.lower(): new_project})
            except:
                pass
        return project_list

    def write_projects(self):
        projects = []
        for project in self.project_list:
            participants_id = self.project_list[project].participants
            projects.append([project,*participants_id])
        with open('projects.csv','w+',newline='') as file:
            csvwrite = csv.writer(file)
            for project in projects:
                csvwrite.writerow(project)


class Project(object):
    def __init__(self,name,participants):
        self.name = name
        self.participants = participants
