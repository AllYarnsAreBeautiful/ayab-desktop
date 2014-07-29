import ConfigParser
## https://docs.python.org/2/library/configparser.html

config = ConfigParser.SafeConfigParser()

config.add_section("Arduino Uno")
config.add_section("Arduino Mega 2560")

config.set("Arduino Uno", "latest", "uno/ayab_uno_latest.hex")
config.set("Arduino Uno", "v3", "uno/v3/ayab_uno_v3.hex")
config.set("Arduino Uno", "v3_dummy", "uno/v3/ayab_uno_v3_dummy.hex")
config.set("Arduino Mega 2560", "latest", "mega/ayab_mega_latest.hex")
config.set("Arduino Mega 2560", "v3", "mega/v3/ayab_mega_v3.hex")
config.set("Arduino Mega 2560", "v3_dummy", "mega/v3/ayab_mega_dummy.hex")

with open('example_repo.cfg', 'wb') as configfile:
  config.write(configfile)
