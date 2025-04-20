import json


class Senator:

    def __init__(self):
        self.json_deputat = None
        self.id = ""
        self.f = ""
        self.i = ""
        self.o = None
        self.region = ""
        self.date_birth = ""
        self.start_date = ""
        self.end_date = ""
        self.post = ""
        self.social_links = []
        self.telephone = ""
        self.adress = []
        self.telephone_fax = ""
        self.education = []
        self.rewards = []
        self.academic_degrees = []
        self.previos_post = []
        self.academic_rewards = []
        self.data = {}

    def to_cort(self):
        self.data = {"f": self.f,
                "i": self.i,
                "o": self.o,
                "region": self.region,
                "birth_date": self.date_birth,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "post": self.post,
                "social_networks": self.social_links,
                "telephone": self.telephone,
                "address": self.adress,
                "telephone_and_fax": self.telephone_fax,
                "education": self.education,
                "rewards": self.rewards,
                "academic_degrees": self.academic_degrees,
                "academic_rewards": self.academic_rewards,
                "previous_post": self.previos_post}
    def to_json(self):
        """Преобразует объект в JSON."""
        self.data = {"f": self.f,
                "i": self.i,
                "o": self.o,
                "region": self.region,
                "birth_date": self.date_birth,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "post": self.post,
                "social_networks": self.social_links,
                "telephone": self.telephone,
                "address": self.adress,
                "telephone_and_fax": self.telephone_fax,
                "education": self.education,
                "rewards": self.rewards,
                "academic_degrees": self.academic_degrees,
                "academic_rewards": self.academic_rewards,
                "previous_post": self.previos_post}
        #print(data)
        json_info = json.dumps(self.data, indent=4, ensure_ascii=False)
        self.json_deputat = json_info