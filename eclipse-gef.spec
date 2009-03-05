%define gcj_support     0
%define eclipse_base     %{_libdir}/eclipse
%define eclipse_dropin   %{_datadir}/eclipse/dropins/gef
%define install_loc         %{_datadir}/eclipse/dropins

Summary:        Graphical Editor Framework (GEF) plugin for Eclipse
Name:           eclipse-gef
Version:        3.4.2
Release:        %mkrel 0.1.0
License:        Eclipse Public License
Group:          Development/Java
URL:            http://www.eclipse.org/gef/

# Generate the source drop for GEF 3.3 using the enclosed script:
# sh ./fetch-gef.sh
Source0:        gef-%{version}.tar.gz

BuildRequires:    eclipse-pde >= 3.3
BuildRequires:    zip
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

Requires:       eclipse-platform >= 3.3

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
%setup -q -n gef-%{version}

rm -r org.eclipse.gef-feature/sourceTemplateFeature
rm -r org.eclipse.draw2d-feature/sourceTemplateFeature
rm -r org.eclipse.zest-feature/sourceTemplateFeature

# make sure upstream hasn't sneaked in any jars we don't know about
JARS=""
for j in `find -name "*.jar"`; do
  if [ ! -L $j ]; then
    JARS="$JARS $j"
  fi
done
if [ ! -z "$JARS" ]; then
   echo "These jars should be deleted and symlinked to system jars: $JARS"
   exit 1
fi

%build
# build all features
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.gef.all \
  -a "-DjavacTarget=1.6 -DjavacSource=1.6"

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{eclipse_dropin}
unzip -d %{buildroot}%{eclipse_dropin} build/rpmBuild/org.eclipse.gef.all.zip

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
%defattr(-,root,root,-)
%dir %{eclipse_dropin}
%doc %{eclipse_dropin}/eclipse/epl-v10.html
%doc %{eclipse_dropin}/eclipse/notice.html
%doc %{eclipse_dropin}/eclipse/readme
%{eclipse_dropin}/eclipse/content.xml
%{eclipse_dropin}/eclipse/features/org.eclipse.gef_*
%{eclipse_dropin}/eclipse/features/org.eclipse.draw2d_*
%{eclipse_dropin}/eclipse/features/org.eclipse.zest_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.gef_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.draw2d_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.zest.core_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.zest.layouts_*

%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/org.eclipse.gef_*
%{_libdir}/gcj/%{name}/org.eclipse.draw2d_*
%{_libdir}/gcj/%{name}/org.eclipse.zest.core_*
%{_libdir}/gcj/%{name}/org.eclipse.zest.layouts_*
%endif

%files sdk
%defattr(-,root,root,-)
%doc %{eclipse_dropin}/eclipse/epl-v10.html
%doc %{eclipse_dropin}/eclipse/notice.html
%doc %{eclipse_dropin}/eclipse/readme
%{eclipse_dropin}/eclipse/features/org.eclipse.gef.sdk_*
%{eclipse_dropin}/eclipse/features/org.eclipse.gef.source_*
%{eclipse_dropin}/eclipse/features/org.eclipse.draw2d.sdk_*
%{eclipse_dropin}/eclipse/features/org.eclipse.draw2d.source_*
%{eclipse_dropin}/eclipse/features/org.eclipse.zest.sdk_*
%{eclipse_dropin}/eclipse/features/org.eclipse.zest.source_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.gef.doc.isv_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.gef.source_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.gef.examples.ui.pde_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.draw2d.doc.isv_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.draw2d.source_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.zest.source_*

%if %{gcj_support}
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.ui.pde_*
%endif

%files examples
%defattr(-,root,root,-)
%doc %{eclipse_dropin}/eclipse/epl-v10.html
%doc %{eclipse_dropin}/eclipse/notice.html
%doc %{eclipse_dropin}/eclipse/readme
%{eclipse_dropin}/eclipse/features/org.eclipse.gef.all_*
%{eclipse_dropin}/eclipse/features/org.eclipse.gef.examples_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.gef.examples.flow_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.gef.examples.logic_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.gef.examples.shapes_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.gef.examples.source_*
%{eclipse_dropin}/eclipse/plugins/org.eclipse.gef.examples.text_*

%if %{gcj_support}
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.flow_*
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.logic_*
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.shapes_*
%{_libdir}/gcj/%{name}/org.eclipse.gef.examples.text_*
%endif
