__author__ = 'cagdas'
import sys

class Users():

    chap_secret_file = '.'
    user_list = []

    def __init__(self, chap_secret_file):
        self.chap_secret_file = chap_secret_file

    def fetch_users(self):
        self.user_list = []
        try:
            with open(self.chap_secret_file, "r") as ins:
                for line in ins:
                    print "line=>>", line
                    if line[0] != '#':
                        self.user_list.append(line)
        except:
            print "Exception occurred while fetching user information"
            print "Unexpected error:", sys.exc_info()[0]
            pass

        return self.user_list
