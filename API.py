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
        MERGE (n:User $props)
        MERGE (n:User $props)
        RETURN n
        """
        result = session.run(query, props=props)
        record = result.single()
        return record
    
#Creación de relaciones entre usuarios, géneros, actores y directores

def create_user_like_relation(username, otherNodeName, otherNodeLabel, rel_props):
    with driver.session() as session:
        query = f"""
        MATCH (n:User) where n.username = $username
        MATCH (m:{otherNodeLabel}) where m.name = $otherNodeName
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
def get_directors():
    with driver.session() as session:
        #Obtener los directores más populares
        query = f"""
        MATCH (n:Director) 
        -[:DIRECTED]->
        (m:Movie) 
        where m.rating >= 8.0 
        return n.name;
        """
        result = session.run(query)
        record = result.data()
        return record

#Obtener información sobre los actores
def get_actors():
    with driver.session() as session:
        #Obtener los actores más populares
        query = f"""
        MATCH (n:Actor) 
        -[r:ACTED_IN]->
        (m:Movie) 
        where m.rating >= 8.0
        and r.order < 3
        return n.name;
        """
        result = session.run(query)
        record = result.data()
        return record

def get_user_preferences(username):
    with driver.session() as session:
        query = """
        MATCH (u:User {username: $username})-[r:LIKES]->(p)
        RETURN type(r) AS rel_type, labels(p) AS node_type, p.name AS name
        """
        result = session.run(query, username=username)
        return result.data()

def check_user_exists(username):
    with driver.session() as session:
        query = """
        MATCH (u:User {username: $username})
        RETURN u.username AS username
        """
        result = session.run(query, username=username)
        record = result.single()
        return record is not None

def get_movie_recommendations(username):
    with driver.session() as session:
        # Verificar si el usuario tiene preferencias
        check_query = """
        MATCH (u:User {username: $username})-[:LIKES]->()
        RETURN COUNT(*) AS count
        """
        result = session.run(check_query, username=username)
        count = result.single()["count"]

        if count == 0:
            return ["No tienes preferencias guardadas. Ve a 'Preferencias' y selecciona géneros, actores y directores."]

        # Generar recomendaciones basadas en las preferencias del usuario
        query = """
        MATCH (u:User {username: $username})-[:LIKES]->(pref)
        MATCH (m:Movie)-[:HAS_GENRE|HAS_ACTOR|HAS_DIRECTOR]->(pref)
        RETURN m.title AS movie, COUNT(pref) AS score
        ORDER BY score DESC
        LIMIT 10
        """
        result = session.run(query, username=username)
        recommendations = [record["movie"] for record in result]

        return recommendations if recommendations else ["No se encontraron recomendaciones. Intenta seleccionar más preferencias."]
#Método para verificar la existencia de un usuario
def check_user(username):
    with driver.session() as session:
        query = f"""
        MATCH (n:User {{username: $username}})
        RETURN n.username, n.password
        """
        result = session.run(query, username=username)
        record = result.data()
        return record

    


