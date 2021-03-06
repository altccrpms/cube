%global shortname cube
%global ver 4.3.4
%{?altcc_init}
# We can't build the frontend with the Intel C++ compiler without having Qt built with intel compiler
%{?altcc:%bcond_with frontend}
%{!?altcc:%bcond_without frontend}

Name:           %{shortname}%{?altcc_pkg_suffix}
Version:        4.3.4
Release:        4%{?dist}
Summary:        CUBE Uniform Behavioral Encoding generic presentation component

License:        BSD
URL:            http://www.scalasca.org/software/cube-4.x/download.html
Source0:        http://apps.fz-juelich.de/scalasca/releases/cube/4.3/dist/cube-%{version}.tar.gz
Source1:        %{shortname}.module.in

# disable check for new versions
Patch1:         cube-nocheck.patch
BuildRequires:  dbus-devel
BuildRequires:  qt4-devel
BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%{?altcc_reqmodules}
%{?altcc_provide}

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


%package        libs
Summary:        Libraries for %{name}
%{?altcc:%altcc_provide libs}

%description    libs
Libraries required by %{name}

%package        devel
Summary:        Development files for %{name}
# cube-devel may be required by profiling packages on compute nodes,
# so don't require cube, to avoid graphics
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%{?altcc:%altcc_provide devel}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch
%{?altcc:%altcc_provide doc}

%description    doc
The %{name}-doc package contains documentation for %{name}.


%prep
%setup -q -n %{shortname}-%{version}
%patch1 -p1


%build
for f in platform-frontend-user-provided platform-backend-user-provided platform-mpi-user-provided platform-shmem-user-provided
do
  cat > $f <<EOF
CC=$CC
CXX=$CXX
F90=$FC
EOF
done
%configure --disable-static \
  --disable-silent-rules \
  --with-platform=linux \
  --with-custom-compilers \
  --with-xerces-name=xerces-j2.jar
make %{?_smp_mflags}


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Install doc
cp -p AUTHORS ChangeLog COPYING README \
      %{buildroot}%{_defaultdocdir}/%{shortname}/

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

# Install desktop file
cat <<EOF >CUBE.desktop
[Desktop Entry]
Comment=Performance profile browser CUBE
Encoding=UTF-8
Exec=/usr/bin/cube
Icon=/usr/share/icons/Cube.xpm
InitialPreference=3
MimeType=application/cube;
Name=Cube (scalasca.org)
Terminal=false
Type=Application
Categories=Science;ComputerScience;DataVisualization;
EOF
desktop-file-install --dir=%{buildroot}%{_datadir}/applications CUBE.desktop

%{?altcc:%altcc_writemodule %SOURCE1}


%check
make check


%files
%{?altcc:%altcc_files -d %{_bindir} %{_libdir}}
%dir %{_defaultdocdir}/cube/
%{_defaultdocdir}/cube/AUTHORS
%{_defaultdocdir}/cube/ChangeLog
%{_defaultdocdir}/cube/COPYING
%{_defaultdocdir}/cube/README
%if %{with frontend}
%{_bindir}/cube
%endif
%{_bindir}/cube3to4
%{_bindir}/cube4to3
%{_bindir}/cube_calltree
%{_bindir}/cube_canonize
%{_bindir}/cube_clean
%{_bindir}/cube_cmp
%{_bindir}/cube_commoncalltree
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
%if %{with frontend}
%{_libdir}/libgraphwidgetcommon-plugin.so.7*
%{_libdir}/cube-plugins/
%endif
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/CUBE.desktop
%{_datadir}/icons/*
%{_datadir}/%{shortname}/

%files libs
%{?altcc:%altcc_files -m %{_libdir}}
%{_libdir}/lib%{shortname}*.so.7*

%files devel
%{?altcc:%altcc_files %{_includedir}}
%{_bindir}/cube-config
%{_bindir}/cube-config-backend
%{_bindir}/cube-config-frontend
%{_includedir}/%{shortname}*/
%{_libdir}/lib%{shortname}*.so
%if %{with frontend}
%{_libdir}/libgraphwidgetcommon-plugin.so
%endif
%{_defaultdocdir}/cube/example/

%files doc
%{?altcc:%altcc_files -d}
%{_defaultdocdir}/cube/


%changelog
* Tue May 10 2016 Dave Love <loveshack@fedoraproject.org> - 4.3.4-4
- Run ldconfig for both main as well as libs (for libgraphwidgetcommon-plugin)

* Mon May  9 2016 Dave Love <loveshack@fedoraproject.org> - 4.3.4-3
- Run ldconfig for libs package, not main

* Thu May  5 2016 Dave Love <loveshack@fedoraproject.org> - 4.3.4-2
- Have cube require matching cube-libs
- Don't do network check for new version

* Wed May  4 2016 Dave Love <loveshack@fedoraproject.org> - 4.3.4-1
- Update to 4.3.4
- Adjust for desktop and module files removed from distribution
- Remove xerces from configure
- Reinstate smp make

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.3-1
- Update to 4.3.3

* Sat Oct  3 2015 Dave Love <loveshack@fedoraproject.org> - 4.3.2-3
- Have devel package depend on cube-libs, not cube

* Fri Jun 26 2015 Dave Love <d.love@liverpool.ac.uk> - 4.3.2-2
- Make separate libs package (for scorep)
- Don't BR Java stuff

* Fri Jun 19 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.2-1
- Update to 4.3.2
- Drop java sub-package, moved to separate release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 5 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.1-1
- Update to 4.3.1

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.2.3-5
- Rebuilt for GCC 5 C++11 ABI change

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
