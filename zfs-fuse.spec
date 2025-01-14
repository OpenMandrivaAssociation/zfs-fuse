Name:		zfs-fuse
Version:	0.6.0
Release:	3
Summary: 	ZFS file system support for FUSE
License:	CDDL
Group:		System/Libraries
URL:		https://zfs-fuse.net
Source0:	http://zfs-fuse.net/releases/%{version}/%{name}-%{version}.tar.bz2
Source1:	%name.init
Source2:	http://www.sun.com/bigadmin/scripts/sunScripts/zfs_completion.bash.txt
Source3:	zfs.1m
Source4:	zpool.1m
Source5:	zdb.1m
# Patch0:		zfs-fuse-0.4.0_beta1-gcc4.2.patch
# Patch1:		zfs-fuse-0.4.0_beta1-daemon.patch
# Packager:	Chris Hills <chaz@chaz6.com>
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: gcc-c++ fuse-devel scons libaio-devel zlib-devel
Requires:      fuse
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description
zfs-fuse is a port of Solaris zfs filesystem to the FUSE framework for Linux.

%prep
%setup -q
#patch0 -p1
#patch1 -p1

%build
cd src
scons 

%install
rm -rf %{buildroot}
cd src
scons install install_dir=%{buildroot}/%_sbindir
mkdir -p -m 0755 %{buildroot}/%{_initrddir}
install -m 0755 %SOURCE1 %{buildroot}/%{_initrddir}/%name
mkdir -p -m 0755 %{buildroot}/%{_sysconfdir}/bash_completion.d
install -m 0644 %SOURCE2 %{buildroot}/%{_sysconfdir}/bash_completion.d/%name
mkdir -p -m 0755 %{buildroot}/%{_mandir}/man1
install -m 0644 %SOURCE3 %{buildroot}/%{_mandir}/man1/zfs.1
install -m 0644 %SOURCE4 %{buildroot}/%{_mandir}/man1/zpool.1
install -m 0644 %SOURCE5 %{buildroot}/%{_mandir}/man1/zdb.1

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %_sbindir/*
%attr(0755,root,root) %config(noreplace) %{_initrddir}/%name
%config(noreplace) %{_sysconfdir}/bash_completion.d/%name
%{_mandir}/*/*
%doc BUGS CHANGES HACKING INSTALL LICENSE README STATUS TESTING TODO

%preun
%_preun_service %name

%post
%_post_service %name

%postun
if [ $1 -ge 1 ] ; then
  service %name condrestart >/dev/null 2>&1
fi
