import logging
import time
import threading
import scpidev

FORMAT = "%(levelname)s: %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
# logging.basicConfig(format=FORMAT, level=logging.INFO)

# Define our action functions
def test_function(*args, **kwargs):
    print("## Execute: {} ##".format(repr(kwargs["command_string"])))
    i = 0
    for arg in args:
        # time.sleep(1)
        print("Got arg {}: {}".format(str(i), repr(arg)))
        i += 1
    return i

def test_function2(test):
    print("## Execute. ##" + str(test))

def idn(*args, **kwargs):
    return "SCPIDevice,0.0.1a"

def rst(*args, **kwargs):
    print("Clear device history")
    dev.clear_alarm(clear_history=True)

# Define some test command strings
command_strings = [
    # "*RST",
    # "*IDN?",
    "MEASure:CURRent[:DC]? [{<range>|AUTO|MIN|MAX|DEF} [,{<resolution>|MIN|MAX|DEF}] ]",
    "MEASure[:VOLTage][:DC]? [{<range>|AUTO|MIN|MAX|DEF} [,{<resolution>|MIN|MAX|DEF}] ]",
    "[SENSe:]VOLTage[:DC]:NULL[:STATe] {ON|OFF}",
    ":VOLTage[:DC]:NULL[:STATe] {ON|OFF}",
    "CALCulate:FUNCtion {NULL | DB | DBM | AVERage | LIMit}",
    """
    MEASure[:VOLTage][:DC]? 
        [{<range>|AUTO|MIN|MAX|DEF} [, {<resolution>|MIN|MAX|DEF}] ]
    """,
]

# Define some test commands, which will be sent to our device
test_commands = [
    # "*RST",
    # "*IDN?",
    "CONF AUTO",
    "MEAS:CURREnt? 10 A, MAX",
    "XXX?",
]

# Create the instance of our SCPI device
dev = scpidev.SCPIDevice(
    name="My SCPI Device",
)

dev.add_command("*IDN?", idn)
dev.add_command("*RST", rst)

# Create commands
for cmd in command_strings:
    dev.add_command(
        scpi_string=cmd,
        action=test_function,
    )

# Crate the communication interfaces
dev.create_interface("tcp")
dev.create_interface("udp")
dev.create_interface("serial", port="COM7", baudrate="500000", dsrdtr=1)

# Start the server thread but kill it after some time
# t = threading.Thread(target=dev.run)
# t.start()
# time.sleep(2)
# dev.stop()
# t.join()

# Start the server thread and wait until program is terminated (ctrl+c).
t = threading.Thread(target=dev.run)
t.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    dev.stop()
exit()

# try:
#     dev.run()
# except KeyboardInterrupt:
#     dev.stop()
#     exit()
