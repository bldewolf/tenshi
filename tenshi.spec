#--------------------------------------------------------------------------------
#  Program:  tenshi.spec
#
#  Purpose:  This is the data file user to generate RPM files so that we can
#            distrbute 'canned' versions of what we have done more easily.
#--------------------------------------------------------------------------------
#  10-Nov-06 - REP - Initial version

#--------------------------------------------------------------------------------
#  Some basic definitions for use to use later in the file.  We really only want
#  to define things once, and have to change things in only one place.
#--------------------------------------------------------------------------------
%define name       tenshi
%define version    0.9.1
%define release    1
%define mandir     /usr/share/man
%define sbindir    /usr/sbin

#--------------------------------------------------------------------------------
#  Basic package information
#--------------------------------------------------------------------------------
Summary:           Tenshi log monitoring program
Name:              %{name}
Version:           %{version}
Release:           %{release}
Group:             System Environment/Daemons
License:           ISC-style
Url:               http://dev.inversepath.com/trac/tenshi/wiki/
Source0:           %{name}-%{version}.tar.gz
Requires:          perl
Buildroot:         %{_tmppath}/%{name}-buildroot

#--------------------------------------------------------------------------------
#  Description of the package
#--------------------------------------------------------------------------------
%description
tenshi is a log monitoring program, designed to watch one or more log
files for lines matching user defined regular expressions and report
on the matches. The regular expressions are assigned to queues which
have an alert interval and a list of mail recipients.

#--------------------------------------------------------------------------------
#  What things to do in preparation of making the package
#--------------------------------------------------------------------------------
%prep
%setup

#--------------------------------------------------------------------------------
#  The build process for the package
#--------------------------------------------------------------------------------
%build

#--------------------------------------------------------------------------------
#  Configuration process for the package
#--------------------------------------------------------------------------------

### No configure process for tenshi

#--------------------------------------------------------------------------------
#  The install process for the package
#--------------------------------------------------------------------------------
%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/etc/sysconfig
mkdir -p %{buildroot}/usr/share/man/man8/
mkdir -p %{buildroot}/var/run/%{name}/

make DESTDIR=%{buildroot} mandir=%{_mandir} install

install -m755 tenshi.redhat-init %{buildroot}%{_initrddir}/%{name}
touch %{buildroot}/etc/sysconfig/%{name}
touch %{buildroot}/var/run/%{name}/%{name}.pid

#--------------------------------------------------------------------------------
#  Things to run after it has been installed.
#--------------------------------------------------------------------------------
%post
/sbin/chkconfig --add %{name}
# Manually add user/group
%{sbindir}/groupadd %{name}
%{sbindir}/useradd -g %{name} -d %{_sysconfdir}/%{name} -s /bin/false %{name}

#--------------------------------------------------------------------------------
#  Take tenshi out of runlevels
#--------------------------------------------------------------------------------
%preun
if [ "$1" = 0 ]; then
  /sbin/chkconfig --del %{name}
fi

#--------------------------------------------------------------------------------
#  Remove tenshi user/group if necessary (since "tenshi" is the only
#  member of group "tenshi", then deletion of "tenshi" user deletes
#  the group.
#--------------------------------------------------------------------------------
%postun
if [ "$1" = 0 ]; then
  %{sbindir}/userdel tenshi
fi

#--------------------------------------------------------------------------------
#  What files and permissions are included in the package
#--------------------------------------------------------------------------------
%files
%defattr(644,root,root,755)
%doc README INSTALL CREDITS LICENSE Changelog FAQ
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) /etc/sysconfig/%{name}
%attr(755,root,root) %config(noreplace) %{_initrddir}/%{name}
%attr(755,root,root) %{sbindir}/%{name}
%{_mandir}/man8/%{name}.8*
%dir %attr(775,tenshi,tenshi) /var/run/%{name}
%ghost %attr(600,tenshi,tenshi) /var/run/%{name}/%{name}.pid

#--------------------------------------------------------------------------------
#  What final cleanup should occur after the package construction has been
#  completed
#--------------------------------------------------------------------------------
%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

#--------------------------------------------------------------------------------
#  Changelog
#--------------------------------------------------------------------------------
%changelog
* Mon Aug 27 2007 Andrea Barisani <andrea@inversepath.com> 0.8
  - assorted fixes, thanks goes to Elan Ruusam�e <glen@delfi.ee>
* Fri Nov 10 2006 Steven McCoy, Jr. <steven@indigorobot.com> 0.6-1
  - Initial specfile/rpm creation. Used syslog-ng.spec as template
  - Thanks to: Richard E. Perlotto II (syslog-ng spec maintainer)
