import os
import re

from bs4 import BeautifulSoup

import config
import requests

import senator


class Scraper:
    def __init__(self):
        self.lend_link = config.lend_link
        self.dir_personal_links = r"files/personal_links"
        self.base_link = config.base_link
        self.personal_links = []
        self.soup = None
        self.file_dir = "pers_files/"
        self.new_senator = None
        self.all_senators = {}
        self.id = ""

    def save_links(self):
        temp_str = ""
        for link in self.personal_links:
            temp_str += ("|" + link)
        temp_str = temp_str[0:]
        f = open(self.dir_personal_links, "w")
        f.write(temp_str)
        f.close()

    def parse_people_link(self):
        res = []
        counter = 0
        try:
            soup = BeautifulSoup(requests.get(self.lend_link).text, "html.parser")
            a_s = soup.find_all("a", attrs={"class": {"group__persons__item", "group__persons__item_with_photo"}})
            for a in a_s:
                # <a itemprop="url" class="person__title__link link link--color
                if a is not None and a.get("href") is not None:
                    links = a.get("href")
                    res.append(links)
                else:
                    print(a)
            print(counter)
            self.personal_links = res

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {self.lend_link} - {e}")

    def parse_links_from_files(self):
        try:
            f = open(self.dir_personal_links, "r")
            self.personal_links = f.read().split("|")
            self.personal_links.pop(0)
            f.close()
        except Exception:
            print(f"Can't open {self.dir_personal_links}")

    @staticmethod
    def get_id(link):
        return link.split("/")[-2]

    @staticmethod
    def clear_text(text):
        text = text.replace("\n", "").replace("\xa0", " ").replace("  ", " ").replace("\t", "")
        while text.find("  ") != -1:
            text = text.replace("  ", " ")
        if len(text) > 0:
            while text[0] == " ":
                text = text[1:]
            while text[-1] == " ":
                text = text[:-1]
        return text

    @staticmethod
    def correct_date(date):
        res = ""
        for i in range(3):
            if i!=2:
                date[i] = (2 - len(str(date[i])))*"0"+str(date[i])
            res += ("-"+date[i])
        return res[1:]

    def parse_files(self):
        for link in self.personal_links:
            print(self.base_link + link)
            soup = BeautifulSoup(requests.get(self.base_link+link).text, "html.parser")
            #print(self.file_dir + self.get_id(link) + ".html")
            with open(self.file_dir + self.get_id(link) + ".html", "w") as f:
                f.write(soup.text)

    def parse_all_files(self):
        list_dir = os.listdir("pers_files")

        for file in list_dir:
            file_ad = "pers_files/"+file
            with open(file_ad, "r") as f:
                self.soup = BeautifulSoup(f.read(), "html.parser")
            self.id = file.split(".")[0]
            self.parse_one_person()
            self.all_senators[self.id]=self.new_senator

    def parse_one_person(self):
        self.new_senator = senator.Senator()
        self.new_senator.id = self.id
        self.parse_fio()
        self.parse_region()
        self.parse_post()
        self.parse_dates()
        self.parse_contacts()
        self.parse_biography()
        self.new_senator.to_json()
        self.new_senator.to_cort()
        f = open("output.txt", "a")
        f.write("\n"+self.id+"\n"+self.new_senator.json_deputat)
        f.close()
        self.all_senators[self.new_senator.id] = self.new_senator.data

    def parse_fio(self):
        h2 = self.soup.find("h2", class_="senators_title")
        if h2 != None:
            fio = h2.find("span").text.split(" ")
            self.new_senator.f, self.new_senator.i = fio[0], fio[1]
            if len(fio) > 2:
                self.new_senator.o = fio[2]
        #print(fio)

    @staticmethod
    def get_month(text):
        month = 0
        match text[:3]:
            case "янв":
                month = 1
            case "фев":
                month = 2
            case "мар":
                month = 3
            case "апр":
                month = 4
            case "май":
                month = 5
            case "июн":
                month = 6
            case "июл":
                month = 7
            case "авг":
                month = 8
            case "сен":
                month = 9
            case "окт":
                month = 10
            case "ноя":
                month = 11
            case "дек":
                month = 12
            case _:
                month = 0
        return month

    @staticmethod
    def clear_numbers(data):
        return re.sub('\D', '', data)

    #person_info_private tooltip__wrapper
    def parse_dates(self):
        block = self.soup.find("div", class_="person__additional_info")
        p_s = block.find("div", attrs={"class":{"person_info_private", "tooltip__wrapper"}}).findAll("p")
        for p in p_s:
            res = self.clear_text(p.text).split(" ")
            match res[1]:
                case "рождения:":
                    self.new_senator.date_birth = self.correct_date([res[2], self.get_month(res[3]), res[4]])
                    #print(self.new_senator.date_birth)
                case "наделения":
                    self.new_senator.start_date = self.correct_date([res[3], self.get_month(res[4]), res[5]])
                    #print(self.new_senator.start_date)
                case "Срок":
                    self.new_senator.end_date = res[5]+" "+res[6]
                    #print(self.new_senator.end_date)

    def parse_contacts(self):
        self.conts = self.soup.findAll("div", class_="person__contacts")
        if len(self.conts) == 0:
            print(self.new_senator.id + " не имеет контактов")
        else:
            p_s = self.conts[0].findAll("p")
            for p in p_s:
                p_text = self.clear_text(p.text)
                match p_text.split(" ")[0]:
                    case "Телефон:":
                        #print(self.clear_numbers(p_text.split(":")[1]))
                        self.new_senator.telephone = self.clear_numbers(p_text.split(":")[1])
                    case "Адрес":
                        #print(self.clear_text(p_text.split(":")[1]))
                        self.new_senator.adress = self.clear_text(p_text.split(":")[1])
                    case "Телефон":
                        #print(self.clear_numbers(p_text.split(":")[1]))
                        self.new_senator.telephone_fax = self.clear_numbers(p_text.split(":")[1])
                    case _:
                        print("##########################", p_text.split(" ")[0], sep="\n")

    def parse_post(self):
        div = self.soup.find("div", class_="person__additional_top")
        self.new_senator.post = self.clear_text(div.getText().replace("VK", "").replace("Телеграм", "").replace("Одноклассники", ""))
        ul = div.find("ul")
        if ul is not None:
            lis = ul.findAll("li")
            for li in lis:
                res = {
                    "soc_net": self.clear_text(li.find("a").text),
                    "link": li.find("a").get("href")
                }
                self.new_senator.social_links.append(res)
        #print(self.new_senator.post)
        #print(self.new_senator.social_links)

    def parse_region(self):
        self.new_senator.region = self.clear_text(self.soup.find("a", class_="region_name_link").text)
        #print(self.new_senator.region)
    def parse_biography(self):
        bio = self.soup.find("div", class_="person__biography")

        if bio is None:
            return ""

        h4 = bio.findAll("h4")
        div = bio.findAll("div", class_="biography_block")

        for i in range(len(h4)):
            match self.clear_text(h4[i].text):
                case "Образование:":
                    p_s = div[i].findAll("p")
                    for p in p_s:
                        p_text = self.clear_text(p.text).split(" - ", maxsplit=1)
                        if self.clear_text(p.text).find("(") != -1:
                            res = {
                                "university": self.clear_text(p_text[1].split("(")[0]),
                                "specialization": self.clear_text(p_text[1].split("(")[1].split(")")[0]),
                                "year": self.clear_numbers(p_text[0])
                            }
                        else:
                            res = {
                                "university": self.clear_text(p_text[1]),
                                "year": self.clear_numbers(p_text[0])
                            }
                        self.new_senator.education.append(res)
                    #print(self.new_senator.education)
                case "Государственные награды:":
                    p_s = div[i].findAll("p")
                    for p in p_s:
                        p_text = self.clear_text(p.text).split(" - ", maxsplit = 1)
                        self.new_senator.rewards.append({
                            "reward": self.clear_text(p_text[1]),
                            "year": self.clear_numbers(p_text[0])
                        })
                    #print(self.new_senator.rewards)
                case "Ученые степени:":
                    p_s = div[i].findAll("p")
                    for p in p_s:
                        self.new_senator.academic_degrees.append(self.clear_text(p.text))
                    #print(self.new_senator.academic_degrees)
                case "Должность перед избранием (назначением):":
                    p_s = div[i].findAll("p")
                    for p in p_s:
                        self.new_senator.previos_post.append(self.clear_text(p.text))
                    #print(self.new_senator.previos_post)
                case "Ученые звания:":
                    p_s = div[i].findAll("p")
                    for p in p_s:
                        self.new_senator.academic_rewards.append(self.clear_text(p.text))
                    #print(self.new_senator.academic_rewards)
                case _:
                    print("####################################################################\n", self.clear_text(h4[i].text))