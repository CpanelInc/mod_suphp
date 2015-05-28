#
# ----------------- Keep this copyright notice --------------------
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
# See also http://en.opensuse.org/openSUSE:Specfile_guidelines
#
# ----------------- Keep this copyright notice --------------------

# NOTE: This modules requires httpd-devel, because it also provides
# the RPM macros necessary to expand %{_httpd_*} through out this
# spec file.

# Defining the package namespace
%global ns_name ea
%global upstream_name mod_suphp

%define debug_package %{nil}

Name:           %{ns_name}-%{upstream_name}
Version:        0.7.2
Release:        4%{dist}
License:        GPL-2.0
Vendor:         cPanel, Inc.
Summary:        Execute PHP scripts with the permissions of their owner.
Url:            http://www.suphp.org
Group:          System Environment/Daemons
Source:         http://suphp.org/download/suphp-%{version}.tar.gz
Source1:        httpd-suphp.conf
Source2:        httpd-suphp.modules.conf
Source4:        etc-suphp.conf
Patch0:         0001-mod_userdir-support-and-userdir_overrides_usergroup-.patch
Patch1:         0002-Allow-scripts-to-show-itself-in-process-list.patch
Patch2:         0003-Option-to-turn-off-paranoid-mode-via-configuration-f.patch
Patch3:         0004-Force-rebuild-of-configure-script.patch
Patch4:         0005-Add-support-for-Apache-2.4-in-configure-script.patch
Patch5:         0006-Fix-void-return-within-int-context.patch
Patch6:         0007-Fix-autoreconf-usage-when-generating-configure-scrip.patch
Patch7:         suphp-0.7.1-cagefs.patch
BuildRequires:  ea-apache24-devel
BuildRequires:  ea-apr-devel >= 1.5.0
BuildRequires:  gcc-c++
BuildRequires:  libtool
Requires:       ea-apache24-mmn = %{_httpd_mmn}
Requires:       ea-apr >= 1.5.0
Conflicts:      ea-mod_ruid2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

%description
suPHP is a tool for executing PHP scripts with the permissions of their owners.
It consists of an Apache module (mod_suphp) and a setuid root binary (suphp)
that is called by the Apache module to change the uid of the process executing
the PHP interpreter.

%prep
%setup -q -n suphp-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build

mkdir -p m4
autoreconf -fi

%configure \
    --with-apache-user=nobody \
    --with-setid-mode=paranoid \
    --with-apr=%{_usr}/bin/apr-1-config \
    --with-apxs=%{_httpd_apxs} \
    --with-logfile=%{_localstatedir}/log/apache2/suphp_log \
    --enable-lve

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -D %{SOURCE4}             %{buildroot}%{_sysconfdir}/suphp.conf
install -D %{SOURCE1}             %{buildroot}%{_httpd_confdir}/00-suphp.conf
install -D %{SOURCE2}             %{buildroot}%{_httpd_modconfdir}/90-suphp.conf
install -D /dev/null              %{buildroot}%{_localstatedir}/log/apache2/suphp_log

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%attr(0755,root,nobody) %{_httpd_moddir}/mod_suphp.so
%attr(4750,root,nobody) %{_sbindir}/suphp
%config(noreplace) %{_sysconfdir}/suphp.conf
%config(noreplace) %{_httpd_confdir}/00-suphp.conf
%config(noreplace) %{_httpd_modconfdir}/90-suphp.conf
%ghost %{_localstatedir}/log/apache2/suphp_log
%doc %attr(0644,root,root) AUTHORS  ChangeLog  COPYING  NEWS
%doc %attr(0644,root,root) doc/*

%changelog
* Thu May 28 2015 Darren Mobley <darren@cpanel.net> - 0.7.2-4
- Changed ea-apache2 to ea-apache24

* Wed May 27 2015 Matt Dees <matt.dees@cpanel.net> - 0.7.2-3
- Fix file permissions

* Thu Apr 30 2015 Dan Muey <dan@cpanel.net> - 0.7.2-2
- Corrected suphp.conf's logfile value

* Fri Mar 27 2015 S. Kurt Newman <kurt.newman@cpanel.net> - 0.7.2-1
- Added proper release number
- Removed logrotate in favor of WHM's implemenation

* Mon Feb 02 2015 trinity.quirk@cpanel.net
- Running as 'nobody' user

* Wed Jan 14 2015 kurt.newman@cpanel.net
- Updated for cPanel support on CentOS 6

* Sun Aug  4 2013 novell@tower-net.de
- New suphp 0.7.2 (http://www.suphp.org/)
