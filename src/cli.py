#Mikrotik to smarthseet dumper CLI code
#2022
#Angelo.poggi@opti9tech.com

import click
from common.env_creator import create_env_file
from src.mikrotikclass import *


@click.group(
    help="Simple tool to dump a firewall into Smartsheet"
)
def cli():
    pass

@cli.command()
def generate_env_file():
    return create_env_file()

@cli.command()
@click.option(
    '--client' , '-c', help="Clients name",
    required=True,
    type=str
)
@click.option(
    '--firewall' , '-f', help="Firewall you want to dump",
    required=True,
    type = str
)
def dumpIPs(client,firewall):
    mikrotik = mtinit(client,firewall)
    return mikrotik.dumpIPs()

@cli.command()
@click.option(
    '--client' , '-c', help="Clients name",
    required=True,
    type=str
)
@click.option(
    '--firewall' , '-f', help="Firewall you want to dump",
    required=True,
    type = str
)
def dumproutes(client,firewall):
    mikrotik = mtinit(client,firewall)
    return mikrotik.dumproutes()

@cli.command()
@click.option(
    '--client' , '-c', help="Clients name",
    required=True,
    type=str
)
@click.option(
    '--firewall' , '-f', help="Firewall you want to dump",
    required=True,
    type = str
)
def dumpfilters(client,firewall):
    mikrotik = mtinit(client, firewall)
    return mikrotik.dumpfilters()

@cli.command()
@click.option(
    '--client' , '-c', help="Clients name",
    required=True,
    type=str
)
@click.option(
    '--firewall' , '-f', help="Firewall you want to dump",
    required=True,
    type = str
)
def dumpNats(client,firewall):
    mikrotik = mtinit(client, firewall)
    return mikrotik.dumpNats()

@cli.command()
@click.option(
    '--client' , '-c', help="Clients name",
    required=True,
    type=str
)
@click.option(
    '--firewall' , '-f', help="Firewall you want to dump",
    required=True,
    type = str
)
def dumpAddrLists(client,firewall):
    mikrotik = mtinit(client, firewall)
    return mikrotik.dumpAdrLists()

@cli.command()
@click.option(
    '--client' , '-c', help="Clients name",
    required=True,
    type=str
)
@click.option(
    '--firewall' , '-f', help="Firewall you want to dump",
    required=True,
    type = str
)
def dumpipsecPh1(client,firewall):
    mikrotik = mtinit(client, firewall)
    return mikrotik.dumpipsecPh1()

@cli.command()
@click.option(
    '--client' , '-c', help="Clients name",
    required=True,
    type=str
)
@click.option(
    '--firewall' , '-f', help="Firewall you want to dump",
    required=True,
    type = str
)
def dumph1Profile(client,firewall):
    mikrotik = mtinit(client, firewall)
    return mikrotik.dumpipsecPh1Profile()

@cli.command()
@click.option(
    '--client' , '-c', help="Clients name",
    required=True,
    type=str
)
@click.option(
    '--firewall' , '-f', help="Firewall you want to dump",
    required=True,
    type = str
)
def dumpipsecph2(client,firewall):
    mikrotik = mtinit(client, firewall)
    return mikrotik.dumpIpsecPh2()

@cli.command()
@click.option(
    '--client' , '-c', help="Clients name",
    required=True,
    type=str
)
@click.option(
    '--firewall' , '-f', help="Firewall you want to dump",
    required=True,
    type = str
)
def dumpall(client,firewall):
    mikrotik = mtinit(client, firewall)
    return mikrotik.dumpAll()










