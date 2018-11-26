import re

from . import utils
from .keyword import SCPIKeyword, SCPIKeywordList
from .parameter import SCPIParameter, SCPIParameterList


class SCPICommand():
    def __init__(self, scpi_string, action, name="", description=""):
        scpi_string = utils.sanitize(scpi_string)
        self._action = action
        self._description = description
        self._keyword_string, self._parameter_string = utils.create_command_tuple(scpi_string)
        self._keyword_list = SCPIKeywordList(self._keyword_string)
        self._parameter_list = SCPIParameterList(self._parameter_string)
        self._scpi_string = self._keyword_string + " " + self._parameter_string
        if name:
            self._name = name
        else:
            self.name = self._keyword_string
        self._is_query = self._keyword_string.endswith("?")

    def __repr__(self):
        ret = "\n"
        for key, val in self.__dict__.items():
            ret = ret + str(key) + ": " + str(val) + "\n"
        return str(ret)

    def __str__(self):
        return self._scpi_string

    def get_action_name(self):
        return self._action.__name__

    def get_keyword_string(self):
        return self._keyword_string

    def get_keyword_list(self):
        return self._keyword_list

    def get_parameter_string(self):
        return self._parameter_string
    
    def get_parameter_list(self):
        return self._parameter_list

    def get_parameter_string_list(self):
        parameter_string_list = list()
        for parameter in self.get_parameter_list():
            parameter_string_list.append(parameter.get_parameter_string())
        return parameter_string_list

    # def add_parameter(self, 
    #         name, 
    #         optional="False", 
    #         value_list=list(), 
    #         default=None, 
    #         parameter_string=""):
    #     """Add a parameter at the end of the parameter list."""
    #     self._parameter_list.append(
    #         SCPIParameter(
    #             name=name, 
    #             optional=optional, 
    #             value_list=value_list, 
    #             default=default, 
    #             parameter_string=parameter_string,
    #     ))

    def execute_if_match(self, command_string):
        """Execute the attached action if the ``command_string`` matches the 
        commands syntax. The first parameter will alwas be the full 
        ``command_string``. After that, a list of parsed parameters will 
        follow."""
        command_string = utils.sanitize(command_string, False)
        if not self.match(command_string):
            return None
        return self.execute(command_string)

    def execute(self, command_string):
        """Execute the attached action. The first parameter will alwas be the 
        full ``command_string``. After that, a list of parsed parameters will 
        follow."""
        keyword_string, parameter_string = utils.create_command_tuple(command_string)
        args = list()
        args.append(command_string)
        if parameter_string:
            args = args + parameter_string.split(",")
        # Todo: create a named list, which corresponds to parameter names 
        # defined in the command creation string.
        kwargs = dict()
        return self._action(*args, **kwargs)

    def is_query(self):
        return self._is_query

    def match(self, command_string):
        """Return ``True`` if ``command_string`` matches the instance's 
        keyword AND parameters. ``False`` otherwise."""
        keyword_string, parameter_string = utils.create_command_tuple(command_string)
        matches_keyword = self.match_keyword(keyword_string)
        matches_parameter = self.match_parameters(parameter_string)
        return matches_keyword and matches_parameter

    def match_keyword(self, keyword_string):
        """Return ``True`` if ``keyword_string`` matches the instances 
        keyword. ``False`` otherwise."""
        keyword_string = keyword_string.lower()
        # Check if the command is a query. If True, remove the trailing '?'.
        if keyword_string.endswith("?"):
            if self.is_query():
                keyword_string = keyword_string.replace("?", "")
            else:
                return False
        elif self.is_query():
            return False

        # Split keywords into a test string list against which each keyword 
        # will be tested.
        test_string_list = keyword_string.split(":")

        # Iterate over all keywords. Leave the procedure as soon as a mismatch 
        # is detected. When the loop finishes ordinarily, the matching was 
        # succesful.
        keyword_i = 0
        for keyword in self.get_keyword_list():
            if keyword_i >= len(test_string_list):
                if not keyword.is_optional():
                    return False
                continue
            test_string = test_string_list[keyword_i]
            req_string = keyword[0].lower()
            opt_string = req_string + keyword[1].lower()
            if not test_string.startswith(req_string):
                if keyword.is_optional():
                    continue
                else:
                    return False
            if not opt_string.startswith(test_string):
                return False
            keyword_i += 1
        if keyword_i < len(test_string_list):
            return False
        return True

    def match_parameters(self, test_string):
        test_string = utils.sanitize(test_string, remove_all_spaces=True)
        test_parameter_string_list = test_string.split(",")
        pos = 0
        n_test_parameter = len(test_parameter_string_list)
        for parameter in self.get_parameter_list():
            if pos >= n_test_parameter:
                if not parameter.is_optional():
                    return False
                continue
            test = test_parameter_string_list[pos]
            if not parameter.match(test):
                return False
            pos += 1
        return True


class SCPICommandList(list):
    def __init__(self):
        list.__init__(self)
