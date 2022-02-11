from loguru import logger


class Logger:
    """
    General Logger class to output debug messages in the specific scope
    """

    def __init__(self,
                 scope_name: str,
                 indentation_level: int = 2,
                 log_level: str = 'debug'
                 ):
        self.scope_name = scope_name
        self.indentation_level = indentation_level
        self.log_level = log_level

        self.indentation = ' ' * 4 * self.indentation_level

    def log(self,
            message: str,
            log_level: str = None
            ) -> None:
        """
        The main method to log messages with specified log level or log level of the
        current Logger object. Messages are formatted in the next way:
            [<scope of the logger>]: <message>

        Possible values of 'log_level' argument are (in order of increasing log severity):
            ['trace', 'debug', 'info', 'success', 'warning', 'error', 'critical']
        """
        if log_level is None:
            log_level = self.log_level
        log_function = getattr(logger, log_level)
        log_message = f"{self.indentation}[{self.scope_name}]: {message}"
        log_function(log_message)
