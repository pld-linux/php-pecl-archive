#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname		archive
%define		status		beta
Summary:	%{modname} - manipulate tar/cpio archives
Summary(pl.UTF-8):	%{modname} - obróbka archiwów tar/cpio
Name:		%{php_name}-pecl-%{modname}
Version:	0.3.1
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-0.2.tgz
# Source0-md5:	1b121440b2c460b2a1af46e31f23e46e
Patch100:	branch.diff
URL:		http://pecl.php.net/package/archive/
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	libarchive-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%{?with_tests:BuildRequires:	%{php_name}-cli}
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-archive < 0.2-17
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
archive extension allows to read and write tar and cpio archives using
libarchive.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie archive pozwala na odczyt i zapis archiwów tar oraz cpio
przy użyciu biblioteki libarchive.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-*/* .
%patch100 -p1

%build
phpize
%configure
%{__make}

%if %{with tests}
# simple module load test
%{__php} -n \
	-dextension_dir=modules \
	-dextension=%{modname}.so \
	-m > modules.log
grep %{modname} modules.log
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}
install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%doc API.txt CREDITS tests
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
