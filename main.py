# author Pavel Baranek

# libraries needed:
import requests
import csv
from bs4 import BeautifulSoup as BS

def welcome():
    separator = (100 * "*")
    print(separator)
    print((20 * " ") + "----> Welcome here in our election scraper app! <----")
    print(separator)
    print("""
Here you will get the results of elections in year 2017 for selected region. 
You have to choose one region from the following link: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ 
On the web page choose the name of the region (by clicking on "X") and then copy the link.
""")
    print(separator)

def get_link():
    link = input("Enter the link here please: ")
    if "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=" in link and "&xnumnuts=" in link:
        return link
    else:
        print("Wrong url, get the right link and try it again please!")
        quit()

def get_name():
    separator = (100 * "*")
    name = input("""Please name your file in wich we will save the data
(it will automatically safe in CSV format, so don't specify the suffix please): 
""")
    if ".csv" not in name:
        print(separator)
        print("Getting it done... please wait")
        print(separator)
        return name
    else:
        print("Don't add suffix, to the file name please, try it again")
        quit()

def download_data(link):
    page = requests.get(link)
    whole_page = BS(page.text, "html.parser")
    return whole_page

def get_headers_data(tr):
    tds = tr.find_all("td")
    id = tds[0].getText()
    village = tds[1].getText()
    link_ = tds[0].find("a").get("href")
    return id, village, link_

def data_to_dict(header_data):
    id, village, link_ = header_data
    link_base = "https://volby.cz/pls/ps2017nss/" + link_
    soup = download_data(link_base)
    tables = soup.find_all("table")
    cells = tables[0].find_all("td")
    data_dict = {"ID": id, "Village": village, "Voters": cells[3].getText(), "Envelopes": cells[6].getText(),
                 "Votes Total": cells[7].getText()}

    for table in tables[1:]:
        trs = table.find_all("tr")
        for tr in trs[2:-1]:
            tds = tr.find_all("td")
            name_of_party = tds[1].getText()
            total_votes = tds[2].getText()
            data_dict[name_of_party] = total_votes
    return data_dict

def data_to_list(soup):
    villages_ = soup.find_all("div", {"class": "t3"})
    data_list = []
    for table in villages_:
        all_rows = table.find_all("tr")
        for row in all_rows[2:]:
            data_list.append(data_to_dict(get_headers_data(row)))
        return data_list


def main():
    welcome()
    separator = (100 * "*")
    link = get_link()
    print(separator)
    file_name = get_name()
    soup = download_data(link)
    data_list = data_to_list(soup)
    with open(file_name + ".csv", "w", newline="") as file:
        header = data_list[0].keys()
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(data_list)

    print(f"Done! Now you can find your data in {file_name}.csv. Thank you for using our app, Bye")
    print(separator)


main()