from pprint import pprint, pformat
from swagbot.core import BasePlugin
import re
import swagbot.starwars_database as swdb
import swagbot.utils as utils

class Plugin(BasePlugin):
	def __init__(self, bot):
		self.methods = self.__setup_methods()
		BasePlugin.__init__(self, bot)

	def starwars(self, command=None):
		if command:
			term = command.command_args
			if term:
				table = command.command["name"].replace("starwars-", "")
				output = swdb.query(table=table, term=term)
				if output:
					if len(output) > 0:
						output = self.__clean_output(output)
						utils.make_success(command, content=pformat(output))
					else:
						utils.make_error(command, content="No records found matching the specified search criteria.")
				else:
					utils.make_error(command, content="Failed to query the Star Wars database. Please try again later.")
			else:
				utils.make_error(command, content=["No search term specified.", "Usage: {}".format(command.command["usage"])])
		else:
			utils.make_error(command, content="An unknown error has occurred.")

	def __clean_output(self, output=None):
		# Later we'll try to convert "int" to int and "float" to float
		to_array = [
			"characters",
			"films",
			"people",
			"pilots",
			"planets",
			"residents",
			"species",
			"starships",
			"vehicles",
		]
		for record in output:
			for k, v in record.items():
				if k in to_array:
					if v == None:
						record[k] = []
					else:
						record[k] = re.split(",", v)
			else:
				if v != None:
					record[k] = v
		return output

	def __setup_methods(self):
		return {
			"starwars-films": {
				"usage": "films <term> -- Search for a Star Wars film.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"method": "starwars",
				"monospace": 1,
			},
			"starwars-people": {
				"usage": "films <term> -- Search for a Star Wars character.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"method": "starwars",
				"monospace": 1,
			},
			"starwars-planets": {
				"usage": "films <term> -- Search for a Star Wars planet.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"method": "starwars",
				"monospace": 1,
			},
			"starwars-species": {
				"usage": "films <term> -- Search for a Star Wars species.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"method": "starwars",
				"monospace": 1,
			},
			"starwars-starships": {
				"usage": "films <term> -- Search for a Star Wars starship.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"method": "starwars",
				"monospace": 1,
			},
			"starwars-vehicles": {
				"usage": "films <term> -- Search for a Star Wars vehicle.",
				"level": 0,
				"type": "all",
				"can_be_disabled": 1,
				"hidden": 0,
				"method": "starwars",
				"monospace": 1,
			},
		}