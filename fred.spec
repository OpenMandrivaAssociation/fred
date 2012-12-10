Summary:	Simple action game: save Fred from a plummeting death!
Name:		fred
Version:	0.1.1
Release:	%mkrel 8
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
Comment=Simple action game: save Fred from a plummeting death
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



%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-8mdv2011.0
+ Revision: 618339
- the mass rebuild of 2010.0 packages

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.1.1-7mdv2010.0
+ Revision: 437585
- rebuild

* Sun Feb 22 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.1.1-6mdv2009.1
+ Revision: 343911
- Fix font patch
- Fix desktop file

* Sat Feb 21 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.1.1-5mdv2009.1
+ Revision: 343526
- Remove tabs on the Name

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.1.1-4mdv2009.0
+ Revision: 245344
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Thu Feb 28 2008 Adam Williamson <awilliamson@mandriva.org> 0.1.1-2mdv2008.1
+ Revision: 175972
- rebuild for new era
- fd.o icons
- run autoreconf so everything works with modern automake / autoconf
- add font.patch (use DejaVu instead of the non-free ttf files)
- add build.patch (fixes an error in a header file that breaks build)
- new license policy
- improve summary
- spec clean
- use a modified tarball without non-free .ttf files

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - auto-convert XDG menu entry
    - kill re-definition of %%buildroot on Pixel's request
    - use %%mkrel
    - import fred


* Tue Feb 15 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.1.1-1mdk
- 0.1.1 (it works!)
- drop P1 (fixed upstream)

* Wed Jun 16 2004 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 0.1.0-4mdk
- rebuild

* Fri Apr 02 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.1.0-3mdk
- rebuild
- fix buildrequires (lib64..)
- change summary macro to avoid possible conflicts if we were to build debug package

* Thu Mar 20 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.1.0-2mdk
- switched to other unix specific sources
- updated Patch1
- now use configure macro
- updated docs
- dropped Patch0

* Tue Feb 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.1.0-1mdk
- Corrected title
- 0.1.0
- Don't use the make macro as it won't support multiple jobs

* Thu Nov 19 2002 Per Øyvind Karlsen <peroyvind@delonic.no> 0.0.4-1mdk
- First release
