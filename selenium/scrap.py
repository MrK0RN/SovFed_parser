import config


class Scraper:
    def __init__(self):
        self.lend_link = config.lend_link
        self.dir_personal_links = r"../personal_links"
        self.base_link = config.base_link
        self.personal_links = []
        self.soup = None
        self.file_dir = "../files/pers_files/"
        self.new_senator = None
        self.all_senators = {}
        self.id = ""


    @staticmethod
    def get_id(link):
        return link.split("/")[-2]

    def parse_links_from_files(self):
        try:
            print(1)
            f = open(self.dir_personal_links, "r")
            self.personal_links = f.read().split("|")
            self.personal_links.pop(0)
            f.close()
        except Exception:
            print(f"Can't open {self.dir_personal_links}")

    @staticmethod
    def save_html_to_file(id, data):
        f = open("pers_files/" + str(id) + ".html", "w")
        f.write(data)
        f.close()