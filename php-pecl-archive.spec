%define		_modname	archive
%define		_status		beta
Summary:	%{_modname} - manipulate tar/cpio archives
Summary(pl.UTF-8):	%{_modname} - obróbka archiwów tar/cpio
Name:		php-pecl-%{_modname}
Version:	0.2
Release:	10
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	1b121440b2c460b2a1af46e31f23e46e
Patch0:		%{name}-php52.patch
URL:		http://pecl.php.net/package/archive/
BuildRequires:	libarchive-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
archive extension allows to read and write tar and cpio archives using
libarchive.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
Rozszerzenie archive pozwala na odczyt i zapis archiwów tar oraz cpio
przy użyciu biblioteki libarchive.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
cd %{_modname}-%{version}
%patch0 -p0

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{API.txt,CREDITS,tests}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
