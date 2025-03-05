from neo4j import GraphDatabase

# Conexión a la db
URI = "neo4j+s://4cb369a6.databases.neo4j.io"
USERNAME = "neo4j"
PASSWORD = "cl36WyQYuOYK-8D4TGKqy6DW8uN3bjC0TNdmPKl7MEw"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


def compute_movie_similarity():
    """Crea relaciones SIMILAR_A entre películas basadas en ratings de usuarios con GDS"""
    with driver.session() as session:
        query = """
        CALL gds.nodeSimilarity.write({
            nodeProjection: 'Movie',
            relationshipProjection: {
                RATED_BY: {
                    type: 'RATES',
                    properties: 'rating',
                    orientation: 'UNDIRECTED'
                }
            },
            similarityMetric: 'cosine',
            writeRelationshipType: 'SIMILAR_A',
            writeProperty: 'score'
        })
        """
        session.run(query)
        print("✅ Similitud entre películas calculada y guardada en Neo4j!")


if __name__ == "__main__":
    compute_movie_similarity()

