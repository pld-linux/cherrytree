Summary:	A hierarchical note taking application
Summary(pl.UTF-8):	Hierarchiczna aplikacja do robienia notatek
Name:		cherrytree
Version:	0.99.47
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://www.giuspen.com/software/%{name}_%{version}.tar.xz
# Source0-md5:	948329bf59ce60ceb8bd9625b5f35f62
URL:		https://www.giuspen.com/cherrytree/
BuildRequires:	curl-devel
BuildRequires:	gspell-devel
BuildRequires:	gtkmm3-devel
BuildRequires:	gtksourceviewmm3-devel
BuildRequires:	libfmt-devel
BuildRequires:	libxml++2-devel
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	shared-mime-info
BuildRequires:	spdlog-devel >= 1:1.8.1
BuildRequires:	uchardet-devel
Requires:	gspell
Requires:	gtksourceviewmm3
Requires:	libfmt
Requires:	libxml++2
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

## Remove unsupported locale
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{hi_IN,kk_KZ}

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
%{_datadir}/metainfo/com.giuspen.cherrytree.metainfo.xml
%{_desktopdir}/cherrytree.desktop
%{_datadir}/cherrytree/
%{_iconsdir}/hicolor/scalable/apps/cherrytree.svg
%{_mandir}/man1/cherrytree.1*
