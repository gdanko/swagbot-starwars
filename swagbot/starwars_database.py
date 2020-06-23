import os
import sqlite3

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

def _dict_factory(cursor, row):
	d = {}
	for idx,col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def quote_list(l):
	return ",".join(["\'{}\'".format(x) for x in l])

def query(table=None, term=None):
	ids = find_ids(table=table, term=term)
	output = query_ids(table=table, ids=ids)
	return output

def find_ids(table=None, term=None):
	ids = []
	key = "title" if table == "films" else "name"
	select = "SELECT id FROM {} WHERE {} LIKE '%{}%'".format(table, key, term)
	res = cursor.execute(select)
	for row in res:
		ids.append(row["id"])
	return sorted(ids)

def query_ids(table=None, ids=None):
	output = []
	if table == "films":
		for id in ids:
			rows = query_films(id=id)
			for row in rows:
				output.append(row)
		
	elif table == "people":
		for id in ids:
			rows = query_people(id=id)
			for row in rows:
				output.append(row)

	elif table == "planets":
		for id in ids:
			rows = query_planets(id=id)
			for row in rows:
				output.append(row)

	elif table == "species":
		for id in ids:
			rows = query_species(id=id)
			for row in rows:
				output.append(row)

	elif table == "starships":
		for id in ids:
			rows = query_starships(id=id)
			for row in rows:
				output.append(row)

	elif table == "vehicles":
		for id in ids:
			rows = query_vehicles(id=id)
			for row in rows:
				output.append(row)

	return output

def query_films(id=None):
	rows = []
	select = """SELECT *,
		(SELECT GROUP_CONCAT(character_name)
			FROM
			(
				SELECT people.name AS character_name FROM films
				INNER JOIN films_people ON films_people.film_id = films.id
				INNER JOIN people on films_people.person_id = people.id
				WHERE films.id={id}
				GROUP BY films.id,people.name
			)
		) as characters,
		(SELECT GROUP_CONCAT(planet_name)
			FROM
			(
				SELECT planets.name AS planet_name FROM films
				INNER JOIN films_planets ON films_planets.film_id = films.id
				INNER JOIN planets on films_planets.planet_id = planets.id
				WHERE films.id={id}
				GROUP BY films.id,planets.name
			)
		) as planets,
		(SELECT GROUP_CONCAT(starship_name)
			FROM
			(
				SELECT starships.name AS starship_name FROM films
				INNER JOIN films_starships ON films_starships.film_id = films.id
				INNER JOIN starships on films_starships.starship_id = starships.id
				WHERE films.id={id}
				GROUP BY films.id,starships.name
			)
		) as starships,
		(SELECT GROUP_CONCAT(vehicle_name)
			FROM
			(
				SELECT vehicles.name AS vehicle_name FROM films
				INNER JOIN films_vehicles ON films_vehicles.film_id = films.id
				INNER JOIN vehicles on films_vehicles.vehicle_id = vehicles.id
				WHERE films.id={id}
				GROUP BY films.id,vehicles.name
			)
		) as vehicles,
		(SELECT GROUP_CONCAT(species_name)
			FROM
			(
				SELECT species.name AS species_name FROM films
				INNER JOIN films_species ON films_species.film_id = films.id
				INNER JOIN species on films_species.species_id = species.id
				WHERE films.id={id}
				GROUP BY films.id,species.name
			)
		) as species
		FROM films
		WHERE films.id={id}""".format(id=id)
	res = cursor.execute(select)
	for row in res:
		rows.append(row)
	return rows

def query_people(id=None):
	rows = []
	select = """SELECT *,
		(SELECT GROUP_CONCAT(film_title)
			FROM
			(
				SELECT films.title AS film_title FROM people
				INNER JOIN films_people ON films_people.person_id = people.id
				INNER JOIN films on films_people.film_id = films.id
				WHERE people.id={id}
			)
		) as films,
		(SELECT GROUP_CONCAT(species_name)
			FROM
			(
				SELECT species.name AS species_name FROM people
				INNER JOIN people_species ON people_species.person_id = people.id
				INNER JOIN species on people_species.species_id = species.id
				WHERE people.id={id}
			)
		) as species,
		 (SELECT GROUP_CONCAT(starship_name)
			FROM
			(
				SELECT starships.name AS starship_name FROM people
				INNER JOIN people_starships ON people_starships.person_id = people.id
				INNER JOIN starships on people_starships.starship_id = starships.id
				WHERE people.id={id}
			)
		) as starships,
		  (SELECT GROUP_CONCAT(vehicle_name)
			FROM
			(
				SELECT vehicles.name AS vehicle_name FROM people
				INNER JOIN people_vehicles ON people_vehicles.person_id = people.id
				INNER JOIN vehicles on people_vehicles.vehicle_id = vehicles.id
				WHERE people.id={id}
			)
		) as vehicles
		FROM people
		WHERE people.id={id}""".format(id=id)
	res = cursor.execute(select)
	for row in res:
		rows.append(row)
	return rows

