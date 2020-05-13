%define name		bumblebee-config-gui
%define Summary         Graphical Bumblebee Configuration
%define Summary_hu      Grafikus Bumblebee beállítófelület
%define sourcetype      tar.xz
%define version         0.7.0

Name: 		%name
Summary: 	%Summary
Summary(hu): 	%Summary_hu
Version:	%version
Release: 	%mkrel 2
License: 	GPL3
Distribution:	blackPanther OS
Vendor:    	blackPanther Europe
Packager:  	Charles K Barcza <kbarcza@blackpanther.hu>
Group: 		System/Configuration
Source0:	%name-%version.%sourcetype
Buildarch:	noarch
BuildRequires:	python3 >= 3.7
Requires: 	python3-gobject3
Requires: 	bumblebee-ui 
Requires:	bumblebee
Requires:	gettext

%description
%Summary

%description -l hu
%Summary_hu

%files
%defattr(-,root,root)
%_bindir/%name
%_datadir/applications/*.desktop
%python3_sitelib/bumblebee_config
%python3_sitelib/bumblebee_config*.egg-info
%_iconsdir/*.png
%_iconsdir/*/*.png
%_iconsdir/hicolor/scalable/apps/%{name}.svg

%prep
%setup -q 
sed -i "s|../img/bumblebee-config.svg|%{_iconsdir}/hicolor/scalable/apps/%{name}.svg|" bumblebee_config/main_window.ui

%build
%py3_build

%install
%py3_install


%define  nameicon img/bumblebee-config.png
mkdir -p -m755 %{buildroot}{%_liconsdir,%_iconsdir,%_miconsdir}
convert -scale 48x48 %{nameicon} %{buildroot}/%{_liconsdir}/%{name}.png
convert -scale 32x32 %{nameicon} %{buildroot}/%{_iconsdir}/%{name}.png
convert -scale 16x16 %{nameicon} %{buildroot}/%{_miconsdir}/%{name}.png
install -d -m 755 %{buildroot}%{_iconsdir}/hicolor/scalable/apps
install -m 644 img/bumblebee-config.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
pushd %buildroot%_bindir
mv bumblebee-config %name
popd


%clean
rm -rf %buildroot


%changelog
* Wed May 13 2020 Charles K. Barcza <info@blackpanther.hu> 0.7.0-2bP
- build package for blackPanther OS v17-19.x 32/64 bit or ARM
- dependency fix
- publish spec
- fix summary
-------------------------------------------------------------------------
* Tue May 12 2020 Charles K. Barcza <info@blackpanther.hu> 0.7.0-1bP
- build package for blackPanther OS v17-19.x 32/64 bit or ARM
- ported
- write to Python3
- add logo 
- edit logo path
- disable apt work only Ubuntu
. fix stderr 
- add first Hungarian translation
-------------------------------------------------------------------------

* Thu Sep 05 2016 Charles Barcza <info@blackpanther.hu> 
- build for blackPanther OS
----------------------------------------------------------
