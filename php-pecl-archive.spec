%define		_modname	archive
%define		_status		beta

Summary:	%{_modname} - manipulate tar/cpio archives
Summary(pl):	%{_modname} - obróbka archiwów tar/cpio
Name:		php-pecl-%{_modname}
Version:	0.2
Release:	2
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	1b121440b2c460b2a1af46e31f23e46e
URL:		http://pecl.php.net/package/archive/
BuildRequires:	libarchive-devel
BuildRequires:	libtool
BuildRequires:	php-devel >= 3:5.0.0
Requires:	php-common >= 3:5.0.0
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
archive extension allows to read and write tar and cpio archives using
libarchive.

In PECL status of this extension is: %{_status}.

%description -l pl
Rozszerzenie archive pozwala na odczyt i zapis archiwów tar oraz cpio
przy u¿yciu biblioteki libarchive.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{API.txt,CREDITS,tests}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
