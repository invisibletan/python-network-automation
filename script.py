import json
import myfunction as fn
import netmiko
import os
import sys

if len(sys.argv) < 3:
    print('Usage: script.py commands.txt devices.json')
    exit()

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException, netmiko.ssh_exception.NetMikoAuthenticationException)

username, password = fn.get_credentials()

with open(sys.argv[1]) as cmd_file:
    commands = cmd_file.readlines()

with open(sys.argv[2]) as dev_file:
     devices = json.load(dev_file)

for device in devices:
    device['username'] = username
    device['password'] = password
    try:
        print('-' * 70)
        print('Connecting to device:', device['ip'])
        connection = netmiko.ConnectHandler(**device)
        connection.enable()
        newdir = connection.base_prompt
        try:
            os.mkdir(newdir)
        except OSError as error:
            # FileExistsError is error # 17
            if error.errno == 17:
                print('Directory', newdir, 'already exists.')
            else:
                # re-raise the exception if some other error occurred.
                raise
        for command in commands:
            filename = command.rstrip().replace(' ', '_') + '.txt'
            filename = os.path.join(newdir, filename)
            print('Saving Backup ' + command, end='')
            with open(filename, 'w') as out_file:
                out_file.write(connection.send_command(command) + '\n')
        print('\nSaved Successfully')
        connection.disconnect()
    except netmiko_exceptions as error:
        print('Failed to ', device['ip'], error)