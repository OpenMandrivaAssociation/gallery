Name:             %{name}
Version:          %{version}
Release:          %{release}

%define name      gallery
%define major	  2
%define version   2.3
%define release   %mkrel 4

Summary:          Customizable photo gallery web site
Url:              http://gallery.menalto.com
Source0:          http://downloads.sourceforge.net/gallery/gallery-%{version}-full.tar.gz
#Source1:		  README.urpmi
License:          GPLv2+
Group:            Networking/WWW
Requires:	  apache-mod_php
Requires:         php-gd
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:        noarch
BuildRoot:        %{_tmppath}/%{name}-%{version}

%description
Gallery is an open source web based photo album organizer. You must
have your own website with PHP and database support in order to
install and use it. With Gallery you can easily create and maintain
albums of photos (and videos) via an intuitive interface. Photo
management includes automatic thumbnail creation, image resizing,
rotation, ordering, captioning, searching and more. Albums and photos
can have view, edit, delete and other permissions per individual
authenticated user for an additional level of privacy.

%prep
%setup -q -n %{name}%{major}

%build

%install
%__rm -fr %{buildroot}
%__mkdir_p %{buildroot}%{_var}/www/%{name}
%__cp -pR * %{buildroot}%{_var}/www/%{name}
%__mkdir_p %{buildroot}%{_sysconfdir}/%{name}

## Create a config file for apache
%__mkdir_p %{buildroot}%{_webappconfdir}
%__cat > %{buildroot}%{_webappconfdir}/%{name}.conf << EOF
Alias /%{name} %{_var}/www/%{name}

<Directory %{_var}/www/%{name}>
    AllowOverride Options FileInfo

    Order allow,deny
    Allow from all
    <Files ~ "\.(inc|class)$">
         Order deny,allow
         Deny from all
    </Files>

    <Files .htaccess>
         Order deny,allow
         Deny from all
    </Files>
</Directory>

<Directory %{_var}/www/%{name}/g2data>
    Order deny,allow
    Deny from all
</Directory>

<Directory /var/www/gallery/install>
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
    ErrorDocument 403 "Access denied per %{_webappconfdir}/%{name}.conf"
</Directory>
EOF

## Create an empty login.txt file needed for install
## Admin will have to copy here the key given by gallery
touch %{buildroot}%{_sysconfdir}/%{name}/login.txt 
%__ln_s -f %{_sysconfdir}/%{name}/login.txt %{buildroot}%{_var}/www/%{name}/

## Create config.php, which gallery will populate
%__cat > %{buildroot}%{_sysconfdir}/%{name}/config.php << EOF
<?php /* This file intentionally empty - it is populated during Gallery's setup / configuration process */ 
\$gallery->setConfig('data.gallery.base', '%{_var}/www/%{name}/g2data');
?>
EOF
%__ln_s -f %{_sysconfdir}/%{name}/config.php %{buildroot}%{_var}/www/%{name}/
chmod 644 %{buildroot}%{_sysconfdir}/%{name}/config.php

## Create an empty .htaccess file which gallery will configure
%__cat > %{buildroot}%{_var}/www/%{name}/.htaccess << EOF
# url rewriting can be done via gallery rewrite module
EOF
chmod 644 %{buildroot}%{_var}/www/%{name}/.htaccess

## Create default data directory
%__mkdir_p %{buildroot}%{_var}/www/%{name}/g2data
chmod 740 %{buildroot}%{_var}/www/%{name}/

## Give perl scripts u+x
chmod 744 %{buildroot}%{_var}/www/%{name}/lib/tools/po/premerge-messages.pl
chmod 744 %{buildroot}%{_var}/www/%{name}/lib/tools/po/header.pl
chmod 744 %{buildroot}%{_var}/www/%{name}/lib/tools/po/update-all-translations.pl

# remove documentation files
rm -f %{buildroot}%{_var}/www/%{name}/README.html
rm -f %{buildroot}%{_var}/www/%{name}/LICENSE
rm -f %{buildroot}%{_var}/www/%{name}/MANIFEST

## Collect and mark locale-dependent files
## %%find_lang

%clean
%__rm -rf %{buildroot}

%post
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(0644,root,root,-)
%doc LICENSE MANIFEST README.html
%attr(-,apache,root) %config(noreplace) %{_var}/www/%{name}/.htaccess
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/login.txt
%attr(-,apache,root) %config(noreplace) %{_sysconfdir}/%{name}/config.php
%attr(-,apache,root) %config(noreplace) %dir %{_var}/www/%{name}/g2data
%config(noreplace) %{_webappconfdir}/%{name}.conf
%{_var}/www/%{name}
