Name:           conntrack-tools
Version:        1.4.7
Release:        2%{?dist}
Summary:        Manipulate netfilter connection tracking table and run High Availability
License:        GPLv2
URL:            http://conntrack-tools.netfilter.org/
Source0:        http://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
Source1:        conntrackd.service
Source2:        conntrackd.conf

Patch01:        0001-build-conntrack-tools-requires-libnetfilter_conntrac.patch
Patch02:        0002-build-don-t-suppress-various-warnings.patch
Patch03:        0003-network-Fix-Wstrict-prototypes.patch
Patch04:        0004-config-Fix-Wimplicit-function-declaration.patch

BuildRequires:  gcc
BuildRequires:  libnfnetlink-devel >= 1.0.1, libnetfilter_conntrack-devel >= 1.0.9
BuildRequires:  libnetfilter_cttimeout-devel >= 1.0.0, libnetfilter_cthelper-devel >= 1.0.0
BuildRequires:  libmnl-devel >= 1.0.3, libnetfilter_queue-devel >= 1.0.2
BuildRequires:  libtirpc-devel systemd-devel
BuildRequires:  pkgconfig bison flex
Provides:       conntrack = 1.0-1
Obsoletes:      conntrack < 1.0-1
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
BuildRequires: make
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
Requires: libnetfilter_conntrack >= 1.0.9

%description
With conntrack-tools you can setup a High Availability cluster and
synchronize conntrack state between multiple firewalls.

The conntrack-tools package contains two programs:
- conntrack: the command line interface to interact with the connection
             tracking system.
- conntrackd: the connection tracking userspace daemon that can be used to
              deploy highly available GNU/Linux firewalls and collect
              statistics of the firewall use.

conntrack is used to search, list, inspect and maintain the netfilter
connection tracking subsystem of the Linux kernel.
Using conntrack, you can dump a list of all (or a filtered selection  of)
currently tracked connections, delete connections from the state table, 
and even add new ones.
In addition, you can also monitor connection tracking events, e.g. 
show an event message (one line) per newly established connection.

%prep
%autosetup -p1

%build
autoreconf -fi
rm -Rf autom4te*.cache config.h.in~
%configure --disable-static --enable-systemd
%make_build
chmod 644 doc/sync/primary-backup.sh
rm -f doc/sync/notrack/conntrackd.conf.orig doc/sync/alarm/conntrackd.conf.orig doc/helper/conntrackd.conf.orig

%install
%make_install
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
mkdir -p %{buildroot}%{_sysconfdir}/conntrackd
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/conntrackd/

