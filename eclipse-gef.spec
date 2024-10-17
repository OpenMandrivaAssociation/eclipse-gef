%{?_javapackages_macros:%_javapackages_macros}
%global eclipse_dropin   %{_datadir}/eclipse/dropins

# Release has not been tagged, but this commit comprised the release
%global git_version f4eada958b82a6a8c4edff8e0f12cdad47b79c28

Name:      eclipse-gef
Version:   3.9.101
Release:   4.2
Summary:   Graphical Editing Framework (GEF) Eclipse plug-in
Group:     Development/Java
License:   EPL
URL:       https://www.eclipse.org/gef/

Source0:   http://git.eclipse.org/c/gef/org.eclipse.gef.git/snapshot/org.eclipse.gef-%{git_version}.tar.bz2
# Use this script to generate a much smaller version of the above source tarball
#Source1:   get-gef.sh

BuildArch:        noarch

BuildRequires:    tycho
BuildRequires:    eclipse-pde >= 1:4.4.0
BuildRequires:    eclipse-license
BuildRequires:    ant-contrib
Requires:         eclipse-platform >= 1:4.4.0

%description
The Graphical Editing Framework (GEF) allows developers to create a rich
graphical editor from an existing application model. GEF is completely
application neutral and provides the groundwork to build almost any
application, including but not limited to: activity diagrams, GUI builders,
class diagram editors, state machines, and even WYSIWYG text editors.

%package   sdk
Summary:   Eclipse GEF SDK
Group:     Development/Java 
Requires:  eclipse-pde >= 1:4.4.0
Requires:  %{name} = %{version}-%{release}

%description sdk
Documentation and source for the Eclipse Graphical Editing Framework (GEF).

%package   examples
Summary:   Development/Java
Group:     System Environment/Libraries
Requires:  %{name} = %{version}-%{release}

%description examples
Installable versions of the example projects from the SDK that demonstrates how
to use the Eclipse Graphical Editing Framework (GEF) plug-in.

%prep
%setup -q -n org.eclipse.gef-%{git_version}

find -name *.jar -exec rm -rf {} \;
find -name *.class -exec rm -rf {} \;

%mvn_package "org.eclipse.gef:" __noinstall
%mvn_package "org.eclipse.gef.features:org.eclipse.gef.all" __noinstall
%mvn_package "org.eclipse.gef.features:org.eclipse.gef.examples{,.source}" examples
%mvn_package ":org.eclipse.gef.examples.{logic,flow,text,shapes}:jar:sources:" examples
%mvn_package "::jar:sources:" sdk
%mvn_package ":*.{sdk,source,test,tests,capabilities}" sdk
%mvn_package "org.eclipse.draw2d.{features,plugins}:org.eclipse.draw2d" core
%mvn_package "org.eclipse.gef.{features,plugins}:org.eclipse.gef" core
%mvn_package "org.eclipse.zest.features:org.eclipse.zest" core
%mvn_package "org.eclipse.zest.plugins:org.eclipse.zest.{core,layouts}" core

%build
%mvn_build -j -f -- -f org.eclipse.gef.releng/pom.xml -P !LUNA_4_4.target

%install
%mvn_install

%files -f .mfiles -f .mfiles-core
%{_datadir}/maven-metadata/eclipse-gef.xml
%doc org.eclipse.gef-feature/epl-v10.html

%files sdk -f .mfiles-sdk
%doc org.eclipse.gef.sdk-feature/epl-v10.html

%files examples -f .mfiles-examples
%doc org.eclipse.gef.examples-feature/epl-v10.html

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.101-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb  6 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.9.101-3
- Rebuild to generate missing OSGi auto-requires

* Wed Jan 14 2015 Mat Booth <mat.booth@redhat.com> - 3.9.101-2
- Migrate to mvn_build/mvn_install

* Tue Sep 30 2014 Mat Booth <mat.booth@redhat.com> - 3.9.101-1
- Update to 3.9.101

