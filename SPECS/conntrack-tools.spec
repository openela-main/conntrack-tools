Name:           conntrack-tools
Version:        1.4.4
Release:        11%{?dist}
Summary:        Manipulate netfilter connection tracking table and run High Availability
Group:          System Environment/Base
License:        GPLv2
URL:            http://conntrack-tools.netfilter.org/
Source0:        http://netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
Source1:        conntrackd.service
Source2:        conntrackd.conf

Patch1:		conntrack-tools-1.4.4-nat_tuple-leak.patch
Patch2:		conntrack-tools-1.4.4-free-pktb-after-use.patch
Patch3:		conntrack-Fix-CIDR-to-mask-conversion-on-Big-Endian.patch
Patch4:		nfct-helper-Fix-NFCTH_ATTR_PROTO_L4NUM-size.patch
Patch5:		0005-conntrackd-set-default-hashtable-buckets-and-max-ent.patch

BuildRequires:  libnfnetlink-devel >= 1.0.1, libnetfilter_conntrack-devel >= 1.0.6
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
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
export LDFLAGS="${LDFLAGS} -Wl,-z,lazy"
%configure --disable-static --enable-systemd
sed -i "s/DEFAULT_INCLUDES = -I./DEFAULT_INCLUDES = -I. -I\/usr\/include\/tirpc/" src/helpers/Makefile

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
* Fri Nov 04 2022 Phil Sutter <psutter@redhat.com> - 1.4.4-11
- conntrackd: set default hashtable buckets and max entries if not specified

* Mon Nov 18 2019 Phil Sutter <psutter@redhat.com> - 1.4.4-10
- Fix issues on Big Endian (rhbz#1750744)

* Thu Feb 14 2019 Phil Sutter - 1.4.4-9
- Fix previous attempt at linking with -z lazy

* Tue Dec 11 2018 Paul Wouters <pwouters@redhat.com> - 1.4.4-8
- Resolves: rhbz#1646885 [RHEL8] nfct tool lib have undefined symbol
- enable systemd support

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
