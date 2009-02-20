Summary:	Simple action game: save Fred from a plummeting death!
Name:		fred
Version:	0.1.1
Release:	%mkrel 5
# Upstream source includes arial.ttf. Which is, um, copyright
# Microsoft. That's not smart. This source is upstream's tarball
# with arial.ttf and the (likely also copyright someone) grease.ttf
# removed. - AdamW 2008/02
Source0:	http://www.enormousplow.com/projects/fred/%{name}-%{version}-fontclean.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		fred-0.1.1-no-windows.patch
# Fix an error in a header file that breaks build - AdamW 2008/02
Patch1:		fred-0.1.1-build.patch
# Use DejaVu instead of arial.ttf and grease.ttf - AdamW 2008/02
Patch2:		fred-0.1.1-font.patch
License:	GPL+
URL:		http://www.enormousplow.com/projects/fred/
Group:		Games/Arcade
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	SDL_image-devel
BuildRequires:	zlib-devel
BuildRequires:	SDL_ttf-devel
Requires:	fonts-ttf-dejavu

%description
Free Fallin' Fred is a very simple clicking game.
You see the airplane going across the screen and after a while, Fred jumps.
You click on Fred to open his chute.
If you fail to open the chute in time, poor Fred will be dead.
Don't let Fred die. 

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1 -b .build
%patch2 -p1 -b .fonts

%build
rm -f install-sh
autoreconf -i
perl -pi -e 's!DATADIR = "/usr/local/share/games/fred/data/";!DATADIR = "%{_gamesdatadir}/%{name}/data/";!g' src/fred.cpp
%configure2_5x --bindir=%{_gamesbindir}
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_gamesbindir}/%{name}		  
Icon=%{name}		  		  
Categories=Game;ArcadeGame;		  
Name=Fred 
Comment=%{Summary}
EOF

%{__install} -m644 %{SOURCE11} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{__install} -m644 %{SOURCE12} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{__install} -m644 %{SOURCE13} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_gamesbindir}/%{name}
%defattr(644,root,root,755)
%dir %{_gamesdatadir}/%{name}
%{_gamesdatadir}/%{name}/*
%{_mandir}/man6/fred.6*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
%doc AUTHORS ChangeLog INSTALL NEWS README TODO

