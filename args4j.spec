%{?scl:%scl_package args4j}
%{!?scl:%global pkg_name %{name}}

%{?java_common_find_provides_and_requires}

Name:           %{?scl_prefix}args4j
Version:        2.0.30
Release:        3%{?dist}
Summary:        Java command line arguments parser
License:        MIT
URL:            http://args4j.kohsuke.org/
Source0:        https://github.com/kohsuke/%{pkg_name}/archive/%{pkg_name}-site-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix_java_common}mvn(com.sun:tools)
BuildRequires:  %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-site-plugin)

%description
args4j is a small Java class library that makes it easy
to parse command line options/arguments in your CUI application.
- It makes the command line parsing very easy by using annotations
- You can generate the usage screen very easily
- You can generate HTML/XML that lists all options for your documentation
- Fully supports localization
- It is designed to parse javac like options (as opposed to GNU-style
  where ls -lR is considered to have two options l and R)

%package tools
Summary:        Development-time tool for generating additional artifacits

%description tools
This package contains args4j development-time tool for generating
additional artifacits.

%package parent
Summary:        args4j parent POM

%description parent
This package contains parent POM for args4j project.

%package javadoc
Summary:        API documentation for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{pkg_name}-site-%{version}

# removing classpath addition
sed -i 's/<addClasspath>true/<addClasspath>false/g' %{pkg_name}-tools/pom.xml

# fix ant group id
sed -i 's/<groupId>ant/<groupId>org.apache.ant/g' %{pkg_name}-tools/pom.xml

# removing bundled stuff
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# XMvn cannot generate requires on dependecies with scope "system"
%pom_xpath_remove "pom:profile[pom:id[text()='jdk-tools-jar']]" %{pkg_name}-tools
%pom_add_dep com.sun:tools %{pkg_name}-tools

# we don't need these now
%pom_disable_module args4j-maven-plugin
%pom_disable_module args4j-maven-plugin-example

# Avoid koshuke-pom and mockito
%pom_remove_dep org.mockito:mockito-all %{pkg_name}-tools
%pom_remove_parent

# put args4j-tools and parent POM to separate subpackages
%mvn_package :args4j-tools::{}: %{pkg_name}-tools
%mvn_package :args4j-site::{}: %{pkg_name}-parent

# install also compat symlinks
%mvn_file ":{*}" %{pkg_name}/@1 @1
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -- -Dmaven.test.skip=true
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%doc %{pkg_name}/LICENSE.txt

%files tools -f .mfiles-%{pkg_name}-tools

%files parent -f .mfiles-%{pkg_name}-parent
%doc %{pkg_name}/LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc %{pkg_name}/LICENSE.txt

%changelog
* Thu Jan 15 2015 Roland Grunberg <rgrunber@redhat.com> - 2.0.30-3
- SCL-ize.

* Mon Sep 22 2014 Michal Srb <msrb@redhat.com> - 2.0.30-2
- Move args4j-tools and parent POM into subpackages (Resolves: #1144991)

* Mon Sep 01 2014 Michal Srb <msrb@redhat.com> - 2.0.30-1
- Update to upstream version 2.0.30

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Michal Srb <msrb@redhat.com> - 2.0.28-1
- Update to upstream version 2.0.28

* Wed May 07 2014 Michal Srb <msrb@redhat.com> - 2.0.27-1
- Update to upstream version 2.0.27

* Tue May 06 2014 Michal Srb <msrb@redhat.com> - 2.0.26-4
- Port to JSR-269

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0.26-3
- Use Requires: java-headless rebuild (#1067528)

* Thu Feb 20 2014 Michal Srb <msrb@redhat.com> - 2.0.26-2
- Adapt to current guidelines

* Thu Feb 20 2014 Michal Srb <msrb@redhat.com> - 2.0.26-1
- Update to latest upstream 2.0.26

* Sat Aug 10 2013 Mat Booth <fedora@matbooth.co.uk> - 2.0.25-1
- Update to latest upstream, fixes #981339

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 27 2013 Mat Booth <fedora@matbooth.co.uk> - 2.0.23-1
- Update to latest upstream, fixes #808703
- Also drop unneeded patches

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.0.16-10
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Dec 13 2012 Roland Grunberg <rgrunber@redhat.com> - 2.0.16-9
- Update to conform with latest Java packaging guidelines.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Ville Skyttä <ville.skytta@iki.fi> - 2.0.16-7
- Apply upstream source encoding patch to fix build with java 1.7.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 13 2011 Jaromir Capik <jcapik@redhat.com> - 2.0.16-4
- OSGi metadata generated

* Mon May 30 2011 Jaromir Capik <jcapik@redhat.com> - 2.0.16-3
- Removal of bundled stuff in args4j/lib

* Wed May 25 2011 Jaromir Capik <jcapik@redhat.com> - 2.0.16-2
- Removal of unused ant dependency

* Tue May 24 2011 Jaromir Capik <jcapik@redhat.com> - 2.0.16-1
- Initial version of the package
