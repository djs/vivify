import argparse
from bs4 import BeautifulSoup
import os.path
import platform
import re
import shutil
import subprocess
import sys
import urllib2
import zipfile


def platform_check():
    if platform.machine() != 'AMD64':
        print >> sys.stderr, "%s architecture not supported"
        sys.exit(1)

    if int(platform.release()) < 7:
        print >> sys.stderr, "Only modern Windows are supported"
        sys.exit(1)

def ruby(kit):
    f = urllib2.urlopen('http://rubyinstaller.org/downloads/')
    soup = BeautifulSoup(f)
    f.close()

    rubys = sorted(soup.find_all('li', kit), reverse=True, key=lambda k: k.get_text())
    installer = rubys[0].a['href']

    f = urllib2.urlopen(installer)
    with open(os.path.basename(installer), "wb") as local_installer:
        local_installer.write(f.read())

    f.close()

    if kit == 'exe':
        subprocess.check_call([os.path.basename(installer), '/silent',
            '/tasks="assocfiles,modpath"'])
    elif kit == 'sfx':
        os.mkdir('c:/devkit')
        oldpath = os.getcwd()
        os.chdir('c:/devkit')
        subprocess.check_call(['7za', 'x', os.path.join(oldpath,
            os.path.basename(installer))])
        subprocess.check_call(['c:/ruby193/bin/ruby', 'dk.rb', 'init'])
        subprocess.check_call(['c:/ruby193/bin/ruby', 'dk.rb', 'install'])
        os.chdir(oldpath)

def sevenzip():
    f = urllib2.urlopen('http://downloads.sourceforge.net/project/sevenzip/7-Zip/9.20/7za920.zip')
    with open('7za920.zip', 'wb') as local_zip:
        local_zip.write(f.read())

    f.close()

    with zipfile.ZipFile('7za920.zip', 'r') as myzip:
        myzip.extract('7za.exe', os.path.expandvars('$MY_USER_BIN'))

def conemu():
    f = urllib2.urlopen('http://code.google.com/p/conemu-maximus5/downloads/list')
    soup = BeautifulSoup(f)
    f.close()


    ext = soup.find('table', id='resultstable').td.a['href']
    url = 'http://code.google.com' + ext


    f = urllib2.urlopen('http://code.google.com/p/conemu-maximus5/downloads/list')
    soup = BeautifulSoup(f)
    f.close()

    ext = soup.find('a', href=re.compile('.exe$'))['href']
    installer = 'http:' + ext

    f = urllib2.urlopen(installer)
    with open(os.path.basename(installer), "wb") as local_installer:
        local_installer.write(f.read())

    f.close()

    subprocess.check_call([os.path.basename(installer), '/p:x64',
        '/passive'])


def clink():
    installer = 'http://download.microsoft.com/download/A/8/0/A80747C3-41BD-45DF-B505-E9710D2744E0/vcredist_x64.exe'
    f = urllib2.urlopen(installer)
    with open(os.path.basename(installer), "wb") as local_installer:
        local_installer.write(f.read())
    f.close()

    subprocess.check_call([os.path.basename(installer), '/passive'])
    f = urllib2.urlopen('https://code.google.com/p/clink/downloads/list')
    soup = BeautifulSoup(f)
    f.close()


    ext = soup.find('table', id='resultstable').td.a['href']
    url = 'http://code.google.com' + ext


    f = urllib2.urlopen('https://code.google.com/p/clink/downloads/list')
    soup = BeautifulSoup(f)
    f.close()

    ext = soup.find('a', href=re.compile('.exe$'))['href']
    installer = 'http:' + ext

    f = urllib2.urlopen(installer)
    with open(os.path.basename(installer), "wb") as local_installer:
        local_installer.write(f.read())

    f.close()

    subprocess.check_call([os.path.basename(installer), '/S'])

    directory = os.path.join('C:\\Program Files (x86)\\clink', os.walk('C:\\Program Files (x86)\\clink').next()[1][0])
    files = os.listdir(os.path.join(directory, directory))
    for filename in files:
        fullname = os.path.join(directory, filename)
        if(os.path.isfile(fullname)):
            print fullname
            shutil.copy(fullname, 'C:\\Program Files\\ConEmu\\ConEmu\\clink')



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("item")
    args = parser.parse_args()

    platform_check()

    if args.item == 'all':
        sevenzip()
        ruby('exe')
        ruby('sfx')
        conemu()
        clink()
    else:
        method = globals()[args.item]
        method()

if __name__ == '__main__':
    main()
