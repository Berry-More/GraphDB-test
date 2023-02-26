from neo4j import GraphDatabase
from transliterate import translit


class ObjectDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # Create person
    def create_person(self, person_name):
        with self.driver.session(database='neo4j') as session:
            result = session.execute_write(
                self._create_person, person_name)

    @staticmethod
    def _create_person(tx, person_name):
        query = (
            "CREATE (p:Person {name: $person_name}) "
            "RETURN p"
        )
        result = tx.run(query,
                        person_name=person_name)
        return [{"p": row["p"]["name"], } for row in result]

    # If user exist return 1, else 0
    def is_user_not_exist(self, person_name):
        with self.driver.session(database='neo4j') as session:
            result = session.execute_write(
                self._is_user_not_exist, person_name)
            if len(result) == 0:
                answer = 1
            else:
                answer = 0
            return answer

    @staticmethod
    def _is_user_not_exist(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p"
        )
        result = tx.run(query,
                        person_name=person_name)
        return [{"p": row["p"]["name"]} for row in result]

    # Create event
    def create_event(self, person_name1, person_name2):
        with self.driver.session(database='neo4j') as session:
            result = session.execute_write(
                self._create_event, person_name1, person_name2)

    @staticmethod
    def _create_event(tx, person_name1, person_name2):
        query = (
            "MATCH (p1:Person), (p2:Person) "
            "WHERE p1.name = $person_name1 AND p2.name = $person_name2 "
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
            answer = []
            if len(result) == 0:
                answer.append({'name': 'Not exist'})
            for row in result:
                answer.append({'name': translit(row, language_code='ru', reversed=True)})
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
            "RETURN n.name AS name"
        )
        result = tx.run(query)
        return [row["name"] for row in result]
