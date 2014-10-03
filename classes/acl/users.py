__author__ = 'cagdas'

class Users():

    chap_secret_file = '.'
    user_list = []

    def __init__(self, chap_secret_file):
        self.chap_secret_file = chap_secret_file

    def fetch_users(self):
        self.user_list = []
        try:
            f = open(self.chap_secret_file, "r")
            line = f.readline()
            while line:
                if line[0] != '#':
                    self.user_list.append(line)
                line = f.readline()
        except:
            print('Exception occurred while fetching user information');
            pass

        return self.user_list
