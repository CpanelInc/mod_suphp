#!/bin/bash

source debian/vars.sh

echo "BUILDROOT :$buildroot:"

make install DESTDIR=$buildroot
install -D $SOURCE4             $buildroot$_sysconfdir/suphp.conf
install -D $SOURCE1             $buildroot$_httpd_confdir/00-suphp.conf
install -D $SOURCE2             $buildroot$_httpd_modconfdir/90-suphp.conf

mkdir -p debian/tmp/etc/apache2/conf.d
mkdir -p debian/tmp/etc/apache2/conf.modules.d
mkdir -p debian/tmp/usr/lib64/apache2/modules
mkdir -p debian/tmp/usr/sbin
mkdir -p debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2
mkdir -p debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2/apache

cp etc/apache2/conf.d/00-suphp.conf debian/tmp/etc/apache2/conf.d/00-suphp.conf
cp etc/apache2/conf.modules.d/90-suphp.conf debian/tmp/etc/apache2/conf.modules.d/90-suphp.conf
cp opt/cpanel/root/etc/suphp.conf debian/tmp/etc/suphp.conf
cp usr/lib64/apache2/modules/mod_suphp.so debian/tmp/usr/lib64/apache2/modules/mod_suphp.so
cp usr/sbin/suphp debian/tmp/usr/sbin/suphp
cp AUTHORS debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2
cp doc/CONFIG debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2
cp COPYING debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2
cp ChangeLog debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2
cp INSTALL debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2
cp doc/LICENSE debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2
cp NEWS debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2
cp README debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2
cp doc/suphp.conf-example debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2

cp doc/apache/CONFIG debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2/apache
cp doc/apache/INSTALL debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2/apache
cp doc/apache/README debian/tmp/usr/share/doc/ea-apache24-mod_suphp-0.7.2/apache

