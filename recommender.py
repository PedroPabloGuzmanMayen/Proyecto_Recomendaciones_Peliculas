from neo4j import GraphDatabase

#Conxión a la db

URI = "neo4j+s://4cb369a6.databases.neo4j.io"
USERNAME = "neo4j"
PASSWORD = "cl36WyQYuOYK-8D4TGKqy6DW8uN3bjC0TNdmPKl7MEw"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


def check_gds_version(tx):
    result = tx.run("RETURN gds.version()")
    return result.single()[0]

with driver.session() as session:
    version = session.read_transaction(check_gds_version)
    print(f"GDS Version: {version}")