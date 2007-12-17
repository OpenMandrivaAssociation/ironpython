%define name ironpython
%define oname IronPython
%define version 1.1
%define version2 2.0A5
%define release %mkrel 4
%define fversion %version-Src
%define fversion2 %version2-Src
%define ipydir %_prefix/lib/%name

Summary: Python for .NET/Mono
Name: %{name}
Version: %{version}
Release: %{release}
#gw these must be copied to files/
Source0: http://www.ironpython.info/downloads/%{oname}-%{fversion}.zip
Source1: http://www.ironpython.info/downloads/%{oname}-%{fversion2}.zip
Source2: http://www.crummy.com/software/BeautifulSoup/download/BeautifulSoup.py
#Source3: http://heanet.dl.sourceforge.net/sourceforge/cheetahtemplate/Cheetah-2.0rc8.tar.gz
Source4: http://www.dnspython.org/kits/1.5.0/dnspython-1.5.0.tar.gz
Source5: http://effbot.org/downloads/elementtree-1.2.6-20050316.tar.gz
Source6: http://www.lag.net/paramiko/download/paramiko-1.7.1.tar.gz
Source7: http://www.amk.ca/files/python/crypto/pycrypto-2.0.1.tar.gz
Source8: http://divmod.org/static/projects/pyflakes/pyflakes-0.2.1.tar.gz
#Source9: http://download.cherrypy.org/cherrypy/3.0.1/CherryPy-3.0.1.tar.gz
#Source10: http://heanet.dl.sourceforge.net/sourceforge/sqlalchemy/SQLAlchemy-0.3.10.tar.gz
Source10: http://heanet.dl.sourceforge.net/sourceforge/python-irclib/python-irclib-0.4.6.tar.gz
# https://fepy.svn.sourceforge.net/svnroot/fepy/IPCE/download.sh
Source50: https://fepy.svn.sourceforge.net/svnroot/fepy/IPCE/build.sh
Source51: http://fepy.sourceforge.net/license.html
#gw these are usually checked out by build.py
Source100: fepy-535.tar.bz2
Source101: lib-57729.tar.bz2
Source102: wsgiref-57729.tar.bz2
Source103: pybench-57719.tar.bz2
#gw disable svn update
Patch: build.sh-noupdate.patch
Patch1: build.sh-license.patch
License: Shared Source License for IronPython
Group: Development/Python
Url: http://www.codeplex.com/Wiki/View.aspx?ProjectName=IronPython
BuildArch: noarch
BuildRequires: mono-devel
BuildRequires: subversion
BuildRequires: nant
Requires: mono

%description
IronPython is the code name of the new implementation of the Python
programming language running on .NET. It supports an interactive
console with fully dynamic compilation. It is well integrated with the
rest of the .NET Framework and makes all .NET libraries easily
available to Python programmers, while maintaining full compatibility
with the Python language.

This distribution of IronPython is based on the work of FePy's
IronPython Community Edition, see http://fepy.sourceforge.net/ and read
License.html for additional license information.

%prep
%setup -q -T -c -a 100 -a 101 -a 102 -a 103
mkdir files
# %SOURCE3 %SOURCE9 %SOURCE10
cp %SOURCE1 %SOURCE0 %SOURCE2 %SOURCE4 %SOURCE5 %SOURCE6 %SOURCE7 \
 %SOURCE8  %SOURCE10 files
cp %SOURCE50 %SOURCE51 .
chmod +x build.sh
%patch
%patch1

%build
./build.sh

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %buildroot%ipydir
cp -r dist/*  %buildroot%ipydir
#gw some paths are wrong
find %buildroot%ipydir -type f | xargs perl -pi -e "s^#! */usr/.*bin/python^#!%_bindir/mono %ipydir/ipy.exe^"
rm -f %buildroot%ipydir/*.html
mkdir -p %buildroot%_bindir
cat > %buildroot%_bindir/ipy << EOF
#!/bin/sh
%_bindir/mono %ipydir/ipy/ipy.exe "\$@"
EOF
cat > %buildroot%_bindir/ipyw << EOF
#!/bin/sh
%_bindir/mono %ipydir/ipy/ipyw.exe "\$@"
EOF
cat > %buildroot%_bindir/ipy2 << EOF
#!/bin/sh
%_bindir/mono %ipydir/ipy2/ipy.exe "\$@"
EOF
cat > %buildroot%_bindir/ipyw2 << EOF
#!/bin/sh
%_bindir/mono %ipydir/ipy2/ipyw.exe "\$@"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc *.html
%attr(755,root,root) %_bindir/*
%dir %ipydir/
%ipydir/ipy
%ipydir/ipy2
%ipydir/Lib
%ipydir/pybench
%ipydir/pyflakes
