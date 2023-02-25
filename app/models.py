from neo4j import GraphDatabase
from transliterate import translit


class ObjectDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # Create event
    def create_event(self, person_name1, person_name2):
        with self.driver.session(database='neo4j') as session:
            result = session.execute_write(
                self._create_event, person_name1, person_name2)

    @staticmethod
    def _create_event(tx, person_name1, person_name2):
        query = (
            "CREATE (p1:Person { name: $person_name1 }) "
            "CREATE (p2:Person { name: $person_name2 }) "
            "CREATE (p1)-[:CONNECT]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query,
                        person_name1=person_name1,
                        person_name2=person_name2)
        return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]} for row in result]

    # Find connect partner
    def find_connect(self, person_name):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(self._find_conn_return_person,
                                          person_name)
            if len(result) == 0:
                answer = {'name': 'Not exist'}
            for row in result:
                answer = [{'name': translit(person_name, language_code='ru', reversed=True),
                           'partner': translit(row, language_code='ru', reversed=True)}]
            return answer

    @staticmethod
    def _find_conn_return_person(tx, person_name):
        query = (
            "MATCH (:Person {name: $person_name})-[:CONNECT]-(z:Person) "
            "RETURN z.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]

    # Get all users
    def get_all(self):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(self._get_all)
            return [{'name': row} for row in result]

    @staticmethod
    def _get_all(tx):
        query = (
            "MATCH (n:Person) "
            "RETURN n.name AS name LIMIT 50"
        )
        result = tx.run(query)
        return [row["name"] for row in result]
