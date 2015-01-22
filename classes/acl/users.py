__author__ = 'cagdas'
import sys

class Users():

    chap_secret_file = '.'
    user_list = []
    count = 0

    def __init__(self, chap_secret_file):
        self.chap_secret_file = chap_secret_file

    def fetch_users(self):
        self.user_list = []
        index = 0
        with open(self.chap_secret_file, "r") as ins:
            for line in ins:
                index+=1

                line = line.strip()

                if line != '' and line[0] != '#':
                    self.count+=1
                    account = Account(index,line)
                    self.user_list.append(account)

            print "Total %s account" % (self.count)

        return self.user_list

    def add_user(self, username, password, server, ip):
        new_user = "%s\t%s\t%s\t%s\r\n" % (username,server,password,ip)
        with open(self.chap_secret_file, "a") as file:
                file.write(new_user)

    def remove_user(self, _id): 
        write_lines = "";
        index = 0
        f = open(self.chap_secret_file, "r")
        lines = f.readlines()
        for line in lines:
            index += 1

            if index != int(_id):
                write_lines += line

        f.close()

        f = open(self.chap_secret_file, "w")
        f.write(write_lines)
        f.close()

class Account():
    index=username = password = server = ip = ""
    def __init__(self, _id, line):
        item = line.split()
        self.username = item[0]
        self.server = item[1]
        self.password = item[2]
        self.ip = item[3]
        self.index = _id