import CunyFirstScraper
import import_MySQL
import CunyFirstScheduler
import xlwings as xw
import string


def scrap (school, term, crs_list, folder_name):
    sub_list = []
    nbr_list = []
    for item in crs_list:
        sub_list.append(item[:item.find('_')])
        nbr_list.append(item[item.find('_') + 1:])

    # scraper = CunyFirstScraper.CunyFirstScraper('headless')
    scraper = CunyFirstScraper.CunyFirstScraper()
    scraper.login(username, pw)
    scraper.get_courses(school, term, sub_list, nbr_list, folder_name)
    scraper.quit()

def write_to_excel(result, name):
    wb = xw.Book(name+".xlsm")
    ws = wb.sheets[0]
    ws.range("A2").value = len(result)
    for i in range(len(result)):
        cell = string.ascii_uppercase[i] + '1'
        ws.range(cell).value = result[i]
    wb.save()

folder_name = "phi1"
school = 'City College'
term = "2019 Spring Term"
crs_list = ['EE_30600', 'EE_25900', 'EE_42500', 'EE_34400', 'EE_32300']
crs_list.sort()

scrap(school, term, crs_list, folder_name)
import_MySQL.save_classes_info(folder_name)
result = CunyFirstScheduler.find_combination(folder_name, crs_list)
print(result)
write_to_excel(result, folder_name)

# delete existing scaper's folder
# change "folder_name" in this program
# change Templet excel name to match the folder_name
# change "crs_list" to the courses you want to take
# run this program
# open excel to create an empty sheet and import data in the order of
# [Sheet1, TempletSheet, EE_25900, EE_32200, etc...]
# go to the TempletSheet to click the button
# delete the button
