# Graph Viper Logger and Verification Tools

## Environment creation
We will be creating a fresh environment using `conda`. Other nice options are `miniconda` and `mamba`. To create a fresh
environment we can run.

```angular2html
conda create --name viper python=3.11 --no-default-packages
conda activate viper
```
The packages being present are supported for python version 3.8-3.11, so pick your favorite. 

Next we install the two packages that we will be previewing today, both are available on pypi. Both packages are active, 
quick development therefore they will change fairly often. Once testing is finished to the degree that a stable release 
is available, both packages will be rolled into the `greaphviper` framework as tools. 

```angular2html
python -m pip install auror skriba
```

## Skriba Logger 

The logger is designed to be easy to use with a number of ways to be instantiated. Generally, simple python loggers 
created with the python `logging` module require a bit of setup and a call to `logging.get_logger()` when first called
in a function. While this usage is still available in the new logger, the option for much of this to be obfuscated is 
available. The following are ways in which the logger can be initialized.

#### Logger Setup

- The logger can be setup in the usual way be creating an instance of using the `setup_logger()` method:
    ```angular2html
    import skriba.logger
  
    skirba.logger.setup_logger(
        logger_name = "viper-logger",
        log_to_term=True,
        log_to_file=True,
        log_file="viper-log-file",
        log_level=DEBUG
    )    
  ```
  the logger can then be retrieved using
  ```angular2html
  logger = skriba.logger.get_logger(logger_name="viper-logger")
  ```
  This is the standard implementation method I see in notebooks. One way to do this by default, this is the way it is 
  done in `astrohack` currently, this setup can just be done in the `__init__.py` of your package. An example of this is 
  can be seen in the tutorial code. 

- The logger can also just be called be directly importing and calling the logger module. This will give you a default 
  logger instance, ie. Logging to terminal only, the `logger_name` defaults to "logger", there is no log file and the 
  logging level is set to "INFO". For instance if you go to terminal and call
  
  ```angular2html
  import skirba.logger 
  
  skriba.logger.info("This is a log message").
  ```
  you will get a default logging message with no extra work. Since this method creates a default logging instance it is
  also possible to just get the instance and change the level to customize as you wish.
  ```angular2html
  log_instance = skriba.logger.get_logger()
  log_instance.setLevel("DEBUG")
  ```
  With this, the logger will now print debug messages as well.
  
The logger included the standard logging levels, all of which can be called in the same way as above. All logging calls 
include a verbose option as well that will pull the calling function information from the call stack and include it in
log message.

```angular2html
import snake

snake.viper.print_logger_levels(verbose=True)
```

As a note, only the terminal outputs include color and formatting options. The log file creation is handled by a separate
log handler and does not include and escape sequences.

#### General Terminal Formatting
The logger includes and additional package that allows the user to include a number of text formatting options to the 
logger or print output, including 24-bit color (for supported terminals) options. A list of available options are shown 
below and an example notebook will be included in the tutorial.

Instantiating the class `Colorize()`

```
import skriba.console

colorize = skriba.consoleColorize()
```

the following method options are available:
- bold(text: str)
- faint(text: str)
- italics(text: str)
- underline(text: str)
- blink(text: str)
- highlight(text: str) 
- white(text: str)
- black(text: str)
- grey(text: str)
- red(text: str)
- green(text: str)
- yellow(text: str)
- orange(text: str) 
- blue(text: str)
- purple(text: str)
- alert(text: str)
- format(
     text: str
     color: Union[str, List],
     bold: bool = False,
     italics: bool = False,
     faint: bool = False,
     underline: bool = False,
     highlight: bool = False,
     blink: bool = False
  )

To use any of these options simply wrap the text in the function and the escape codes will be added.

