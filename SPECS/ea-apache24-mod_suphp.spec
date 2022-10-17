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
%global ns_name ea-apache24
%global upstream_name mod_suphp

%define debug_package %{nil}

Name:           %{ns_name}-%{upstream_name}
Version:        0.7.2
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4562 for more details
%define release_prefix 32
Release: %{release_prefix}%{?dist}.cpanel
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
Patch7:         0008-Support-phprc_paths-section-in-suphp.conf.patch
Patch8:         suphp-0.7.1-cagefs.patch
Patch9:         0009-Update-allow_file_group_writeable-with-more.patch
BuildRequires:  %{ns_name}-devel
BuildRequires:  ea-apr-devel >= 1.5.0
BuildRequires:  ea-apr-util-devel
BuildRequires:  gcc-c++
BuildRequires:  libtool
Requires:       %{ns_name}-mmn = %{_httpd_mmn}
Requires:       ea-apr >= 1.5.0
Conflicts:      %{ns_name}-mod_ruid2 %{ns_name}-mpm_itk
Provides:       %{ns_name}-exec_code_asuser %{ns_name}-exec_php_asuser
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
%patch8 -p1
%patch9 -p1

%build
set -x

mkdir -p m4
autoreconf -fi

%if 0%{?rhel} >= 9
export CXXFLAGS="$CXXFLAGS -std=c++14 -fPIE"
%endif

%configure \
    --with-apache-user=nobody \
    --with-setid-mode=paranoid \
    --with-apr=%{ea_apr_dir} \
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

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%attr(0755,root,nobody) %{_httpd_moddir}/mod_suphp.so
%attr(4750,root,nobody) %{_sbindir}/suphp
%config(noreplace) %{_sysconfdir}/suphp.conf
%config(noreplace) %{_httpd_confdir}/00-suphp.conf
%config(noreplace) %{_httpd_modconfdir}/90-suphp.conf
%doc %attr(0644,root,root) AUTHORS  ChangeLog  COPYING  NEWS
%doc %attr(0644,root,root) doc/*

%changelog
* Mon Oct 17 2022 Brian Mendoza <brian.mendoza@cpanel.net> - 0.7.2-32
- ZC-10381: Add ea-php82

* Thu Sep 29 2022 Julian Brown <julian.brown@cpanel.net> - 0.7.2-31
- ZC-10009: Add changes so that it builds on AlmaLinux 9

* Wed Dec 29 2021 Dan Muey <dan@cpanel.net> - 0.7.2-30
- ZC-9616: disable OBS debuginfo flag for C6 and C7

* Thu Dec 16 2021 Julian Brown <julian.brown@cpanel.net> - 0.7.2-29
- ZC-9596: Changes to build on Ubuntu 21

* Wed Nov 10 2021 Julian Brown <julian.brown@cpanel.net> - 0.7.2-28
- ZC-9491: Add ea-php81

* Wed Oct 28 2020 Daniel Muey <dan@cpanel.net> - 0.7.2-27
- ZC-7308: Updates for PHP 8 (fix for 7.3 and 7.4)

* Wed Aug 15 2018 Cory McIntire <cory@cpanel.net> - 0.7.2-26
- EA-7779: Revert change from EA-7525 as it causes Cloud Linux ini not to load

* Tue Jul 31 2018 Tim Mullin <tim@cpanel.net> - 0.7.2-25
- EA-7525: Fixed 0008-Support-phprc_paths-section-in-suphp.conf.patch, targetMode used before initialized

* Fri Jul 06 2018 Tim Mullin <tim@cpanel.net> - 0.7.2-24
- EA-7555: Don't remove suphp_log upon uninstall

* Wed Dec 13 2017 Dan Muey <dan@cpanel.net> - 0.7.2-23
- ZC-3144: undo 0.7.2-22 change since it breaks expected inheritance (part of ZC-3130)

* Thu Nov 02 2017 Brett Estrade <brett@cpanel.net> - 0.7.2-22
- SWAT-730: remove phpPrefix/etc from INI scan path

* Thu Sep 21 2017 Dan Muey <dan@cpanel.net> - 0.7.2-21
- EA-6839: only do ini path logic when PHPRC is not in effect

* Wed Sep 20 2017 Dan Muey <dan@cpanel.net> - 0.7.2-20
- EA-6833: Add explicit etc/ and etc/php.d/ paths before CWD so we get ini merging behavior

* Mon Sep 18 2017 Jacob Perkins <jacob.perkins@cpanel.net> - 0.7.2-19
- EA-6814: Added support for PHP72

* Wed Sep 13 2017 Dan Muey <dan@cpanel.net> - 0.7.2-18
- EA-6797: Load the CWD ini last so values set by user take precedent over global values

* Wed Dec 14 2016 S. Kurt Newman <kurt.newman@cpanel.net> - 0.7.2-17
- Added new allow_file_group_writeable patch (EA-4868)

* Mon Nov 07 2016 Dan Muey <dan@cpanel.net> - 0.7.2-16
- EA-5202: Add ea3 patch to support phprc_paths section in suphp.conf

* Fri Jul 29 2016 Jacob Perkins <jacob.perkins@cpanel.net> - 0.7.2-15
- Add support for PHP71

* Mon Jun 20 2016 Dan Muey <dan@cpanel.net> - 0.7.2-14
- EA-4383: Update Release value to OBS-proof versioning

* Thu Dec 17 2015 Matt Dees <matt@cpanel.net> 0.7.2-7
- Add support for PHP7

* Fri Jul 31 2015 Trinity Quirk <trinity.quirk@cpanel.net> - 0.7.2-6
- Using new apr macros

* Thu May 28 2015 Darren Mobley <darren@cpanel.net> - 0.7.2-5
- Changed ea-mod to ea-apache24-mod

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
