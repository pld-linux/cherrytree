Summary:	A hierarchical note taking application
Summary(pl.UTF-8):	Hierarchiczna aplikacja do robienia notatek
Name:		cherrytree
Version:	1.6.1
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://www.giuspen.com/software/%{name}_%{version}.tar.xz
# Source0-md5:	06ea62579d982a015e33c0540d4a1a83
URL:		https://www.giuspen.com/cherrytree/
BuildRequires:	cmake >= 3.5
BuildRequires:	curl-devel
BuildRequires:	fribidi-devel
BuildRequires:	glibmm-devel >= 2.4
BuildRequires:	gspell-devel >= 1.0
BuildRequires:	gtkmm3-devel >= 3.0
BuildRequires:	gtksourceview4-devel >= 3.0
BuildRequires:	libfmt-devel >= 6.0
# C++17
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libxml++2-devel >= 2.6
BuildRequires:	pangomm-devel >= 1.4
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	shared-mime-info
BuildRequires:	spdlog-devel >= 1:1.8.1
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	uchardet-devel
BuildRequires:	vte-devel
Requires:	shared-mime-info
Requires:	spdlog >= 1:1.8.1
Suggests:	p7zip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A hierarchical note taking application, featuring rich text and syntax
highlighting, storing all the data (including images) in a single xml
file with extension ".ctd".

%description -l pl.UTF-8
Hierarchiczna aplikacja do notatek, wspierająca tekst sformatowany i
wyróżnianie składni, przechowująca wszystkie dane (w tym obrazy) w
jednym pliku XML z rozszerzeniem „.ctd”.

%prep
%setup -q -n %{name}_%{version}

%build
install -d build
cd build
%cmake .. \
	-DMAKE_BUILD_TYPE=Release \
	-DBUILD_TESTING=OFF

%{__make} cherrytree

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

## Remove old mime registration files
%{__rm} $RPM_BUILD_ROOT%{_datadir}/mime-info/cherrytree.*

# unify locale dirs
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{hi_IN,hi}
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{kk_KZ,kk}
# should be kk@latin, but not supported
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/kk_LA

%find_lang %{name}

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%postun
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc changelog.txt license.txt
%attr(755,root,root) %{_bindir}/cherrytree
%{_datadir}/cherrytree
%{_datadir}/metainfo/net.giuspen.cherrytree.metainfo.xml
%{_desktopdir}/cherrytree.desktop
%{_iconsdir}/hicolor/scalable/apps/cherrytree.svg
%{_mandir}/man1/cherrytree.1*
