Name:             %{name}
Version:          %{version}
Release:          %{release}

%define name      gallery
%define major	  2
%define version   2.3
%define release   %mkrel 3
%define _webroot  %{_var}/www/%{name}

Summary:          Customizable photo gallery web site
Source0:          http://downloads.sourceforge.net/gallery/gallery-%{version}-full.tar.gz
#Source1:		  README.urpmi
License:          GPLv2+
Group:            Networking/WWW
Requires:	  apache-mod_php
Requires:         php-gd
Requires(post):   rpm-helper
Requires(postun): rpm-helper
BuildArch:        noarch
Url:              http://gallery.menalto.com
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%__mkdir_p %{buildroot}%{_webroot}
%__cp -pR * %{buildroot}%{_webroot}
%__mkdir_p %{buildroot}%{_sysconfdir}/%{name}

## Create a robot.txt
%__cat > %{buildroot}%{_sysconfdir}/%{name}/robots.txt << EOF
User-agent: *
Disallow:   /
EOF
%__ln_s -f %{_sysconfdir}/%{name}/robots.txt %{buildroot}%{_webroot}/

## Create a config file for apache
%__mkdir_p %{buildroot}%{_webappconfdir}
%__cat > %{buildroot}%{_webappconfdir}/%{name}.conf << EOF
Alias /%{name} %{_webroot}

<Directory %{_webroot}>
  AllowOverride Options FileInfo
  <Files ~ "\.(inc|class)$">
     Order Deny,Allow
     Deny from All
  </Files>
</Directory>

<Directory %{_webroot}/g2data>
    Order Deny,Allow
    Deny from All
</Directory>

<Directory /var/www/gallery/install>
    Order Deny,Allow
    Deny from All
    Allow from localhost, 127.0.0.1
</Directory>

<Files %{_webroot}/.htaccess>
    Order Deny,Allow
    Deny from all
</Files>
EOF

## Create an empty login.txt file needed for install
## Admin will have to copy here the key given by gallery
touch %{buildroot}%{_sysconfdir}/%{name}/login.txt 
%__ln_s -f %{_sysconfdir}/%{name}/login.txt %{buildroot}%{_webroot}/

## Create config.php, which gallery will populate
%__cat > %{buildroot}%{_sysconfdir}/%{name}/config.php << EOF
<?php /* This file intentionally empty - it is populated during Gallery's setup / configuration process */ 
\$gallery->setConfig('data.gallery.base', '%{_webroot}/g2data');
?>
EOF
%__ln_s -f %{_sysconfdir}/%{name}/config.php %{buildroot}%{_webroot}/
chmod 644 %{buildroot}%{_sysconfdir}/%{name}/config.php

## Create an empty .htaccess file which gallery will configure
%__cat > %{buildroot}%{_webroot}/.htaccess << EOF
# url rewriting can be done via gallery rewrite module
EOF
chmod 644 %{buildroot}%{_webroot}/.htaccess

## Create default data directory
%__mkdir_p %{buildroot}%{_webroot}/g2data
chmod 740 %{buildroot}%{_webroot}/

## Give perl scripts u+x
chmod 744 %{buildroot}%{_webroot}/lib/tools/po/premerge-messages.pl
chmod 744 %{buildroot}%{_webroot}/lib/tools/po/header.pl
chmod 744 %{buildroot}%{_webroot}/lib/tools/po/update-all-translations.pl

## Move doc files to %{_datadir}/doc
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
#%__cp %{SOURCE1} %{buildroot}%{_datadir}/doc/%{name}/
%__mv %{buildroot}%{_webroot}/LICENSE %{buildroot}%{_datadir}/doc/%{name}/
%__mv %{buildroot}%{_webroot}/MANIFEST %{buildroot}%{_datadir}/doc/%{name}/
%__mv %{buildroot}%{_webroot}/README.html %{buildroot}%{_datadir}/doc/%{name}/


## Collect and mark locale-dependent files
## %%find_lang

%clean
%__rm -rf %{buildroot}

%post
%_post_webapp

%postun
%_postun_webapp

