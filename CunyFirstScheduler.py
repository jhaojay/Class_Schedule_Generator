import pymysql

def find_combination(db_name, course_list):
    combination = {}

    conn = pymysql.connect(host='localhost',
                           user='root', passwd='murasaki', db='mysql', charset='utf8')
    cur = conn.cursor()
    cur.execute("USE {}".format(db_name))

    cur.execute("SELECT ClassNum, DaysAndTimes FROM {}".format(course_list[0]))
    data_1 = cur.fetchall()
    class_1_dic = {}

    for index in range(len(data_1)):
        class_1_dic[data_1[index][0]] = parse_day_time_str(data_1[index][1])

    for i in range(1, len(course_list)):
        cur.execute("SELECT ClassNum, DaysAndTimes FROM {}".format(course_list[i]))
        data_2 = cur.fetchall()

        class_2_dic = {}
        for index in range(len(data_2)):
            class_2_dic[data_2[index][0]] = parse_day_time_str(data_2[index][1])

        combination.clear()
        for key_1, value_1 in class_1_dic.items():
            for key_2, value_2 in class_2_dic.items():
                if not conflict(value_1, value_2):
                    combination[key_1+','+key_2] = value_1 + value_2

        class_1_dic.clear()
        class_1_dic = combination.copy()

    combination_class_nbr = [];
    for key in combination:
        combination_class_nbr.append(key)

    cur.close()
    conn.close()
    return combination_class_nbr

def conflict(periods_list_1, periods_list_2):
    for i in range(len(periods_list_1)):
        for j in range(len(periods_list_2)):
            period_list_1 = periods_list_1[i].split(',')
            period_list_2 = periods_list_2[j].split(',')
            if period_list_1[0] == period_list_2[0]:
                if period_list_1[1] > period_list_2[1]:
                    if period_list_1[1] <= period_list_2[2]:
                        return True
                elif period_list_1[1] < period_list_2[1]:
                    if period_list_1[2] >= period_list_2[1]:
                        return True
                else:
                    return True
    return False

def parse_day_time_str(raw_day_time_str):
    raw_day_time_list = raw_day_time_str.split('<br>')
    parsed_day_time_list = []

    for raw_day_time_s in raw_day_time_list:
        parsed_time_str = ''
        raw_day_str = raw_day_time_s.split(' ')[0]
        raw_time_str = raw_day_time_s.split(raw_day_str)[1].strip()
        for time_s in raw_time_str.split('-'):
            time_s = time_s.strip()
            hr = time_s.split(':')[0]
            min = time_s.split(':')[1]

            if "AM" in min and int(hr) < 12:
                hr = '0' + hr
            elif "PM" in min and "12" not in hr:
                hr = str(12+int(hr))

            parsed_time_str = parsed_time_str + hr + min + ','
        parsed_time_str = parsed_time_str.replace(':','')[:-1]
        parsed_time_str = parsed_time_str.replace("AM", '')
        parsed_time_str = parsed_time_str.replace("PM", '')


        index = 0
        for i in range(int(len(raw_day_str)/2)):
            parsed_day_str = raw_day_str[index : index+2]
            parsed_day_time_list.append(parsed_day_str + ',' + parsed_time_str)
            index = index + 2

    return parsed_day_time_list


# stri = 'Mo 9:30AM - 12:15PM'
# result = parse_day_time_str(stri)
# print (result)

# convert to 'Mo 0930 - 1215'