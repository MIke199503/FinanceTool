

class GetDepart:
    def __init__(self, data_list):
        self.data = data_list
        self.leval_list = {}

    def get_one_leval(self):
        for item in self.data:
            if len(item[0]) == 4:
                self.leval_list[item[0]] = {}
        print(self.leval_list)