def query_planets(id=None):
	rows = []
	select="""SELECT *,
		(SELECT GROUP_CONCAT(person_name)
			FROM
			(
				SELECT people.name AS person_name FROM planets
				INNER JOIN planets_people ON planets_people.planet_id = planets.id
				INNER JOIN people on planets_people.person_id = people.id
				WHERE planets.id={id}
			)
		) as residents,
		  (SELECT GROUP_CONCAT(film_title)
			FROM
			(
				SELECT films.title AS film_title FROM planets
				INNER JOIN films_planets ON films_planets.planet_id = planets.id
				INNER JOIN films on films_planets.film_id = films.id
				WHERE planets.id={id}
			)
		) as films
		FROM planets
		WHERE planets.id={id}""".format(id=id)
	res = cursor.execute(select)
	for row in res:
		rows.append(row)
	return rows

def query_species(id=None):
	rows = []
	select = """SELECT *,
		(SELECT GROUP_CONCAT(person_name)
			FROM
			(
				SELECT people.name AS person_name FROM species
				INNER JOIN people_species ON people_species.species_id = species.id
				INNER JOIN people on people_species.person_id = people.id
				WHERE species.id={id}
			)
		) as people,
		  (SELECT GROUP_CONCAT(film_title)
			FROM
			(
				SELECT films.title AS film_title FROM species
				INNER JOIN films_species ON films_species.species_id = species.id
				INNER JOIN films on films_species.film_id = films.id
				WHERE species.id={id}
			)
		) as films
		FROM species
		WHERE species.id={id}""".format(id=id)
	res = cursor.execute(select)
	for row in res:
		rows.append(row)
	return rows

def query_starships(id=None):
	rows = []
	select = """SELECT *,
		(SELECT GROUP_CONCAT(person_name)
			FROM
			(
				SELECT starships.id,starships.name,people.name AS person_name
				FROM starships
				INNER JOIN people_starships ON people_starships.starship_id = starships.id
				INNER JOIN people ON people_starships.person_id = people.id
				WHERE starships.id={id}
				GROUP BY starships.id,person_name
			)
		) AS pilots,

		(SELECT GROUP_CONCAT(film_title)
			FROM
			(
				SELECT starships.id,starships.name,films.title AS film_title
				FROM starships
				INNER JOIN films_starships ON films_starships.starship_id = starships.id
				INNER JOIN films ON films_starships.film_id = films.id
				WHERE starships.id={id}
				GROUP BY starships.id,film_title
			)
		) AS films
		FROM starships
		WHERE starships.id={id}""".format(id=id)
	res = cursor.execute(select)
	for row in res:
		rows.append(row)
	return rows

def query_vehicles(id=None):
	rows = []
	select = """SELECT *,
		(SELECT GROUP_CONCAT(person_name)
			FROM
			(
				SELECT vehicles.id,vehicles.name,people.name AS person_name
				FROM vehicles
				INNER JOIN people_vehicles ON people_vehicles.vehicle_id = vehicles.id
				INNER JOIN people ON people_vehicles.person_id = people.id
				WHERE vehicles.id={id}
				GROUP BY vehicles.id,person_name
			)
		) AS pilots,

		(SELECT GROUP_CONCAT(film_title)
			FROM
			(
				SELECT vehicles.id,vehicles.name,films.title AS film_title
				FROM vehicles
				INNER JOIN films_vehicles ON films_vehicles.vehicle_id = vehicles.id
				INNER JOIN films ON films_vehicles.film_id = films.id
				WHERE vehicles.id={id}
				GROUP BY vehicles.id,film_title
			)
		) AS films
		FROM vehicles
		WHERE vehicles.id={id}""".format(id=id)
	res = cursor.execute(select)
	for row in res:
		rows.append(row)
	return rows

dbfile = "{}/data/starwars.db".format(PACKAGE_ROOT)
conn = sqlite3.connect(dbfile, check_same_thread=False)
conn.row_factory = _dict_factory
cursor = conn.cursor()