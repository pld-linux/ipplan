Summary:	Package that uses webapps configuration
Summary(pl.UTF-8):	Pakiet używający konfiguracji aplikacji WWW
Name:		ipplan
Version:	4.92
Release:	0.1
License:	GPL v2+
Group:		Applications/WWW
Source0:	http://downloads.sourceforge.net/iptrack/ipplan/%{name}-%{version}.tar.gz
# Source0-md5:	2540b381744d1891b53b660fffc5ec56
URL:		http://iptrack.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires(triggerpostun):	sed >= 4.0
Requires:	webserver(access)
Requires:	webserver(alias)
#Requires:	webserver(auth)
#Requires:	webserver(cgi)
#Requires:	webserver(indexfile)
#Requires:	webserver(php)
#Requires:	webserver(setenv)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description

%description -l pl.UTF-8

%prep
%setup -q -n %{name}

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

cp -a *.js *.jpg *.php $RPM_BUILD_ROOT%{_appdir}
cp -a admin adodb contrib images layout menus templates themes user $RPM_BUILD_ROOT%{_appdir}

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_appdir}
%{_appdir}/admin
%{_appdir}/adodb
%{_appdir}/contrib
%{_appdir}/images
%{_appdir}/layout
%{_appdir}/menus
%{_appdir}/templates
%{_appdir}/themes
%{_appdir}/user
%{_appdir}/*.js
%{_appdir}/*.jpg
%{_appdir}/*.php
