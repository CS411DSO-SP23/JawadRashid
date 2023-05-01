import pymysql
from pandas import DataFrame
db = pymysql.connect(host='localhost',
                user='root',
                password='Bl!nk4182',
                database='academicWorld',
                charset='utf8mb4',
                port=3306,
                cursorclass=pymysql.cursors.DictCursor)

#widget 1
def fac_TableCount(input_value):
    with db.cursor() as cursor:
        sql = 'select count(faculty.id), university.name from faculty, university where university.id = faculty.university_id AND university.name like "%' + input_value + '%" GROUP BY university.name ORDER BY count(faculty.id) DESC;'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

#widget 2
def year_pub(range1, range2):
    with db.cursor() as cursor:
        sql = 'select count(publication.id) as Publications, university.name as University from faculty, faculty_publication, publication, university where faculty.id = faculty_publication.faculty_id and faculty_publication.publication_id = publication.id and faculty.university_id = university.id and publication.year BETWEEN ' + range1 + ' AND ' + range2 + ' GROUP BY university.name ORDER BY count(publication.id) DESC LIMIT 5;'
        cursor.execute(sql)
        df = DataFrame(cursor.fetchall())
        return df

#widget 3
def prof_pub(input_value):
    with db.cursor() as cursor:
        sql = 'select count(publication.id) as count, publication.year from faculty, faculty_publication, publication  where faculty.id = faculty_publication.faculty_id and faculty_publication.publication_id = publication.id and faculty.name like "%' + input_value + '%" GROUP BY publication.year  ORDER BY publication.year ASC;'
        cursor.execute(sql)
        df = DataFrame(cursor.fetchall())
        return df

def add_uni(uni_id, uni_name, uni_photo):
    with db.cursor() as cursor:
        sql_constraint = 'ALTER TABLE university MODIFY COLUMN name VARCHAR(512) NOT NULL;'
        cursor.execute(sql_constraint)
        sql = 'INSERT INTO university(id, name, photo_url) VALUES (%s, %s, %s);'
        cursor.execute(sql, (uni_id, uni_name, uni_photo))
        result = cursor.fetchall()
        return result

def del_uni(uni_name):
    with db.cursor() as cursor:
        sql = 'DELETE FROM university WHERE university.name like "%' + uni_name + '%";'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

def chec_uni(input_value):
    with db.cursor() as cursor:
        sql = 'select university.name, university.id, university.photo_url from university where university.name like "%' + input_value + '%";'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    '''
        df = DataFrame(cursor.fetchall())
        return df
        '''
    
if __name__ == '__main__':
    addthis = add_uni("1868", None , "https://test.png")
    result1 = chec_uni("Wayne State University")
    dellthis = del_uni("Wayne State University")
    result = chec_uni("Wayne State University")
    #deletethis = del_uni("test2 university")
    #result2 = chec_uni("test2 university")
    print(result1)
    print('this')
    print(result)
        
    
#select count(publication.id) as Publications, university.name as University from faculty, faculty_publication, publication, university where faculty.id = faculty_publication.faculty_id and faculty_publication.publication_id = publication.id and faculty.university_id = university.id and publication.year BETWEEN "2001" AND "2011" GROUP BY university.name ORDER BY count(publication.id) DESC LIMIT 5;