* Mon Jun 30 2014 Mat Booth <mat.booth@redhat.com> - 3.9.100-1.gitb63ec56
- Update to latest upstream release
- Add a script to make smaller source tarballs
- Add BR on eclipse-license

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.1-0.4.gitb9f2e9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 3.9.1-0.3.gitb9f2e9
- Use Requires: java-headless rebuild (#1067528)

* Mon Oct 28 2013 Krzysztof Daniel <kdaniel@redhat.com> 3.9.1-0.2.gitb9f2e9
- Deploy missing bundles and features.

* Tue Oct 1 2013 Krzysztof Daniel <kdaniel@redhat.com> 3.9.1-0.1.gitb9f2e9
- Update to Kepler SR1.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.0-2.git22becd5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Krzysztof Daniel <kdaniel@redhat.com> 3.9.0-1.git22becd5
- Kepler release.

* Tue Apr 9 2013 Alexander Kurtakov <akurtako@redhat.com> 3.9.0-0.2.gitbd7178d
- New snapshot containing upstream fix for icu4j 50.x.

* Wed Apr 3 2013 Alexander Kurtakov <akurtako@redhat.com> 3.9.0-0.1.gitdbf4cef
- Update to 3.9.0 snapshot (aka Kepler).
- SCL-ize.

* Thu Feb 21 2013 Alexander Kurtakov <akurtako@redhat.com> 3.8.1-7
- Adapt to the icu4j version jump.
- Skip tests for now.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Krzysztof Daniel <kdaniel@redhat.com> 3.8.1-5
- Ignore Tycho version check.

* Thu Oct 4 2012 Krzysztof Daniel <kdaniel@redhat.com> 3.8.1-4
- Configure only one Tycho version.

* Thu Oct 4 2012 Krzysztof Daniel <kdaniel@redhat.com> 3.8.1-3
- Properly unpack features.

* Wed Oct 3 2012 Krzysztof Daniel <kdaniel@redhat.com> 3.8.1-2
- Fix installation location

* Tue Oct 2 2012 Krzysztof Daniel <kdaniel@redhat.com> 3.8.1-1
- Update to  Juno SR1.
- Build reflects upstream build now.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 3.8.0-1
- Update to upstream Juno release. 

* Mon Apr 16 2012 Krzysztof Daniel <kdaniel@redhat.com> 3.8.0-0.3.20120402
- Generate documentation contents & reference API.

* Fri Apr 13 2012 Krzysztof Daniel <kdaniel@redhat.com> 3.8.0-0.2.20120402
- Update to Eclipse 4.2
- Fix documentation build

* Mon Apr 2 2012 Krzysztof Daniel <kdaniel@redhat.com> 3.8.0-0.1.20120402
- Update to 3.8.0 post M6 build.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 11 2011 Andrew Overholt <overholt@redhat.com> 3.7.0-1
- Update to 3.7.0.

* Fri Mar 18 2011 Mat Booth <fedora@matbooth.co.uk> 3.6.2-1
- Update to 3.6.2.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 7 2010 Chris Aniszczyk <zx@redhat.com> 3.6.1-1
- Update to 3.6.1.

* Fri Jul 9 2010 Alexander Kurtakov <akurtako@redhat.com> 3.6.0-1
- Update to 3.6.0.

* Sun Feb 28 2010 Mat Booth <fedora@matbooth.co.uk> 3.5.2-1
- Update to 3.5.2 upstream version.
- Now requires Eclipse 3.5.1.

* Sun Nov 8 2009 Mat Booth <fedora@matbooth.co.uk> 3.5.1-2
- Update context qualifier to be later than the tags of the individual plugins.

* Tue Oct 27 2009 Alexander Kurtakov <akurtako@redhat.com> 3.5.1-1
- Update to 3.5.1 upstream version.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Mat Booth <fedora@matbooth.co.uk> 3.5.0-2
- SDK requires PDE for example plug-in projects.

* Wed Jul 01 2009 Mat Booth <fedora@matbooth.co.uk> 3.5.0-1
- Update to 3.5.0 final release (Galileo).
- Build the features seperately to allow for a saner %%files section.
- Use %%global instead of %%define.

* Wed May 27 2009 Alexander Kurtakov <akurtako@redhat.com> 3.5.0-0.2.RC2
- Update to 3.5.0 RC2.

* Sat Apr 18 2009 Mat Booth <fedora@matbooth.co.uk> 3.5.0-0.1.M6
- Update to Milestone 6 release of 3.5.0.
- Require Eclipse 3.5.0.

* Tue Apr 7 2009 Alexander Kurtakov <akurtako@redhat.com> 3.4.2-3
- Fix directory ownership.
- Drop gcj support.

* Mon Mar 23 2009 Alexander Kurtakov <akurtako@redhat.com> 3.4.2-2
- Rebuild to not ship p2 context.xml.
- Remove context.xml from %%files section.

* Sat Feb 28 2009 Mat Booth <fedora@matbooth.co.uk> 3.4.2-1
- Update for Ganymede SR2.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Mat Booth <fedora@matbooth.co.uk> 3.4.1-2
- Rebuild GCJ DB during post and postun in sub-packages.

* Thu Nov 20 2008 Mat Booth <fedora@matbooth.co.uk> 3.4.1-1
- New maintainer.
- Updated to verion 3.4.1.
- Update package for new Eclipse plugin guidelines.
- Own the gcj/%%{name} directory.
- The 'examples.ui.pde' plugin is actually part of the SDK feature.

* Thu Jul 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.3.0-3
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.3.0-2
- Autorebuild for GCC 4.3

* Mon Aug 27 2007 Andrew Overholt <overholt@redhat.com> 3.3.0-1
- 3.3.

* Thu Jun 14 2007 Andrew Overholt <overholt@redhat.com> 3.2.1-5
- Add EPEL5 patches from Rob Myers.

* Tue Jan 30 2007 Andrew Overholt <overholt@redhat.com> 3.2.1-4
- Use copy-platform in %%{eclipse_base}.

* Mon Nov 06 2006 Andrew Overholt <overholt@redhat.com> 3.2.1-3
- Use copy-platform in %%{_libdir}.
- Use binary launcher rather than startup.jar to guard against future
  osgi.sharedConfiguration.area changes.

* Thu Oct 19 2006 Andrew Overholt <overholt@redhat.com> 3.2.1-2
- Fix buildroot (don't know how the wrong one slipped in).

* Thu Oct 19 2006 Andrew Overholt <overholt@redhat.com> 3.2.1-1
- 3.2.1.

* Tue Aug 29 2006 Andrew Overholt <overholt@redhat.com> 3.2.0-2
- First release for Fedora.

* Tue Aug 22 2006 Andrew Overholt <overholt@redhat.com> 3.2.0-1jpp_2rh
- -devel -> -sdk to match upstream..

* Tue Jul 25 2006 Andrew Overholt <overholt@redhat.com> 3.2.0-1jpp_1rh
- 3.2.0.

* Tue May 02 2006 Ben Konrath <bkonrath@redhat.com> 3.1.1-1jpp_2rh
- Remove -debug from compile line.
- Add expamples package.

* Mon Apr 3 2006 Ben Konrath <bkonrath@redhat.com> 3.1.1-1jpp_1rh
- Add devel package. 
- Update sources to 3.1.1.
- Some general spec file cleanup.
- Add patch to stop the gefbuilder plugin from setting bootclasspath.
- Change copyright to license.
- Add instructions for generating source drop.

* Tue Sep 6 2005 Aaron Luchko  <aluchko@redhat.com> 3.1.0-1
- change to match eclipse-changelog.spec and fixed typos

* Thu Aug 4 2005 Aaron Luchko  <aluchko@redhat.com>
- Updated to 3.1.0
- added createTarball.sh, gefSource.sh, and build.xml.patch
- added native build
- changes to use eclipsebuilder
- fixes from Matthias Saou

* Mon Jun 27 2005 Aaron Luchko <aluchko@redhat.com> 3.0.1-8
- Added x86_64

* Mon May 2 2005 Ben Konrath <bkonrath@redhat.com> 3.0.1-7
- Build against Eclipse 3.0.2.

* Thu Mar 31 2005 Phil Muldoon <pmuldoon@redhat.com> 3.0.1-6
- Migrate RHEL-3 sources to RHEL-4

* Mon Nov 1 2004 Phil Muldoon  <pmuldoon@redhat.com> 3.0.1-5
- Stopped ant trying to replace about.mappings

* Mon Nov 1 2004 Phil Muldoon  <pmuldoon@redhat.com> 3.0.1-4
- Changed tar name to new tar

* Mon Nov 1 2004 Phil Muldoon  <pmuldoon@redhat.com> 3.0.1-3
- Touch build scripts to point to 3.0.1

* Mon Nov 1 2004 Phil Muldoon  <pmuldoon@redhat.com> 3.0.1-2
- Explicitly set -DJAVADOC14_HOME=%%{java_home}/bin to build javadocs

* Sun Oct 31 2004 Phil Muldoon <pmuldoon@redhat.com> 3.0.1-1
- Initial Import

