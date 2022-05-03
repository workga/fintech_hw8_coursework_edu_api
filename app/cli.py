import click
import asyncio

from app.database.utils import recreate_db, create_admin


loop = asyncio.get_event_loop()


@click.command('recreate-db')
@click.option('--testing', is_flag=True)
def cli_recreate_db(testing: bool) -> None:
    loop.run_until_complete(recreate_db(testing))


@click.command('create-admin')
@click.option('--testing', is_flag=True)
@click.argument('email')
@click.argument('password')
def cli_create_admin(email: str, password: str,  testing: bool) -> None:
    loop.run_until_complete(create_admin(email, password, testing))



@click.group()
def cli_handler():
    pass


cli_handler.add_command(cli_recreate_db)
cli_handler.add_command(cli_create_admin)


if __name__ == '__main__':
    cli_handler()