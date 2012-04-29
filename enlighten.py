from bs4 import BeautifulSoup
import os.path
import subprocess
import urllib2
import zipfile

def main():
    sevenzip()
    ruby('exe')
    ruby('sfx')



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



if __name__ == '__main__':
    main()
