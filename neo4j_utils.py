from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth = ("neo4j", "password"))
session = driver.session(database="academicworld")

def get_uni(university_name):
    with driver.session(database="academicworld") as tx:
        result = tx.run(""" 
        MATCH (institute:INSTITUTE where institute.name CONTAINS $filter)<-[:AFFILIATION_WITH]->(faculty:FACULTY) WITH institute.name AS university_name, COUNT(DISTINCT faculty) AS faculty_count RETURN university_name, faculty_count ORDER BY faculty_count DESC
        """, filter = university_name)
        return result.to_df()

def get_ratio(university_name):
    with driver.session(database="academicworld") as tx:
        result = tx.run(""" 
MATCH (institute:INSTITUTE)<-[:AFFILIATION_WITH]->(faculty:FACULTY)-[:PUBLISH]->(publication:PUBLICATION) WITH institute AS university, (COUNT(DISTINCT publication)/COUNT(DISTINCT faculty)) as Publ_to_Faclty_Ratio RETURN university.name, Publ_to_Faclty_Ratio ORDER BY Publ_to_Faclty_Ratio DESC LIMIT $filter
        """, filter = university_name)
        return result.to_df()
    
def pandas_df(tx):
    result = tx.run("UNWIND range(1, 10) AS n RETURN n, n+1 AS m")
    return result.to_df()

#driver.close()

if __name__ == '__main__':
    result = get_ratio(5)
    #res2 = get_uni("Michigan")
    #result = pandas_df(get_ratio(5))
    print(result['Publ_to_Faclty_Ratio'])

'''
with driver.session(database="academicworld") as session:  
    people = session.execute_read(  
        get_uni, 
        "University", 
    )
    for person in people:
        print(person.data())  # obtain dict representation


        
'''

