from jps_api_wrapper.classic import Classic
from jamf_auth import (
    JamfAuthException,
    AuthResponseConnectionError,
    AuthResponseWasNotValid,
)

from . import config, exceptions, records


class Server:
    """
    Class that allows talking to a server
    """

    def __init__(
        self,
        config_obj=None,
        config_path=None,
        hostname=None,
        username=None,
        password=None,
        prompt=False,
    ):
        """ """
        self.config = config_obj or config.Config(
            config_path=config_path,
            hostname=hostname,
            username=username,
            password=password,
            prompt=prompt,
        )
        if (
            not self.config.hostname
            and not self.config.username
            and not self.config.password
        ):
            raise exceptions.JamfConfigError(
                "No jamf hostname or credentials could be found."
            )
        classic = None
        try:
            classic = Classic(
                self.config.hostname, self.config.username, self.config.password
            )
        except AuthResponseConnectionError:
            print("Could not connect to " + self.config.hostname)
            exit()
        except JamfAuthException:
            print("Incorrect username or password for " + self.config.hostname)
            exit()
        except AuthResponseWasNotValid:
            print("Some error for " + self.config.hostname)
            exit()
        records.set_classic(classic)
        self.records = records