%files
%defattr(0644,root,root,-)
%config(noreplace) %{_webappconfdir}/%{name}.conf
%{_webroot}/bootstrap.inc
%{_webroot}/embed.php
%{_webroot}/config.php
%{_webroot}/images/
%{_webroot}/index.php
%{_webroot}/init.inc
%{_webroot}/install/
%{_webroot}/lib/
%{_webroot}/login.txt
%{_webroot}/main.php
%{_webroot}/robots.txt
%{_sysconfdir}/%{name}/robots.txt
%dir %{_webroot}
%dir %{_webroot}/modules
%{_webroot}/modules/core/
%dir %{_webroot}/themes
%{_webroot}/locale/
%{_webroot}/upgrade/
%doc %{_datadir}/doc/%{name}/LICENSE
%doc %{_datadir}/doc/%{name}/MANIFEST
%doc %{_datadir}/doc/%{name}/README.html
#%doc %{_datadir}/doc/%{name}/README.urpmi
%attr(-,apache,root) %config(noreplace) %{_webroot}/.htaccess
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/login.txt
%attr(-,apache,root) %config(noreplace) %{_sysconfdir}/%{name}/config.php
%attr(-,apache,root) %config(noreplace) %dir %{_webroot}/g2data
%{_webroot}/modules/albumselect/
%{_webroot}/modules/archiveupload/
%{_webroot}/modules/captcha/
%{_webroot}/modules/cart/
%{_webroot}/modules/colorpack/
%{_webroot}/modules/comment/
%{_webroot}/modules/customfield/
%{_webroot}/modules/dcraw/
%{_webroot}/modules/debug/
%{_webroot}/modules/digibug/
%{_webroot}/modules/dynamicalbum/
%{_webroot}/modules/ecard/
%{_webroot}/modules/exif/
%{_webroot}/modules/ffmpeg/
%{_webroot}/modules/flashvideo/
%{_webroot}/modules/fotokasten/
%{_webroot}/modules/gd/
%{_webroot}/modules/getid3/
%{_webroot}/modules/hidden/
%{_webroot}/modules/httpauth/
%{_webroot}/modules/icons/
%{_webroot}/modules/imageblock/
%{_webroot}/modules/imageframe/
%{_webroot}/modules/imagemagick/
%{_webroot}/modules/jpegtran/
%{_webroot}/modules/linkitem/
%{_webroot}/modules/itemadd/
%{_webroot}/modules/keyalbum/
%{_webroot}/modules/members/
%{_webroot}/modules/migrate/
%{_webroot}/modules/mime/
%{_webroot}/modules/mp3audio/
%{_webroot}/modules/multilang/
%{_webroot}/modules/multiroot/
%{_webroot}/modules/netpbm/
%{_webroot}/modules/newitems/
%{_webroot}/modules/nokiaupload/
%{_webroot}/modules/notification/
%{_webroot}/modules/panorama/
%{_webroot}/modules/password/
%{_webroot}/modules/permalinks/
%{_webroot}/modules/photoaccess/
%{_webroot}/modules/picasa/
%{_webroot}/modules/publishxp/
%{_webroot}/modules/quotas/
%{_webroot}/modules/randomhighlight/
%{_webroot}/modules/rating/
%{_webroot}/modules/rearrange/
%{_webroot}/modules/register/
%{_webroot}/modules/remote/
%{_webroot}/modules/replica/
%{_webroot}/modules/reupload/
%{_webroot}/modules/rewrite/
%{_webroot}/modules/rss/
%{_webroot}/modules/search/
%{_webroot}/modules/shutterfly/
%{_webroot}/modules/sitemap/
%{_webroot}/modules/sizelimit/
%{_webroot}/modules/slideshow/
%{_webroot}/modules/slideshowapplet/
%{_webroot}/modules/snapgalaxy/
%{_webroot}/modules/squarethumb/
%{_webroot}/modules/thumbnail/
%{_webroot}/modules/thumbpage/
%{_webroot}/modules/uploadapplet/
%{_webroot}/modules/useralbum/
%{_webroot}/modules/watermark/
%{_webroot}/modules/webcam/
%{_webroot}/modules/webdav/
%{_webroot}/modules/zipcart/
%{_webroot}/themes/ajaxian/
%{_webroot}/themes/carbon/
%{_webroot}/themes/classic/
%{_webroot}/themes/floatrix/
%{_webroot}/themes/hybrid/
%{_webroot}/themes/matrix/
%{_webroot}/themes/siriux/
%{_webroot}/themes/slider/
%{_webroot}/themes/tile/


%changelog
* Sun Oct  4 2009 Jerome Martin <jmartin@mandriva.org> 2.3-3mdv2009.1
- Removed missing README.urpmi
- Fixed rigths

* Thu Feb 20 2009 David Pernot <dpernot@gmail.com> 2.3-2mdv2009.1
- Change name gallery2 to gallery
- Change README-mandriva-gallery2 to README.urpmi
- Remove requires apache
- Add a webroot macro to /var/www/gallery

* Tue Feb 17 2009 David Pernot <dpernot@gmail.com> 2.3-1mdv2009.1
- First build