%files
%license COPYING
%doc AUTHORS TODO doc
%dir %{_sysconfdir}/conntrackd
%config(noreplace) %{_sysconfdir}/conntrackd/conntrackd.conf
%{_unitdir}/conntrackd.service
%{_sbindir}/conntrack
%{_sbindir}/conntrackd
%{_sbindir}/nfct
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %{_libdir}/conntrack-tools
%{_libdir}/conntrack-tools/*

%post
%systemd_post conntrackd.service

%preun
%systemd_preun conntrackd.service

%postun
%systemd_postun conntrackd.service 

%changelog
* Wed Dec 14 2022 Phil Sutter <psutter@redhat.com> - 1.4.7-2
- Explicitly depend on libnetfilter_conntrack-1.0.9

* Thu Dec 01 2022 Phil Sutter <psutter@redhat.com> - 1.4.7-1
- config: Fix -Wimplicit-function-declaration
- network: Fix -Wstrict-prototypes
- build: don't suppress various warnings
- build: conntrack-tools requires libnetfilter_conntrack >= 1.0.9
- New version 1.4.7

* Tue Nov 29 2022 Phil Sutter <psutter@redhat.com> - 1.4.5-17
- conntrackd: set default hashtable buckets and max entries if not specified

* Tue Sep 06 2022 Phil Sutter <psutter@redhat.com> - 1.4.5-16
- local: Avoid sockaddr_un::sun_path buffer overflow

* Mon Aug 15 2022 Phil Sutter <psutter@redhat.com> - 1.4.5-15
- conntrack: fix compiler warnings
- src: fix strncpy -Wstringop-truncation warnings
- connntrack: Fix for memleak when parsing -j arg
- Drop pointless assignments
- Don't call exit() from signal handler
- read_config_yy: Drop extra argument from dlog() call
- helpers: ftp: Avoid ugly casts
- Fix potential buffer overrun in snprintf() calls
- cache: Fix features array allocation
- hash: Flush tables when destroying

* Mon Mar 28 2022 Phil Sutter <psutter@redhat.com> - 1.4.5-14
- conntrackd: use correct max unix path length

* Thu Mar 24 2022 Phil Sutter <psutter@redhat.com> - 1.4.5-13
- conntrackd: Use strdup in lexer
- conntrackd: use strncpy() to unix path

* Tue Mar 15 2022 Phil Sutter <psutter@redhat.com> - 1.4.5-12
- Fix source compile in tests.yml

* Tue Mar 15 2022 Phil Sutter <psutter@redhat.com> - 1.4.5-11
- Enable hardened builds again.

* Tue Jan 25 2022 Phil Sutter <psutter@redhat.com> - 1.4.5-10
- Drop lazy binding via patch from upstream
- Add patches to fix for failing RPC header search

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.4.5-9
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 1.4.5-8
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 14 2018 Paul Wouters <pwouters@redhat.com> - 1.4.5-2
- Disable hardened build to really fix rhbz#1413408

* Mon Dec 10 2018 Paul Wouters <pwouters@redhat.com> - 1.4.5-1
- Resolves: rhbz#1574091 conntrack-tools-1.4.5 is available
- Resolves: rhbz#1413408 ct_helper_ftp not working
  (I've reduced the hardening to use -z,lazy)
- Eanbled systemd support
- Bumped required libnetfilter_conntrack-devel to 1.0.7
- fixup harmless but broken mkdir in spec file
- Don't override CPPFLAGS and LIBS, instead fixup src/helpers/Makefile

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 12 2018 Orion Poplawski <orion@nwra.com> - 1.4.4-7
- Use libtirpc
- Use %%license

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 22 2017 Paul Wouters <pwouters@redhat.com> - 1.4.4-3
- Add upstream patches (free pktb after use, nat_tuple leak)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 22 2016 Paul Wouters <pwouters@redhat.com> - 1.4.4-1
- Updated to 1.4.4 (rhbz#1370668)
- Include new man5 pages

* Wed Apr 20 2016 Paul Wouters <pwouters@redhat.com> - 1.4.3-1
- Resolves: rhbz#1261220 1.4.3 is available
- Update source url
- Remove incorporated patches

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 21 2015 Paul Wouters <pwouters@redhat.com> - 1.4.2-10
- Resolves: 1255578 - conntrackd could neither be started nor be stopped

* Tue Aug 18 2015 Paul Wouters <pwouters@redhat.com> - 1.4.2-9
- Resolves: rhbz#CVE-2015-6496, rhbz#1253757
- Fold in upstream patches since 1.4.2 release up to git 900d7e8
- Fold in upstream patch set of 2015-08-18 for coverity issues

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 12 2015 Paul Komkoff <i@stingr.net> - 1.4.2-7
- bz#1181119 - wait for network to be on before starting conntrackd

* Sun Jan 11 2015 Paul Komkoff <i@stingr.net> - 1.4.2-6
- bz#998105 - remove patch residues from doc

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Paul Komkoff <i@stingr.net> - 1.4.2-3
- rebuilt

* Sat Sep  7 2013 Paul P. Komkoff Jr <i@stingr.net> - 1.4.2-2
- bz#850067

* Sat Sep  7 2013 Paul P. Komkoff Jr <i@stingr.net> - 1.4.2-1
- new upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 08 2013 Paul Komkoff <i@stingr.net> - 1.4.0-2
- fix bz#909128

* Mon Nov 26 2012 Paul P. Komkoff Jr <i@stingr.net> - 1.4.0-1
- new upstream version

* Tue Jul 24 2012 Paul P. Komkoff Jr <i@stingr.net> - 1.2.1
- new upstream version

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 07 2012 Paul Wouters <pwouters@redhat.com> - 1.0.1-1
- Updated to 1.0.1
- Added daemon using systemd and configuration file
- Removed legacy spec requirements
- Patch for: parse.c:240:34: error: 'NULL' undeclared 

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu May  5 2011 Paul P. Komkoff Jr <i@stingr.net> - 1.0.0
- new upstream version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Paul P. Komkoff Jr <i@stingr.net> - 0.9.15-1
- new upstream version

* Thu Mar 25 2010 Paul P. Komkoff Jr <i@stingr.net> - 0.9.14-1
- update, at last

* Tue Nov 10 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.9.13-2
- failed to properly commit the package :(

* Tue Oct 13 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.9.13-1
- new upstream version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 24 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.9.12-3
- new upstream version

* Sun May 24 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.9.12-2
- versioning screwup

* Sun May 24 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.9.12-1
- new upstream version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 13 2009 Paul P. Komkoff Jr <i@stingr.net> - 0.9.9-1
- new upstream version

* Sun Oct 26 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.9.8-1
- new upstream version
- remove rollup patch

* Wed Jul 16 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.9.7-2
- fix Patch0/%%patch.

* Wed Jul 16 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.9.7-1
- new upstream version

* Sat Feb 23 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.9.6-0.1.svn7382
- new version from svn

* Fri Feb 22 2008 Paul P. Komkoff Jr <i@stingr.net> - 0.9.5-5
- fix the PATH_MAX-related compilation problem

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.5-4
- Autorebuild for GCC 4.3

* Tue Oct 23 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.9.5-3
- review fixes

* Sun Oct 21 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.9.5-2
- review fixes

* Fri Oct 19 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.9.5-1
- new upstream version

* Sun Jul 22 2007 Paul P. Komkoff Jr <i@stingr.net> - 0.9.4-1
- replace conntrack with conntrack-tools