## Auror Parameter Verification
The `auror` parameter verification package is built as an extension of the [cerberus](https://docs.python-cerberus.org/)
framework and has been built into a simple to implement function decorator. Once a function is wrapped in a decorator it 
is checked against a json configuration file stored in the place of the users choosing; it is recommended that the file 
be included in a config directory within the package but any directory *should* work.

### Configuration

As with the logger, `auror` needs some initialization; in this case it needs know where the configuration files are. There 
are a few ways to provide this. The configuration files should be in a single directory together and names according to
`function_name.param.json`. The verification works for both general function and class members, the code can tell the 
difference and proceed accordingly. 

- <u>Configuration directory parameter:</u>
  The simplest way to get the configuration files to `auror` is to pass it directly as a parameter.
  
  ```angular2html
  import auror.parameter
  
  @auror.parameter.validate(
    config_dir="/path/tp/config/"
  )
  def some_function(x:int, y: float, z: float):
    ...
  ```
  with this `auror` will parse the configuration file for the function if it finds it in the destination and throw and 
  exception if there is a failure.

If the configuration directory is not given the code will do with try two different options, checking for an environment 
variable location and doing a simple file search in a couple of standard locations before failing.

- <u>Setting up an environment variable collection</u>
  
  A simple and easy way to make sure the configuration files are found is to set up an environment variable specifying the
  configuration path. When checking this `auror` will assume a path variable according to the format of the standard linux
  PATH variable, `PATH=$PATH:/path/to/package-a/config:/path/to/pacakge-b/config`. If the path variable is found, the 
  code will parse the path and do a search in each path for the specified functions configuration file. The environment 
  variable option could be setup in fashion similar to the logger.

  ```angular2html
  __init__.py:
  
  if pathlib.Path(__file__).parent.resolve().joinpath("config").exists():
    # If environment variable not set
    if not os.environ.get("AUROR_CONFIG_PATH"):
        os.environ["AUROR_CONFIG_PATH"] = str(pathlib.Path(__file__).parent.resolve().joinpath("config"))

    # If the environment variable does exist and is not in the list, append it
    else:
        if str(pathlib.Path(__file__).parent.resolve().joinpath("config")) not in os.environ["AUROR_CONFIG_PATH"]:
            os.environ["AUROR_CONFIG_PATH"] = os.environ["AUROR_CONFIG_PATH"] + \
                                              ":" + str(pathlib.Path(__file__).parent.resolve().joinpath("config"))
  ```
  
In this way the environment variable can be used for multiple packages without tripping over each other. The 
code **does require that the environment variable be named "AUROR_CONFIG_PATH"**.

- <u>Path search</u>
  
  If both of the above options fail to produce a configuration file the code will do a directory search in two specific 
  locations, first it will look in the current path for the `src/` directory, if it exists, and then do a top-down search
  looking for the configuration file for the functions that was wrapped. This is mostly useful for developer installs. 
  Second, it will look in the `site-packages/` directory of the associated module and do a similar search there before 
  giving up and throwing an error.

### Implementation Example

The parameter checking is applied to any function decorated with the function `auror.paramter.validate(...)`. The verification
function has the following input parameters available. 

- `config_dir`: This specifies the configuration directory
- `logger`: This allows teh user to pass a specific logger instance to the parameter checking. If this is not done, `auror`
  will spawn its own internal logger. The only difference will be the logger name in the output.
- `add_data_type`: Not all data types are available from teh default setup more importantly though there are a number of 
  instance in the framework(s) where custom data objects are passed to function and there needs to be a way to check these 
  as well. This allows the user to register a custom data ype for checking. All that is needed if to pass an instance of 
  the data type.
- `custom_checker`: This allows the user to register a function that will return all allowed data types for a parameter.

Taking the example from the code, to implement the verification on the `snake_danger_checker(...)` function, assuming the 
configuration directory is set up in `__init__.py`:

### Standard Function Implementation:
```angular2html
import auror.parameter

@auror.parameter.validate
def snake_danger_checker(number: int, poison: bool, species: str)->Union[int, NoReturn]:
    ...
```

The configuration file for this would be as follows (though the user could add more layers)

```angular2html
snake/config/viper.param.json:

{
  "snake_danger_checker":{
    "number": {
      "required": true,
      "type": ["int"]
    },
    "poison": {
      "required": true,
      "type": "boolean"
    },
    "species": {
      "required": true,
      "type": "string"
    }
  }
```

If this was a checker on a class method the only change to be made would be that that function name would change to 
`ClassName.snake_danger_checker`.

This is only a very sparse version of a configuration file, the requirements can be made quite strict with some work. A 
full list of supported parameter checks at [cerberus::validation](https://docs.python-cerberus.org/validation-rules.html). 
In addition, `auror` also supports:

- Custom data types: `ndarray` is supported by default in `auror` and any valid data type can be registered.
- Custom checking function
- Sequence validation
- Structure data type

The framework is fully extensible so additional checks can be added without too much work.

### Function with Custom Data Implementation:

Extending our previous example, let's say we have a custom data object that we can use to dynamically store snake 
information, and we want to pass this instead. If we define the object as follows,

```angular2html
snake_info = snake.viper.SnakeObject(
    object_name="snake-info-list", 
    poison=True, 
    species="cobra", 
    color="brown", 
    angry=True
)
```

We can use this in a modified snake checking function and verify it by simply passing an instance of the `SnakeObject` to
the validation using the `add_data_type` parameter.

```angular2html
@auror.parameter.validate(
    logger=skriba.logger.get_logger(logger_name="viper-logger"),
    add_data_type=SnakeObject
)
def snake_object_danger_checker(number: int, snake_info: SnakeObject) -> Union[float, NoReturn]:
    ...
```

### Custom Data Checker

This option is for the case that the user wants to define a function that will use some sort of custom logic to decide the
acceptable values for a given parameter and then return them to the validation scheme. The vest example of this is in `astrohack`
where some of the plotting functions have a different set of acceptable units depending on the plot being made, therefore 
we want a easily modifiable list of units that can be returned instead of hard-coding each function separately. The primary 
requirement for a custom checking function is that it take a string parameter and return a list of acceptable values to 
check against. In the case of `astrohack` this was a list of acceptable plotting units depending on whether teh function 
needs trigonometric, time or radian units. The custom check function in this case was,

```angular2html
def custom_unit_checker(unit_type):
    if unit_type == "units.trig":
        return trigo_units

    elif unit_type == "units.length":
        return length_units

    elif unit_type == "units.time":
        return time_units

    else:
        return "Not found"
```

where the units are defined in a constants module as,

```angular2html
# Length units
length_units = ['km', 'mi', 'm', 'yd', 'ft', 'in', 'cm', 'mm', 'um', 'mils']

# Trigonometric units
trigo_units = ['rad', 'deg', 'hour', 'asec', 'amin']

# Time units
time_units = ['nsec', 'usec', 'msec', 'sec', 'min', 'hour', 'day']
```

In order to add this to the plotting function

```angular2html
 @auror.parameter.validate(
        logger=logger.get_logger(logger_name="astrohack"),
        custom_checker=custom_unit_checker
    )
    def plot_array_configuration(
            self,
            destination: str,
            stations: bool = True,
            zoff: bool = False,
            unit: str = 'm',
            box_size: Union[int, float] = 5000,
            display: bool = False,
            figure_size: Union[Tuple, List[float], np.array] = None,
            dpi: int = 300
    ) -> None:
    ...
```

and in the configuration file this function has teh following parameter check for the unit parameter,

```angular2html
...
    "unit":{
            "nullable": false,
            "required": false,
            "type": ["string"],
            "check allowed with": "units.length"
    },
...
```
  






