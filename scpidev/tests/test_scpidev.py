import logging
import re

import scpidev

# logging.basicConfig(level=logging.DEBUG)

def test_function(text):
    print("Test function, {}".format(str(text)))

cmd_str = "MEASure[:VOLTage][:DC]? [{<range>|AUTO|MIN|MAX|DEF} [,  {<resolution>|MIN|MAX|DEF}] ]"
cmd_str = "MEASure:CURRent[:DC]? [{<range>|AUTO|MIN|MAX|DEF} [,{<resolution>|MIN|MAX|DEF}] ]"
# cmd_str = "[SENSe:]VOLTage[:DC]:NULL[:STATe] {ON|OFF}"
# cmd_str = ":VOLTage[:DC]:NULL[:STATe] {ON|OFF}"
# cmd_str = "CALCulate:FUNCtion {NULL | DB | DBM | AVERage | LIMit}"
cmd_str = """
  :MEASure:VRMS 
    [<interval>{CYCLe | DISPlay}]
    [,]
    [<type>{AC | DC}]
    [,]
    [<source>{CHANnel<n> | FUNCtion | MATH | WMEMory<r>}]
"""
# """
# MEASure[:VOLTage][:DC]? 
#     [{<range>|AUTO|MIN|MAX|DEF} [, {<resolution>|MIN|MAX|DEF}] ]
# """

cmd = scpidev.SCPICommand(cmd_str, test_function)
# cmd.execute("moinsen")
print(cmd._scpi_string)
print(cmd._keyword_string)
print(cmd._parameter_string)
# print(cmd)
