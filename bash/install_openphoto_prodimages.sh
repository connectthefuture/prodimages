#!/bin/bash
#######################################
# OpenPhoto Install
# Run with sudo for best results
#######################################
SECONDS=0
if [[ "$(/usr/bin/whoami)" != "root" ]]; then
    echo "This script must be run as root or using sudo.Script aborted."
    exit 1
fi

echo ""
echo ""
echo "===================================================="
echo "Updating Ubuntu and apt-get"
echo "===================================================="
echo ""
echo ""

apt-get update --assume-yes --quiet
apt-get upgrade --assume-yes --quiet

echo ""
echo ""
echo "===================================================="
echo "Installing needed packages and modules"
echo "===================================================="
echo ""
echo ""

# Apache
apt-get install --assume-yes --quiet apache2 php5 libapache2-mod-php5 php5-curl curl php5-gd php5-mcrypt php5-mysql php-pear php-apc build-essential libpcre3-dev
## Mysql if not Maria install
# apt-get install mysql-server mysql-client
a2enmod rewrite

echo ""
echo ""
echo "===================================================="
echo "Installing optional but recommended packages and modules"
echo "===================================================="
echo ""
echo ""

apt-get install --assume-yes --quiet php5-dev php5-imagick exiftran
a2enmod deflate
a2enmod expires
a2enmod headers

echo ""
echo ""
echo "===================================================="
echo "Installing oauth from pecl"
echo "===================================================="
echo ""
echo ""

pecl install oauth
mkdir -p /etc/php5/apache2/conf.d/
echo "extension=oauth.so" >> /etc/php5/apache2/conf.d/oauth.ini

echo ""
echo ""
echo "===================================================="
echo "Downloading OpenPhoto and unpacking"
echo "===================================================="
echo ""
echo ""

wget https://github.com/photo/frontend/tarball/master -O openphoto.tar.gz
tar -zxvf openphoto.tar.gz > /dev/null 2>&1
mv photo-frontend-* /var/www/openphoto
sudo rm openphoto.tar.gz

echo ""
echo ""
echo "===================================================="
echo "Setting permissions for Dev server"
echo "===================================================="
echo ""
echo ""

mkdir /var/www/openphoto/src/userdata
chown www-data:www-data /var/www/openphoto/src/userdata

mkdir /var/www/openphoto/src/html/assets/cache
chown www-data:www-data /var/www/openphoto/src/html/assets/cache

mkdir /var/www/openphoto/src/html/photos
chown www-data:www-data /var/www/openphoto/src/html/photos


chmod 775 /var/www/openphoto/src/userdata
chmod 775 /var/www/openphoto/src/html/photos
chmod 775 /var/www/openphoto/src/html/assets/cache


echo ""
echo ""
echo "===================================================="
echo "Setting up Nginx for PHP"
echo "===================================================="
echo ""
echo ""
# Nginx
apt-get install nginx php5-fpm curl php5-curl php5-gd php5-mcrypt php-pear

### Nginx

sed  -e 's:#fastcgi_pass fastcgi_pass unix\:fastcgi_pass unix\:/var/run/php5-fpm.sock;:g' -e 's/fastcgi_pass 127.0.0.1:9000;/#fastcgi_pass 127.0.0.1:9000;/g' -e 's/yourdomain.com/openphoto.prodimages.ny.bluefly.com/g' -e 's:/var/www/yourdomain.com/src/html/:/var/www/openphoto.prodimages.ny.bluefly.com/src/html/:g' -e 's:/var/www/openphoto:/var/www/openphoto.prodimages.ny.bluefly.com:g' /var/www/openphoto.prodimages.ny.bluefly.com/src/configs/openphoto-nginx.conf > /etc/nginx/sites-enabled/openphoto

echo ""
echo ""
echo "===================================================="
echo "Setting up Apache"
echo "===================================================="
echo ""
echo ""

### Apache
cp /var/www/openphoto/src/configs/openphoto-vhost.conf /etc/apache2/sites-available/openphoto
sed -e 's/file_uploads.*/file_uploads = On/g' -e 's/\/path\/to\/openphoto\/html\/directory/\/var\/www\/openphoto\/src\/html/g' /var/www/openphoto/src/configs/openphoto-vhost.conf > /etc/apache2/sites-available/openphoto
# Add below to above or edit apache config after
## -e 's/AliasMatch \.ini\$   /404/#AliasMatch \.ini$   /404/g' -e 's/#RewriteRule \.ini\$ - [F,NC]/RewriteRule \.ini$ - [F,NC]/g'
a2dissite default
a2ensite openphoto

echo ""
echo ""
echo "===================================================="
echo "Adjusting PHP settings"
echo "===================================================="
echo ""
echo ""

sed -e 's/<VirtualHost *:80>/<VirtualHost *:8082>/g' -e 's/upload_max_filesize.*/upload_max_filesize = 225M/g' -e 's/post_max_size.*/post_max_size = 225M/g' /etc/php5/apache2/php.ini > /etc/php5/apache2/php.ini.tmp
mv /etc/php5/apache2/php.ini.tmp /etc/php5/apache2/php.ini

echo ""
echo ""
echo "===================================================="
echo "Launching Your OpenPhoto site"
echo "===================================================="
echo ""
echo ""

/etc/init.d/apache2 restart

# finding IP address and compensating for possible EC2 installation
EC2=`curl --silent --connect-timeout 1 http://169.254.169.254/latest/meta-data/public-hostname`
if [[ $EC2 != "" ]];
then
	IP=`echo $EC2 | sed -rn 's/ec2-(.*?)\.compute.*/\1/p' | sed 's/-/./g'`
else
	IP=`ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'`
fi

echo ""
echo ""
echo ""
echo "****************************************************"
echo "===================================================="
echo "CONGRATULATIONS!!!"
echo ""
echo "The photographic heavens are applauding your"
echo "brand new installation of OpenPhoto."
echo ""
echo ""
echo "Took $SECONDS seconds to install."
echo ""
echo ""
echo "Now you can test your installation by directing your"
echo "browser to $IP"
echo "===================================================="
echo "****************************************************"
echo ""
echo ""
echo ""
echo ""
echo ""
echo ""


