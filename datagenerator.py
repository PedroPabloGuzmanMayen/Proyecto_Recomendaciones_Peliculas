import pandas as pd
from neo4j import GraphDatabase
from datetime import datetime
import ast

#Credenciales de la db en neo4j

URI = "neo4j+s://4cb369a6.databases.neo4j.io"
USERNAME = "neo4j"
PASSWORD = "cl36WyQYuOYK-8D4TGKqy6DW8uN3bjC0TNdmPKl7MEw"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

df = pd.read_csv('archive/merged_movies.csv') #Leer el csv

#Crear los nodos de películas, directores, actores, géneros y sus relaciones

id_genres = 0

df = df[df['vote_count'] > 1200] 


df = df.drop_duplicates(subset=['title'])


def create_node(labelname, props):
    with driver.session() as session:
        query = f"""
        MERGE (n:{labelname} {{id: $id}})
        SET n += $props
        RETURN n
        """
        result = session.run(query, props=props, id=props['id'])
        record = result.single()

def create_movie_genre(label1, rel_label, label2, label1_props, label2_props, rel_props):
    with driver.session() as session:
        query = f"""
        MERGE (n:{label1} {{id: $id1}})
        MERGE (m:{label2} {{id: $id2}})
        MERGE (n)-[r:{rel_label}]->(m)
        SET r += $rel_props
        RETURN n, r, m
        """
        result = session.run(query, 
                             id1=label1_props['id'],  
                             id2=label2_props['id'], 
                             rel_props=rel_props)
        
        record = result.single()



def create_movie_actor(label1, rel_label, label2, label1_props, label2_props, rel_props):
    with driver.session() as session:
        query = f"""
        MERGE (n:{label1} {{id: $id1}})
        MERGE (m:{label2} {{id: $id2}})
        MERGE (n)-[r:{rel_label}]->(m)
        SET r += $rel_props
        RETURN n, r, m
        """
        
        result = session.run(query, 
                             id1=label1_props['id'],  
                             id2=label2_props['id'], 
                             rel_props=rel_props)
        
        record = result.single()



for row in df.itertuples():
    movie_props = {"title": row.title, "releaseDate": pd.to_datetime(row.release_date), 
                    "rating": row.vote_average, "original_language": row.original_language,
                    "runtime": row.runtime, "overview": row.overview, 
                    "poster": row.poster_path, "id": row.id}
    create_node("Movie", movie_props)

    for genre in ast.literal_eval(row.genres):
        genre_props = {"name": genre['name'], "id": genre['id'], "date_created": datetime.now(), "likes":0, "description": "hello world"}
        create_node("Genre", genre_props)
        rel_props = {"date_created": datetime.now(), "id_relation": id_genres, "updated_at": datetime.now()}
        create_movie_genre("Movie", "BELONGS_TO", "Genre", movie_props, genre_props, rel_props)
        id_genres += 1

    for actor in ast.literal_eval(row.cast):
        
        actor_props = {"name": actor['name'], "id": actor['id'], "date_created": datetime.now(), "likes":0, "profie": actor["profile_path"],
                       "gender": actor['gender']}
        create_node("Actor", actor_props)
        rel_props = {"date_created": datetime.now(), "id_relation": actor['cast_id'], "character": actor['character'], "order": actor['order']}
        create_movie_actor("Actor", "ACTED_IN", "Movie", actor_props, movie_props, rel_props)


    for director in ast.literal_eval(row.crew):
        if director['department'] == 'Directing':
            director_props = {"name": director['name'], "id": director['id'], "date_created": datetime.now(), 
                              "likes":0, "profie": director["profile_path"], "gender": director["gender"]}
            create_node("Director", director_props)
            rel_props = {"date_created": datetime.now(), "id_relation": director['credit_id'], "job": director['job']}
            create_movie_actor("Director", "DIRECTED", "Movie", director_props, movie_props, rel_props)
        

#Similitudes entre películas usando los géneros, actores y directores. 

def create_movie_similarity():
    pass


driver.close()

print("Proceso terminado")










