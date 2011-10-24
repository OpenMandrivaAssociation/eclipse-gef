%global eclipse_base     %{_libdir}/eclipse
%global eclipse_dropin   %{_datadir}/eclipse/dropins

Name:      eclipse-gef
Version:   3.6.2
Release:   1
Summary:   Graphical Editing Framework (GEF) Eclipse plugin
Group:     System/Libraries
License:   EPL
URL:       http://www.eclipse.org/gef/

# source tarball and the script used to generate it from upstream's source control
# script usage:
# $ sh get-gef.sh
Source0:   gef-%{version}.tar.gz
Source1:   get-gef.sh

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:        noarch

BuildRequires:    java-devel
BuildRequires:    java-javadoc
BuildRequires:    jpackage-utils
BuildRequires:    eclipse-pde >= 0:3.6.0
Requires:         java
Requires:         jpackage-utils
Requires:         eclipse-platform >= 0:3.6.0

%description
The Graphical Editing Framework (GEF) allows developers to create a rich
graphical editor from an existing application model. GEF is completely
application neutral and provides the groundwork to build almost any
application, including but not limited to: activity diagrams, GUI builders,
class diagram editors, state machines, and even WYSIWYG text editors.

%package   sdk
Summary:   Eclipse GEF SDK
Group:     System/Libraries
Requires:  java-javadoc
Requires:  eclipse-pde >= 0:3.5.1
Requires:  %{name} = %{version}-%{release}

%description sdk
Documentation and source for the Eclipse Graphical Editing Framework (GEF).

%package   examples
Summary:   Eclipse GEF examples
Group:     System/Libraries
Requires:  %{name} = %{version}-%{release}

%description examples
Installable versions of the example projects from the SDK that demonstrates how
to use the Eclipse Graphical Editing Framework (GEF) plugin.

%prep
%setup -q -n gef-%{version}

#%patch0 -p0

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
# We build the gef and examples features seperately, rather than just
# building the "all" feature, because it makes the files section easier to
# maintain (i.e. we don't have to know when upstream adds a new plugin)

# Note: Use the tag in get-gef.sh as the context qualifier because it's
#       later than the tags of the individual plugins.
OPTIONS="-DforceContextQualifier=v20110225-1600"

# build gef features
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.gef -a "$OPTIONS"
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.zest -a "$OPTIONS"
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.gef.sdk \
  -a "$OPTIONS -DJAVADOC14_HOME=%{java_home}/bin"
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.zest.sdk \
  -a "$OPTIONS -DJAVADOC14_HOME=%{java_home}/bin"

# build examples features
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.gef.examples

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{eclipse_dropin}
unzip -q -n -d %{buildroot}%{eclipse_dropin}/gef          build/rpmBuild/org.eclipse.gef.zip
unzip -q -n -d %{buildroot}%{eclipse_dropin}/gef          build/rpmBuild/org.eclipse.zest.zip
unzip -q -n -d %{buildroot}%{eclipse_dropin}/gef-sdk      build/rpmBuild/org.eclipse.gef.sdk.zip
unzip -q -n -d %{buildroot}%{eclipse_dropin}/gef-sdk      build/rpmBuild/org.eclipse.zest.sdk.zip
unzip -q -n -d %{buildroot}%{eclipse_dropin}/gef-examples build/rpmBuild/org.eclipse.gef.examples.zip

# the non-sdk builds are a subset of the sdk builds, so delete duplicate features & plugins from the sdks
(cd %{buildroot}%{eclipse_dropin}/gef-sdk/eclipse/features && ls %{buildroot}%{eclipse_dropin}/gef/eclipse/features | xargs rm -rf)
(cd %{buildroot}%{eclipse_dropin}/gef-sdk/eclipse/plugins  && ls %{buildroot}%{eclipse_dropin}/gef/eclipse/plugins  | xargs rm -rf)

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{eclipse_dropin}/gef
%doc org.eclipse.gef-feature/rootfiles/*

%files sdk
%defattr(-,root,root,-)
%{eclipse_dropin}/gef-sdk
%doc org.eclipse.gef.sdk-feature/rootfiles/*

%files examples
%defattr(-,root,root,-)
%{eclipse_dropin}/gef-examples
%doc org.eclipse.gef.examples-feature/rootfiles/*

