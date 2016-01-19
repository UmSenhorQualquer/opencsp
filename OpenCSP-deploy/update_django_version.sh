sudo apt-get install python-pip
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
sudo pip install django==1.7.10
sudo pip install django-suit==0.2.12
sudo pip install django-jfu==2.0.9
sudo pip install django-suit-redactor
sudo pip install ping
sudo apt-get install mysql-server
sudo apt-get install qt4-dev-tools qt4-qmake
sudo apt-get install sshpass

#sudo nano /etc/mysql/my.cnf
#change the IP of the mysql config file to the machine file

#update user set host='%' where user='root';
#use mysql;
#select host, user from user;
#flush privileges;

sudo apt-get install python-dev
sudo apt-get install python-numpy
sudo apt-get install python-opencv
wget https://github.com/UmSenhorQualquer/pyforms/archive/master.zip
unzip master.zip
cd pyforms-master/
sudo python setup.py install
sudo apt-get install cmake

sudo apt-get remove ffmpeg x264 libx264-dev libav-tools libvpx-dev
wget ftp://ftp.videolan.org/pub/x264/snapshots/last_stable_x264.tar.bz2
tar jxvf last_stable_x264.tar.bz2
cd x264-snapshot-20131118-2245-stable
./configure --enable-pic --enable-shared --disable-asm
sudo make install

sudo apt-get install yasm
wget http://www.ffmpeg.org/releases/ffmpeg-2.8.1.tar.bz2
tar jxvf ffmpeg-2.8.1.tar.bz2
cd ffmpeg-2.8.1
./configure --enable-pic --enable-shared --enable-gpl --enable-libx264
sudo make install

wget https://github.com/Itseez/opencv/archive/3.0.0.zip
unzip 3.0.0.zip
cd opencv-3.0.0
mkdir build
cd build
cmake  BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON -D WITH_QT=ON -D WITH_OPENGL=ON ..
sudo make install
sudo pip install sorl-thumbnail==12.3
sudo pip install django-allauth

sudo apt-get install python-mysqldb
sudo pip install paramiko==1.15
sudo pip install fabric
sudo pip install smartencoding
sudo pip install simplejson
sudo pip install django-sekizai
sudo pip install django-mobile
sudo pip install django-allauth==0.20.0





<VirtualHost *:80>
    ServerName  opencsp.champalimaud.pt
    ServerAlias opencsp.champalimaud.pt 10.40.11.123
    ServerAdmin ricardo.ribeiro@neuro.fchampalimaud.org

    ErrorLog  /var/log/opencsp_error.log
    CustomLog /var/log/opencsp_access.log combined

    #WSGIDaemonProcess opencsp python-path=/var/www/opencsp
    WSGIScriptAlias / /var/www/opencsp/server/wsgi.py

    <Directory /var/www/opencsp>
        Options Indexes FollowSymLinks
        AllowOverride None
        Order allow,deny
        Allow from all
    </Directory>

    <Directory /var/www/opencsp/server>
        Options Indexes FollowSymLinks
        AllowOverride None
        Order allow,deny
        Allow from all
    </Directory>

</VirtualHost>


#Crontab
* * * * * cd /var/www/opencsp/ && python scripts/check_pending_tasks.py
*/5 * * * * cd /var/www/opencsp/ && python scripts/check_lip_jobs.py