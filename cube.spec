Name:           cube
Version:        4.2.3
Release:        4%{?dist}
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
cp -p AUTHORS ChangeLog COPYING README \
      %{buildroot}%{_defaultdocdir}/%{name}/

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/CUBE.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright (c) 2014 Forschungszentrum Juelich GmbH, Germany -->

<application>
 <id type="desktop">CUBE.desktop</id>
 <metadata_license>CC0-1.0</metadata_license>
 <project_license>BSD-3-Clause</project_license>
 <name>Cube</name>
 <summary>A presentation component suitable for displaying
performance data for parallel programs</summary>
 <description>
  <p>
    "Cube" (CUBE Uniform Behavioral Encoding) is a presentation
    component suitable for displaying a wide variety of performance
    data for parallel programs including MPI and OpenMP applications.
  </p>
  <p>
    Program performance is represented in a multi-dimensional space including various program and
    system resources. The tool allows the interactive exploration of this
    space in a scalable fashion and browsing the different kinds of
    performance behavior with ease.  All metrics are uniformly accommodated in the 
    same display and thus provide the ability to easily compare the effects of 
    different kinds of program behavior.
  </p>
  <p>
    "Cube" also includes a library to
    read and write performance data as well as operators to compare,
    integrate, and summarize data from different experiments. 
  </p>
  <p>
    The Cube 4.x release series uses an incompatible API and
    file format compared to previous versions, however,
    existing files in CUBE3 format can still be processed
    for backwards-compatibility.    
  </p>
 </description>
 <screenshots>
  <screenshot type="default" width="1152" height="648">http://apps.fz-juelich.de/scalasca/releases/cube/screenshots/topo1.png</screenshot>
  <screenshot width="1152" height="648">http://apps.fz-juelich.de/scalasca/releases/cube/screenshots/topo2.png</screenshot>
  <screenshot width="1152" height="648">http://apps.fz-juelich.de/scalasca/releases/cube/screenshots/box.png</screenshot>
  <screenshot width="1152" height="648">http://apps.fz-juelich.de/scalasca/releases/cube/screenshots/flat.png</screenshot>
  <screenshot width="1152" height="648">http://apps.fz-juelich.de/scalasca/releases/cube/screenshots/palette.png</screenshot>
 </screenshots>
 <url type="homepage">http://www.scalasca.org/software/cube-4.x/download.html</url>
 <updatecontact>scalasca_at_fz-juelich.de</updatecontact>
</application>
EOF

# Strip rpath
chrpath -d -k %{buildroot}%{_bindir}/* || :

# Install desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications CUBE.desktop

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
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/CUBE.desktop
%{_datadir}/icons/Cube.xpm
%{_datadir}/%{name}/

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
* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 4.2.3-4
- Add an AppData file for the software center

* Tue Mar  3 2015 Peter Robinson <pbrobinson@fedoraproject.org> 4.2.3-3
- rebuild (gcc5)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Orion Poplawski <orion@cora.nwra.com> - 4.2.3-1
- Update to 4.2.3

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
