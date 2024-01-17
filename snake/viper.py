import auror.parameter
import skriba.logger
import skriba.console

from rich.console import Console
from rich.table import Table

from typing import Union, List, NoReturn


def ascii_snake(color: Union[str, List, None] = None):
    if color:
        skriba.logger.info("Printing a cute snake in 24-bit color.")
        colorize = skriba.console.Colorize()
        with open("snake/ascii/snek.txt") as snake:
            print(colorize.format(text=snake.read(), color=color))

    else:
        skriba.logger.info("Printing a cute snake in terminal.")
        with open("snake/ascii/snek.txt") as snake:
            print(snake.read())


def print_logger_levels(verbose: bool = False):
    skriba.logger.info("This is an info message.", verbose=verbose)
    skriba.logger.debug("This is an debug message.", verbose=verbose)
    skriba.logger.warning("This is an warning message.", verbose=verbose)
    skriba.logger.error("This is an error message.", verbose=verbose)
    skriba.logger.critical("This is an critical error message.", verbose=verbose)


class SnakeObject:
    def __new__(cls, **kwargs):
        if kwargs:
            for name, value in kwargs.items():
                setattr(cls, name, value)

        return super(SnakeObject, cls).__new__(cls)

    def __init__(self, object_name, **kwargs):
        self.object_name = object_name

    def __str__(self):
        return self.object_name

    def print(self, all: bool = False):
        for key in dir(self):
            if not all:
                if not key.startswith("__"):
                    print(f"{key}: {getattr(self, key)}")

            else:
                if not key.startswith("__"):
                    print(f"{key}: {getattr(self, key)}")


@auror.parameter.validate(
    logger=skriba.logger.get_logger(logger_name="viper-logger"),
    add_data_type=SnakeObject
)
def snake_object_danger_checker(number: int, snake_info: SnakeObject) -> Union[float, NoReturn]:
    species_score = {
        'viper': "Run",
        'cobra': 'Run fast!',
        'mamba': 'You\'re dead just give up...',
        'garden': 'More scared of you.'
    }

    if snake_info.species not in species_score.keys():
        print("Unknown species. Run.")
        snake_info.print()
        return None

    table = Table(title="Snake Danger Checker: Object Edition")
    table.add_column("Species", justify="right", style="cyan")
    table.add_column("Number", justify="center", style="green")
    table.add_column("Poison", justify="center", style="magenta")
    table.add_column("Score", justify="center", style="red")

    table.add_row(
        SnakeObject.species,
        str(SnakeObject.number),
        str(SnakeObject.poison),
        species_score[SnakeObject.species]
    )

    console = Console()
    console.print(table)


@auror.parameter.validate(
    logger=skriba.logger.get_logger(logger_name="viper-logger")
)
def snake_danger_checker(number: int, poison: bool, species: str) -> Union[int, NoReturn]:
    species_score = {
        'viper': "Run",
        'cobra': 'Run fast!',
        'mamba': 'You\'re dead just give up...',
        'garden': 'More scared of you.'
    }

    if species not in species_score.keys():
        print("Unknown species. Run.")
        return None

    table = Table(title="Snake Danger Checker")
    table.add_column("Species", justify="right", style="cyan")
    table.add_column("Number", justify="center", style="green")
    table.add_column("Poison", justify="center", style="magenta")
    table.add_column("Score", justify="center", style="red")

    table.add_row(species, str(number), str(poison), species_score[species])

    console = Console()
    console.print(table)

