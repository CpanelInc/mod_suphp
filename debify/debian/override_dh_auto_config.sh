#!/bin/bash

source debian/vars.sh

set -x

# pulled from apr-util
mkdir -p config
cp $ea_apr_config config/apr-1-config
cp $ea_apr_config config/apr-config
cp /usr/share/pkgconfig/ea-apr16-1.pc config/apr-1.pc
cp /usr/share/pkgconfig/ea-apr16-util-1.pc config/apr-util-1.pc
cp /usr/share/pkgconfig/ea-apr16-1.pc config
cp /usr/share/pkgconfig/ea-apr16-util-1.pc config

export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:`pwd`/config"
touch configure

export CXXFLAGS="$CXXFLAGS -std=c++14"

mkdir -p m4
autoreconf -fi

./configure \
    --sbindir=/usr/sbin \
    --sysconfdir=/etc \
    --with-apache-user=nobody \
    --with-setid-mode=paranoid \
    --with-apr=$ea_apr_dir \
    --with-apxs=$_httpd_apxs \
    --with-logfile=$_localstatedir/log/apache2/suphp_log \
    --enable-lve
make 
