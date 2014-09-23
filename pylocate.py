from __future__ import print_function
__author__ = 'Roberto Estrada (a.k.a) paridin'
import urllib2
import sys, os
from subprocess import PIPE, Popen


class Pylocate:
    """
     if you don't specify the port by default is 80
     this function get the public ip for you server

     @port: receive the specific port to listen you home server
    """
    def __init__(self, port='80'):
        self.url = 'http://sicam.mx/reportes/php/ip.php'
        self.SOURCE_DIR = os.getcwd() + '/source'
        self.logFile = os.getcwd() + '/log'
        self.port = port
        self.log = True  #False for don't write logs
        try:
            self.ip = urllib2.urlopen(self.url).read()
        except:
            print(sys.exc_info()[1])


    """
        This function get the lasted ip save in a file
    """
    def get_last_ip(self):
        try:
            f = open('source/lastip.txt')
            self.last_ip = f.read()
            f.close()
        except:
            print(sys.exc_info()[1])
        return self.last_ip


    """
        this function is for replace the new ip if the script detect is different
        if is the first time to run this function write the public ip to redirect you own server

        @file
    """
    def replaceAll(self, file, search, replace):
        import fileinput
        for line in fileinput.input(file, inplace=1):
            if search in line:
                line = line.replace(search,replace)
            sys.stdout.write(line)


    """
        This function if for run the script
    """
    def run(self):
        if self.get_last_ip() == '':
            try:
                self.write_file_ip()
            except:
                print(sys.exc_info()[1])
        else:
            try:
                self.write_html()
            except:
                print(sys.exc_info()[1])

    """
        Upload file to server
    """
    def uploadToServer(self, ftp, user, password, filename='index.html',):
        cmd =  "curl -T '%s/%s' %s --user %s:%s" % (self.SOURCE_DIR, filename, ftp, user, password)
        try:
            print("Intentando subir el archivo: %s al ftp." % filename)
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        except OSError as err:
            print(err)
        if self.log:
            f = open(self.logFile + '/upload-file.log', 'w+')
            f.write(p.communicate()[1])
            f.close()
        if p.returncode == 0:
            print("Se subio el archivo: %s al ftp." % filename)
        else:
            print("No fue posible subir el archivo: %s al ftp." % filename)

    """
        This function works writing the public ip in a file
    """
    def write_file_ip(self):
        try:
            f = open('%s/lastip.txt' % self.SOURCE_DIR, 'w')
            f.write("%s:%s" % (self.ip, self.port))
            f.close()
        except:
            print(sys.exc_info()[1])


    """
        This function detect the lasted ip and the new ip, if its the firt time to run this script it works like setup
        to construct all the index file
    """
    def write_html(self):
        lip = self.last_ip
        nip = "%s:%s" % (self.ip, self.port)
        path = "%s/index.html" % self.SOURCE_DIR
        if lip != nip:
            try:
                self.replaceAll(path, "%s" % lip, nip)
                self.write_file_ip()
            except:
                print(sys.exc_info()[1])
        else:
            try:
                self.replaceAll(path, "CHANGE_IP", nip)
            except:
                print(sys.exc_info()[1])


if __name__ == '__main__':
    #Edit this values with your personal values
    ftp='ftp://your_ftp/dir_where_you_want_upload/'
    ftp_user='Your_ftp_user'
    ftp_password='Your_ftp_pass'

    p = Pylocate(port='8000') #specify the port to listen you home server
    p.run()
    p.uploadToServer(ftp, ftp_user, ftp_password)