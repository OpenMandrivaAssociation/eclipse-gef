%define fedora          1
%define redhat          0
%if %{fedora}
%define gcj_support     1
%else
%define gcj_support     0
%endif
%define eclipse_name            eclipse
%define major                   3
%define minor                   2
%define majmin                  %{major}.%{minor}
%define micro                   1
%define eclipse_base            %{_datadir}/%{eclipse_name}
%define eclipse_lib_base        %{_libdir}/%{eclipse_name}

Summary:        Graphical Editor Framework (GEF) plugin for Eclipse
Name:           %{eclipse_name}-gef
Version:        %{majmin}.%{micro}
Release:        %mkrel 4.3
Epoch:          0
License:        EPL
Group:          Development/Java
URL:            http://www.eclipse.org/gef/
Requires:       eclipse-platform

# # Here's how to generate the source drop for GEF 3.2.1:
# #
# mkdir -p temp/home && cd temp
# touch home/.cvspass
# cvs -d :pserver:anonymous@dev.eclipse.org:/home/tools co \
#      -r R32_Maintenance org.eclipse.releng.gefbuilder
# pushd org.eclipse.releng.gefbuilder
# patch -p0 << _EOF_
# --- build.xml   14 Aug 2003 15:26:21 -0000      1.1
# +++ build.xml   29 Mar 2006 04:29:15 -0000
# @@ -21,4 +21,15 @@
#                 </ant>
#         </target>
#       
# +       <target name="fetch" depends="init">
# +               <ant antfile="build.xml" dir="\${pde.build.scripts}"
# +                               target="preBuild">
# +                       <property name="builder" value="\${basedir}/\${component}" />
# +               </ant>
# +               <ant antfile="build.xml" dir="\${pde.build.scripts}"
# +                               target="fetch">
# +                       <property name="builder" value="\${basedir}/\${component}" />
# +               </ant>
# +       </target>
# +
#  </project>
# _EOF_
# 
# # Fetch GEF and Draw2D themselves
# 
# java -cp /usr/share/eclipse/startup.jar \
#     -Duser.home=../../home \
#     org.eclipse.core.launcher.Main \
#     -application org.eclipse.ant.core.antRunner \
#     -buildfile build.xml \
#     -DbaseLocation=/usr/share/eclipse \
#     -Dpde.build.scripts=/usr/share/eclipse/plugins/org.eclipse.pde.build/scripts \
#     -Dcomponent=sdk \
#     -DbaseExists=true \
#     -DfetchTag=R32_Maintenance \
#     fetch
#
# # Fetch examples
#
# java -cp /usr/share/eclipse/startup.jar \
#     -Duser.home=../../home \
#     org.eclipse.core.launcher.Main \
#     -application org.eclipse.ant.core.antRunner \
#     -buildfile build.xml \
#     -DbaseLocation=/usr/share/eclipse \
#     -Dpde.build.scripts=/usr/share/eclipse/plugins/org.eclipse.pde.build/scripts \
#     -Dcomponent=examples \
#     -DbaseExists=true \
#     -DfetchTag=R32_Maintenance \
#     fetch
# 
# popd
# 
# tar jcf eclipse-gef-fetched-src-3.2.1.tar.bz2 org.eclipse.releng.gefbuilder

Source0:        %{name}-fetched-src-%{version}.tar.bz2

Patch0:         %{name}-dont-set-bootclasspath.patch
Patch1:         %{name}-no-bidi.patch
Patch2:         %{name}-no-get-bean-info.patch

BuildRequires:    eclipse-pde
%if %{gcj_support}
BuildRequires:    gcc-java >= 0:4.0.2
BuildRequires:    java-gcj-compat-devel >= 0:1.0.33
%else
BuildRequires:    java-devel >= 0:1.4.2
BuildArch:        noarch
%endif

Requires:       eclipse-platform >= 1:3.2.1

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%package        sdk
Summary:        Eclipse GEF SDK
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%package        examples
Summary:        Eclipse GEF examples
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       %{name}-sdk = %{epoch}:%{version}-%{release}

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
%patch1 -p1
%patch2 -p1

%build
# See comments in the script to understand this.
/bin/sh -x %{eclipse_base}/buildscripts/copy-platform SDK %{eclipse_base}
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
%{java} -cp %{eclipse_base}/startup.jar                \
    -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration \
    -Duser.home=$homedir                              \
    org.eclipse.core.launcher.Main                    \
    -application org.eclipse.ant.core.antRunner \
    -Dcomponent=sdk                             \
    -DjavacFailOnError=true                     \
    -DdontUnzip=true                            \
    -DbaseLocation=$SDK                         \
    -Dpde.build.scripts=$SDK/plugins/org.eclipse.pde.build/scripts \
    -DskipFetch=true                            \
    -DbaseExists=true

# build the examples
%{java} -cp %{eclipse_base}/startup.jar                \
    -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration \
    -Duser.home=$homedir                              \
    org.eclipse.core.launcher.Main                    \
    -application org.eclipse.ant.core.antRunner       \
    -Dcomponent=examples                        \
    -DjavacFailOnError=true                     \
    -DdontUnzip=true                            \
    -DbaseLocation=$SDK                         \
    -Dpde.build.scripts=$SDK/plugins/org.eclipse.pde.build/scripts \
    -DskipFetch=true                            \
    -DbaseExists=true

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
%post -p %{_bindir}/rebuild-gcj-db
%postun -p %{_bindir}/rebuild-gcj-db
%endif

%files
%defattr(-,root,root)
%{eclipse_base}/features/org.eclipse.gef_*
%{eclipse_base}/plugins/org.eclipse.draw2d_*
%{eclipse_base}/plugins/org.eclipse.gef_*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
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
%if %{gcj_support}
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.text_*
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.logic_*
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.flow_*
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.shapes_*
%endif


