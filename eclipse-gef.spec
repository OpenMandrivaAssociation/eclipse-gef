%define gcj_support     1
%define eclipse_base            %{_datadir}/eclipse
%define eclipse_lib_base        %{_libdir}/eclipse

Summary:        Graphical Editor Framework (GEF) plugin for Eclipse
Name:           eclipse-gef
Version:        3.3.0
Release:        %mkrel 0.1.1
License:        Eclipse Public License
Group:          Development/Java
URL:            http://www.eclipse.org/gef/

# Generate the source drop for GEF 3.3 using the enclosed script:
# sh ./fetch-gef.sh
Source0:        %{name}-fetched-src-%{version}.tar.bz2

Patch0:         %{name}-dont-set-bootclasspath.patch

BuildRequires:    eclipse-pde >= 1:3.3
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel >= 1.0.33
%else
BuildRequires:    java-devel >= 1.4.2
%endif

%if %{gcj_support}
ExclusiveArch:    %{ix86} x86_64 ppc ia64
%else
BuildArch:        noarch
%endif

Requires:       eclipse-platform >= 1:3.3

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%package        sdk
Summary:        Eclipse GEF SDK
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

%package        examples
Summary:        Eclipse GEF examples
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-sdk = %{version}-%{release}

%description
The eclipse-gef package contains Eclipse features and plugins that comprise
the Graphical Editor Framework for Eclipse.

%description    sdk
Source and documentation for Eclipse GEF for use within Eclipse.

%description    examples
Example source code that demonstrates how to use Eclipse GEF.

%prep
%setup -q -c

# https://bugs.eclipse.org/bugs/show_bug.cgi?id=134567
pushd org.eclipse.releng.gefbuilder
%patch0 -p0
popd

%build
# See comments in the script to understand this.
%if 0%{?rhel} == 5
/bin/sh -x %{eclipse_lib_base}/buildscripts/copy-platform SDK %{eclipse_base}
%else
/bin/sh -x %{eclipse_base}/buildscripts/copy-platform SDK %{eclipse_base}
%endif
SDK=$(cd SDK > /dev/null && pwd)

mkdir home
homedir=$(cd home > /dev/null && pwd)

cd org.eclipse.releng.gefbuilder

# some notes about what we're doing here:
#
# -Duser.home=$homedir: override java.home in the vm so that eclipse only adds files in the buildroot 
# -Dcomponent=sdk: the component of GEF we want to build 
# -DjavacFailOnError=true: fail if there is an error 
# -DdontUnzip=true: don't unzip the result, we will do it manually
# -DbaseLocation=$SDK: $SDK is a mirror of the system SDK dir that is writable by the process 
#                      running the build. This let's the build "see" the jars and have a place to 
#                      put the plugins that have just been built
# -DskipFetch=true: don't fetch the sources 
# -DbaseExists=true: don't download the SDK, we want to use the one in $SDK
eclipse \
    -nosplash \
    -application org.eclipse.ant.core.antRunner \
    -Dcomponent=sdk                             \
    -DjavacFailOnError=true                     \
    -DdontUnzip=true                            \
    -DbaseLocation=$SDK                         \
    -Dpde.build.scripts=$SDK/plugins/org.eclipse.pde.build/scripts \
    -DskipFetch=true                            \
    -DbaseExists=true                           \
    -DmapsLocal=true

# build the examples
eclipse \
    -nosplash \
    -application org.eclipse.ant.core.antRunner \
    -Dcomponent=examples                        \
    -DjavacFailOnError=true                     \
    -DdontUnzip=true                            \
    -DbaseLocation=$SDK                         \
    -Dpde.build.scripts=$SDK/plugins/org.eclipse.pde.build/scripts \
    -DskipFetch=true                            \
    -DbaseExists=true                           \
    -DmapsLocal=true

%install
rm -rf ${RPM_BUILD_ROOT}
install -d -m755 ${RPM_BUILD_ROOT}/%{eclipse_base}

for file in $(pwd)/org.eclipse.releng.gefbuilder/src/eclipse/I*/*.zip; do
  case $file in
    *eclipse*)
      # The ".." is needed since the zip files contain "eclipse/foo".
      (cd $RPM_BUILD_ROOT/%{eclipse_base}/.. && unzip -qq -o $file)
      ;;
  esac
done

# These are already included in the Eclipse SDK but the packaging guidelines
# would like them in a directory owned by this package
mv $RPM_BUILD_ROOT/%{eclipse_base}/epl-v10.html \
  $RPM_BUILD_ROOT/%{eclipse_base}/features/org.eclipse.gef_*
mv $RPM_BUILD_ROOT/%{eclipse_base}/notice.html \
  $RPM_BUILD_ROOT/%{eclipse_base}/features/org.eclipse.gef_*

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean 
rm -rf ${RPM_BUILD_ROOT}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root)
%{eclipse_base}/features/org.eclipse.gef_*
%{eclipse_base}/plugins/org.eclipse.draw2d_*
%{eclipse_base}/plugins/org.eclipse.gef_*
%if %{gcj_support}
%{_libdir}/gcj/%{name}/org.eclipse.draw2d_*
%{_libdir}/gcj/%{name}/org.eclipse.gef_*
%endif
%doc %{eclipse_base}/readme/*
%doc %{eclipse_base}/features/org.eclipse.gef_*/notice.html
%doc %{eclipse_base}/features/org.eclipse.gef_*/epl-v10.html

%files sdk
%defattr(-,root,root)
%{eclipse_base}/features/org.eclipse.gef.sdk_*
%{eclipse_base}/features/org.eclipse.gef.source_*
%{eclipse_base}/plugins/org.eclipse.draw2d.doc.isv_*
%{eclipse_base}/plugins/org.eclipse.gef.doc.isv_*
%{eclipse_base}/plugins/org.eclipse.gef.source_*

%files examples
%defattr(-,root,root)
%{eclipse_base}/features/org.eclipse.gef.examples_*
%{eclipse_base}/plugins/org.eclipse.gef.examples.source_*
%{eclipse_base}/plugins/org.eclipse.gef.examples.text_*
%{eclipse_base}/plugins/org.eclipse.gef.examples.logic_*
%{eclipse_base}/plugins/org.eclipse.gef.examples.flow_*
%{eclipse_base}/plugins/org.eclipse.gef.examples.shapes_*
%{eclipse_base}/plugins/org.eclipse.gef.examples.ui.pde_*
%if %{gcj_support}
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.text_*
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.logic_*
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.flow_*
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.shapes_*
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.ui.pde_*
%endif
