#helps to create env file
#2021 - Angelo Poggi : angelo.poggi@webair.com
import click


def create_env_file():
    """Creates the .env file which stores the firewalls username and password"""
    username = input("please enter username of the firewall\n")
    password = input("please enter password of the firewall\n")
    smart_token = input("please enter your smartsheet access token\n")
    smart_workspace = input("please enter the workspace ID in smartsheet\n")
    with open('.env', 'w') as envFile:
        envFile.write(f'MIKROTIK_USERNAME={username}\n')
        envFile.write(f'MIKROTIK_PASSWORD={password}\n')
        envFile.write(f'SMARTSHEET_ACCESS_TOKEN={smart_token}\n')
        envFile.write(f'WORKSPACE_ID={smart_workspace}\n')
    click.echo(".env file generated, you should now be able to run the script against a firewall!")