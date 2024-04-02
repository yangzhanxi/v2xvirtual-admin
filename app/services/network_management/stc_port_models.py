class StcPort(object):
    """
    This class is used to store the STC port information.
    """

    def __init__(self,
                 name: str,
                 handle: str,
                 link_status: str,
                 auto_negotiation: bool,
                 auto_negotiation_role: str,
                 duplex_mode: str,
                 line_speed: str):
        self.__name = name
        self.__handle = handle
        self.__link_status = link_status
        self.__auto_negotiation = auto_negotiation
        self.__auto_negotiation_role = auto_negotiation_role
        self.__duplex_mode = duplex_mode
        self.__line_speed = line_speed

    @property
    def name(self) -> str:
        return self.__name

    @property
    def handle(self) -> str:
        return self.__handle

    @property
    def link_status(self) -> str:
        return self.__link_status

    @property
    def auto_negotiation(self) -> str:
        return self.__auto_negotiation

    @property
    def auto_negotiation_role(self) -> str:
        return self.__auto_negotiation_role

    @property
    def duplex_mode(self) -> str:
        return self.__duplex_mode

    @property
    def line_speed(self) -> str:
        return self.__line_speed
