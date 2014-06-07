Name:           cube
Version:        4.2.2
Release:        2%{?dist}
Summary:        CUBE Uniform Behavioral Encoding generic presentation component

License:        BSD
URL:            http://www.scalasca.org/software/cube-4.x/download.html
Source0:        http://apps.fz-juelich.de/scalasca/releases/cube/4.2/dist/cube-%{version}.tar.gz
# Lnk libcube4 against -lz
Patch0:         cube-link.patch

BuildRequires:  dbus-devel
BuildRequires:  qt4-devel
BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  xerces-j2
BuildRequires:  chrpath
BuildRequires:  desktop-file-utils

%description
CUBE (CUBE Uniform Behavioral Encoding) is a generic presentation component
suitable for displaying a wide variety of performance metrics for parallel
programs including MPI and OpenMP applications. CUBE allows interactive
exploration of a multidimensional performance space in a scalable fashion.
Scalability is achieved in two ways: hierarchical decomposition of individual
dimensions and aggregation across different dimensions. All performance
metrics are uniformly accommodated in the same display and thus provide the
ability to easily compare the effects of different kinds of performance
behavior.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
The %{name}-doc package contains documentation for %{name}.


%package        java
Summary:        CUBE reader for Java
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch
Requires:       java
Requires:       jpackage-utils

%description    java
The %{name}-java package contains a CUBE reader written in Java.


%prep
%setup -q
%patch0 -p1 -b .link
sed -i -e 's/"//g' CUBE.desktop.in


%build
# We need to explicitly set CXX here so that scorep picks it up
%configure --disable-static \
  --disable-silent-rules \
  --with-platform=linux \
  --with-java-reader=yes \
  --with-xerces-name=xerces-j2.jar
make
# %{?_smp_mflags} - CubeReader.jar fails


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Install doc
cp -p AUTHORS ChangeLog COPYING NEWS README \
      %{buildroot}%{_defaultdocdir}/%{name}/

# Strip rpath
chrpath -d -k %{buildroot}%{_bindir}/* || :

# Fix jar install location
mkdir -p %{buildroot}%{_datadir}/java
mv %{buildroot}%{_libdir}/CubeReader.jar %{buildroot}%{_datadir}/java/CubeReader.jar

# Install desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications CUBE.desktop

# Move documentatioin to proper location
mv %{buildroot}%{_datadir}/%{name}/doc/* %{buildroot}%{_defaultdocdir}/%{name}/
rm -r %{buildroot}%{_datadir}/%{name}

# Not needed since we install into the system dirs
rm -r %{buildroot}%{_datadir}/modulefiles


%check
make check


%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%dir %{_defaultdocdir}/cube/
%{_defaultdocdir}/cube/AUTHORS
%{_defaultdocdir}/cube/ChangeLog
%{_defaultdocdir}/cube/COPYING
%{_defaultdocdir}/cube/NEWS
%{_defaultdocdir}/cube/README
%{_bindir}/cube
%{_bindir}/cube3to4
%{_bindir}/cube4to3
%{_bindir}/cube_calltree
%{_bindir}/cube_canonize
%{_bindir}/cube_clean
%{_bindir}/cube_cmp
%{_bindir}/cube_cut
%{_bindir}/cube_derive
%{_bindir}/cube_diff
%{_bindir}/cube_dump
%{_bindir}/cube_exclusify
%{_bindir}/cube_inclusify
%{_bindir}/cube_info
%{_bindir}/cube_is_empty
%{_bindir}/cube_mean
%{_bindir}/cube_merge
%{_bindir}/cube_nodeview
%{_bindir}/cube_part
%{_bindir}/cube_rank
%{_bindir}/cube_regioninfo
%{_bindir}/cube_remap2
%{_bindir}/cube_sanity
%{_bindir}/cube_score
%{_bindir}/cube_stat
%{_bindir}/cube_test
%{_bindir}/cube_topoassist
%{_bindir}/tau2cube
%{_libdir}/lib%{name}*.so.4*
%{_datadir}/applications/CUBE.desktop
%{_datadir}/icons/Cube.xpm

%files devel
%{_bindir}/cube-config
%{_bindir}/cube-config-backend
%{_bindir}/cube-config-frontend
%{_includedir}/%{name}*/
%{_libdir}/lib%{name}*.so

%files doc
%{_defaultdocdir}/cube/

%files java
%{_datadir}/java/CubeReader.jar


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 3 2014 Orion Poplawski <orion@cora.nwra.com> - 4.2.2-1
- Update to 4.2.2
- Fix doc duplication
- Add icon and destop-database scriptlets
- Use chrpath to strip rpaths

* Fri Feb 28 2014 Orion Poplawski <orion@cora.nwra.com> - 4.2.1-2
- Add %%check

* Wed Feb 26 2014 Orion Poplawski <orion@cora.nwra.com> - 4.2.1-1
- Update to 4.2.1

* Fri Nov 8 2013 Orion Poplawski <orion@cora.nwra.com> - 4.2-3
- Fix 32bit build

* Wed Oct 2 2013 Orion Poplawski <orion@cora.nwra.com> - 4.2-2
- Use patch to fix up various libdir paths
- Modify configure to remove rpath

* Fri Sep 27 2013 Orion Poplawski <orion@cora.nwra.com> - 4.2-1
- Initial package
