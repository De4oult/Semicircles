from functions import initialize, download

import click

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)

@cli.command()
def init(): # init workspace
    initialize()

@cli.command()
@click.argument('name')
def get(name): # get package from 
    download(name)

if __name__ == '__main__':
    cli(obj={})