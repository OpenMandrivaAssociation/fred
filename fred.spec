%define	name	fred
%define	version	0.1.1
%define	release	 %mkrel 1
%define Summary	Free Fallin' Fred

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://www.enormousplow.com/projects/fred/%{name}-%{version}.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
Patch0:		fred-0.1.1-no-windows.patch.bz2
License:	GPL
Url:		http://www.enormousplow.com/projects/fred/
Group:		Games/Arcade
BuildRequires:	SDL_image-devel zlib-devel SDL_ttf-devel

%description
Free Fallin' Fred is a very simple clicking game.
You see the airplane going across the screen and after a while, Fred jumps.
You click on Fred to open his chute.
If you fail to open the chute in time, poor Fred will be dead.
Don't let Fred die. 

%prep
%setup -q -n %{name}
%patch0 -p1

%build
autoconf
perl -pi -e 's!DATADIR = "/usr/local/share/games/fred/data/";!DATADIR = "%{_gamesdatadir}/%{name}/data/";!g' src/fred.cpp
%configure2_5x	--bindir=%{_gamesbindir}
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_gamesbindir}/%{name}		  
Icon=%{name}		  		  
Categories=Game;ArcadeGame;		  
Name=Fred		  
Comment=%{Summary}
EOF

%{__install} -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
%{__install} -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
%{__install} -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root,755)
%{_gamesbindir}/%{name}
%defattr(644,root,root,755)
%dir %{_gamesdatadir}/%{name}
%{_gamesdatadir}/%{name}/*
%{_mandir}/man6/fred.6*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop
%doc AUTHORS ChangeLog INSTALL NEWS README TODO

