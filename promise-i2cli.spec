%define	no_install_post_chrpath	1
Summary:	Promise I2 CLI
Summary(pl.UTF-8):	Narzędzia CLI dla kontrolerów Promise I2
Name:		promise-i2cli
Version:	2.5.0.25
Release:	1
License:	distributable
Group:		Applications/System
Source0:	http://www.promise.com/upload/Support/Utility/Linux_32bits.rar
# Source0-md5:	7e8c9c33d7023e3405c4c8e5dcc480ed
Source1:	http://www.promise.com/upload/Support/Utility/Linux_64bits.rar
# Source1-md5:	68a724fd535672c525d36aecda698a0f
URL:		http://domsch.com/linux/
BuildRequires:	rpm-utils
BuildRequires:	sed >= 4.0
BuildRequires:	unrar
ExclusiveArch:	%{ix86}
# this is lie so far since binaries are 32bit only even in Linux_64bits.rar
# ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cli is the abbreviation of Promise Technology, Inc. FastTrak serial
product utilities. It contains RAID API, command line utilities. RAID
API is the application programming interface with FastTrak serial
driver.

%description -l pl.UTF-8
cli to skrót od narzędzi dla kontrolerów szeregowych FastTrak firmy
Promise Technology, Inc. Zawiera RAID API i narzędzia linii poleceń.
RAID API to interfejs programistyczny dla sterownika szeregowego
FastTrak.

%prep
%setup -q -c -T

%ifarch %{ix86}
unrar x %{SOURCE0}
%else
unrar x %{SOURCE1}
%endif

%build
rpm2cpio *.rpm | cpio -i -d

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir}/%{name}}

install -d fixed-lib
for l in usr/lib/*6.so; do
	install $l fixed-lib/$(basename $l 6.so).so
done
install usr/sbin/cli $RPM_BUILD_ROOT%{_libdir}/%{name}
install fixed-lib/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}

sed -i -e 's#1>&# > #g' $RPM_BUILD_ROOT%{_libdir}/%{name}/libpri2plugin.so

cat << 'EOF' >  $RPM_BUILD_ROOT%{_sbindir}/promise-i2cli
#!/bin/sh
LD_LIBRARY_PATH=%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export LD_LIBRARY_PATH
cd /tmp 2> /dev/null
exec %{_libdir}/%{name}/cli $*
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc usr/share/doc/*/*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/cli
%attr(755,root,root) %{_libdir}/%{name}/*.so
