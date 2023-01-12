import CunyFirstParser
import pymysql
import time
import os


def save_course_details(folder_name):
    t0 = time.time()
    conn = pymysql.connect(host='localhost',
                           user='root', passwd= 'murasaki', db='mysql', charset='utf8')
    cur = conn.cursor()
    dbname = time.strftime("course_details_%Y%m%d%H")
    #dbname = "course_details"
    cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(dbname))
    cur.execute("USE {}".format(dbname))

    path = os.getcwd() + "\\" + folder_name

    parser = CunyFirstParser.CunyFirstParser()
    for school_file in os.listdir(path):
        school_name = os.fsdecode(school_file).replace(' ','_')
        cur.execute(
            "CREATE TABLE {} ("
            "CourseAbbrev VARCHAR(100),"
            "CourseName VARCHAR(100) NOT NULL,"
            "Units VARCHAR(100) NOT NULL,"
            "ClsComponent VARCHAR(100) NOT NULL,"
            "Career VARCHAR(100) NOT NULL,"
            "Description TEXT NOT NULL)".format(school_name)
        )
        for term_file in os.listdir(path+'\\'+school_file):
            for subject_file in os.listdir(path+'\\'+school_file+'\\'+term_file):
                for course_file in os.listdir(path+'\\'+school_file+'\\'+term_file+'\\'+subject_file):
                    file = path+'\\'+school_file+'\\'+term_file+'\\'+subject_file+'\\'+course_file
                    print(file)
                    course_details = parser.parse_course_details(file)

                    cur.execute(
                        "INSERT INTO {} (CourseAbbrev, CourseName, Units, ClsComponent, Career, Description)"
                        "VALUES ('{}','{}','{}','{}','{}','{}')"
                        .format(school_name, course_details[0], course_details[1].replace("'", "''"),
                                course_details[2], course_details[3], course_details[4], course_details[5].replace("'", "''"))
                    )


    conn.commit()
    cur.close()
    conn.close()
    t1 = time.time()
    print(t1-t0)


def save_classes_info(folder_name):
    conn = pymysql.connect(host='localhost',
                           user='root', passwd='murasaki', db='mysql', charset='utf8')
    cur = conn.cursor()

    path = os.getcwd() + "\\" + folder_name

    try:
        cur.execute("DROP DATABASE {}".format(folder_name))
        cur.execute("CREATE DATABASE {}".format(folder_name))
    except:
        #cur.execute("DROP DATABASE {}".format(folder_name))
        cur.execute("CREATE DATABASE {}".format(folder_name))

    cur.execute("USE {}".format(folder_name))

    parser = CunyFirstParser.CunyFirstParser()
    for course_file in os.listdir(path):
        course_abbreviation = os.path.splitext(course_file)[0]
        cur.execute(
            "CREATE TABLE {} ("
            "Name VARCHAR(100) NOT NULL,"
            "Abbrev VARCHAR(100) NOT NULL,"
            "ClassNum VARCHAR(100) PRIMARY KEY,"
            "Section VARCHAR(100) NOT NULL,"
            "DaysAndTimes TINYTEXT NOT NULL,"
            "Room TINYTEXT NOT NULL,"
            "Instructor TINYTEXT NOT NULL,"
            "MeetingDates TINYTEXT NOT NULL,"
            "Status VARCHAR(100) NOT NULL)".format(course_abbreviation)
        )
        file = path+ '\\'+ course_file
        class_info = parser.parse_classes_info(file)
        for key, values in class_info.items():
            for value in values:
                try:
                    cur.execute(
                        "INSERT INTO {} "
                        "(Name, Abbrev, ClassNum, Section, DaysAndTimes,"
                        " Room, Instructor, MeetingDates, Status)"
                        "VALUES "
                        "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                        .format(course_abbreviation, key, value[0], value[1], value[2], value[3], value[4], value[5].replace("'", "''"), value[6], value[7])
                    )
                except pymysql.err.IntegrityError:
                    pass

    conn.commit()
    cur.close()
    conn.close()


# save_classes_info("phi")