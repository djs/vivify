import argparse
from bs4 import BeautifulSoup
import glob
import os.path
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import urllib2
import win32com.client
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
    filtered_rubys = [x for x in rubys if '-2.' not in x.a['href']]
    installer_url = filtered_rubys[0].a['href']
    installer = installer_url.split('?')[0]

    f = urllib2.urlopen(installer_url)
    with open(os.path.basename(installer), "wb") as local_installer:
        local_installer.write(f.read())

    f.close()

    if kit == 'exe':
        subprocess.check_call([os.path.basename(installer), '/silent',
            '/tasks="assocfiles,modpath"'])
    elif kit == 'sfx':
        if not os.path.exists('c:/devkit'):
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

def gvim():
    installer = 'https://bitbucket.org/djs/vim-win64/downloads/gvim73-772-win-amd64.exe'
    f = urllib2.urlopen(installer)
    with open(os.path.basename(installer), "wb") as local_installer:
        local_installer.write(f.read())
    f.close()

    subprocess.check_call([os.path.basename(installer), '/S'])

def rapidee():
    installer = 'http://www.rapidee.com/download/RapidEE_setup.exe'
    f = urllib2.urlopen(installer)
    with open(os.path.basename(installer), "wb") as local_installer:
        local_installer.write(f.read())
    f.close()

    subprocess.check_call([os.path.basename(installer), '/S'])

def ctags():
    f = urllib2.urlopen('http://downloads.sourceforge.net/project/ctags/ctags/5.8/ctags58.zip')
    with open('ctags58.zip', 'wb') as local_zip:
        local_zip.write(f.read())

    f.close()

    with zipfile.ZipFile('ctags58.zip', 'r') as myzip:
        myzip.extract('ctags58/ctags.exe', os.path.expandvars('$MY_USER_BIN'))

def fonts():

    def install_font(font):
        obj = win32com.client.Dispatch('Shell.Application')
        folder = obj.Namespace(os.path.dirname(os.path.abspath(font)))
        item = folder.ParseName(font)
        item.InvokeVerb('Install')

    tarball = 'https://fedorahosted.org/releases/l/i/liberation-fonts/liberation-fonts-ttf-2.00.1.tar.gz'
    f = urllib2.urlopen(tarball)
    with open(os.path.basename(tarball), "wb") as local_tarball:
        local_tarball.write(f.read())
    f.close()

    oldpath = os.getcwd()
    tar = tarfile.open(os.path.basename(tarball))
    os.mkdir('liberation')
    os.chdir('liberation')
    tar.extractall()
    tar.close()
    os.chdir(os.walk('.').next()[1][0])
    for font in glob.glob('*.ttf'):
        install_font(font)


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
        gvim()
        rapidee()
        fonts()
        ctags()
    else:
        method = globals()[args.item]
        method()

if __name__ == '__main__':
    main()
