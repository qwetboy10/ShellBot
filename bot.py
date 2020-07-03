import discord, subprocess, os, re, shlex
import requests
import secrets

context = {}

async def run_command(command, message, sudo=False):
    timeout = 1
    if command.startswith('```') and command.endswith('```'):
        command = command[3:-3]
    elif command.startswith('`') and command.endswith('`'):
        command = command[1:-1]
    if command == 'cd ~':
        context[message.channel] = 'cd ~'
    elif command.startswith('cd '):
        context[message.channel] = command[3:]
    else:
        try:
            if command.startswith('timeout='):
                timeout = int(command[len('timeout='):command.index(';')])
                command = command[command.index(';')+1:]
            if sudo:
                command = 'echo "password123" | sudo -S ' + command
            print('command: ' + command)
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, timeout=timeout, cwd=context[message.channel])
            outstr = output.decode('utf-8')
            if sudo and outstr.startswith('[sudo] password for bot: '):
                outstr = outstr[len('[sudo] password for bot: '):]
            if len(outstr) > 0:
                await message.channel.send('```' + outstr + '```')
            else:
                await message.channel.send(os.getcwd())
        except subprocess.TimeoutExpired as e:
            await message.channel.send('command timed out')
        except Exception as e:
            try:
                await message.channel.send('Error with exit code: ' + str(e.returncode) + '\n')
                outstr = e.output.decode('utf-8')
                if sudo and outstr.startswith('[sudo] password for bot: '):
                    outstr = outstr[len('[sudo] password for bot: '):]
                if len(outstr) > 0:
                    await message.channel.send('```' + outstr + '```')
            except Exception as e:
                print('error: ' + str(e))

async def handle_file(message):
    for attachment in message.attachments:
        print('fetching: ' + attachment.url)
        name = attachment.url[attachment.url.rindex('/')+1:]
        r = requests.get(attachment.url)
        with open(context[message.channel] + '/' + name, 'wb') as out:
            out.write(r.content)


class ShellClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        os.chdir('/home/bot')

    async def on_message(self, message):
        try:
            if isinstance(message.channel, discord.TextChannel) and isinstance(message.author, discord.Member):
                if not message.channel in context:
                    context[message.channel] = "/home/bot"
                channel = message.channel
                author = message.author
                if channel.name.startswith('tty') or channel.name.startswith('pty'):
                    sudo = False
                    if any(str(role.name) == 'President' for role in author.roles):
                        sudo = True
                    if any(str(role.name) == 'Shell' for role in author.roles):
                        if len(message.attachments) != 0:
                            await handle_file(message)
                        else:
                            await run_command(message.content, message, sudo=sudo)
        except Exception as e:
            print('big error: ' + str(e))

client = ShellClient()
client.run(secrets.token)
