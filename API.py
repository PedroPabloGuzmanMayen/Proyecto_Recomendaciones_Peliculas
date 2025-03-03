from neo4j import GraphDatabase

#Conxión a la db

URI = "neo4j+s://4cb369a6.databases.neo4j.io"
USERNAME = "neo4j"
PASSWORD = "cl36WyQYuOYK-8D4TGKqy6DW8uN3bjC0TNdmPKl7MEw"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


#CRUD

#Creación de usuarios
def create_User(props):
    with driver.session() as session:
        query = f"""
        CREATE (n:User $props)
        RETURN n
        """
        result = session.run(query, props=props)
        record = result.single()
        return record
    
#Creación de relaciones entre usuarios, géneros, actores y directores

def create_user_like_relation(username, otherNodeName, otherNodeLabel, rel_props):
    with driver.session() as session:
        query = f"""
        MATCH (n:User {{username: $username}})
        MATCH (m:{otherNodeLabel} {{name: $otherNodeName}})
        MERGE (n)-[r:LIKES]->(m)
        SET r += $rel_props
        RETURN n, r, m
        """
        result = session.run(query, 
                             username=username,  
                             otherNodeName=otherNodeName, 
                             rel_props=rel_props)
        
        record = result.single()
        return record


#Creación de relación entre películas y usuarios
def create_movie_review(username, moviename, rel_props):
    with driver.session() as session:
        query = f"""
        MERGE (n:User {{username: $username}})
        MERGE (m:Movie {{title: $moviename}})
        MERGE (n)-[r:RATES]->(m)
        SET r += $rel_props
        RETURN n, r, m
        """
        result = session.run(query, 
                             username=username,  
                             moviename=moviename, 
                             rel_props=rel_props)
    
        records = result.data()
        return records

#Obtención de información sobre las películas
def get_movies():
    with driver.session() as session:
        query = f"""
        MATCH (n:Movie)
        RETURN n.title, n.releaseDate, n.overview, n.rating, n.poster
        """
        result = session.run(query)
        record = result.data()
        return record
    
#Obtener información sobre los géneros
def get_genres():
    with driver.session() as session:
        query = f"""
        MATCH (n:Genre)
        RETURN n.name
        """
        result = session.run(query)
        record = result.data()
        return record
    
#Obtener información sobre los actores y directores
def get_actors_directors(label):
    with driver.session() as session:
        query = f"""
        MATCH (n:{label})
        RETURN n.name
        """
        result = session.run(query)
        record = result.data()
        return record

print(get_genres())
