%define tarname	ScientificPython

Summary: 	Various Python modules for scientific computing
Name: 		python-scientific
Version: 	2.8
Release: 	6
Source: 	%{tarname}-%{version}.tar.lzma
Patch0:		setup.py.patch
License: 	CeCILL-C
Group: 		Development/Python
Requires:	python-numpy, openmpi
BuildRequires: 	netcdf-devel
BuildRequires: 	python-numpy-devel
BuildRequires: 	openmpi-devel
BuildRequires: 	openmpi
BuildRequires:	python-devel
BuildRequires: 	pkgconfig(lapack)
Url: 		http://dirac.cnrs-orleans.fr/ScientificPython/

%description
ScientificPython is a collection of Python modules that are useful for
scientific computing. In this collection you will find modules that
cover basic geometry (vectors, tensors, transformations, vector and
tensor fields), quaternions, automatic derivatives, (linear)
interpolation, polynomials, elementary statistics, nonlinear
least-squares fits, unit calculations, Fortran-compatible text
formatting, 3D visualization via VRML, and two Tk widgets for simple
line plots and 3D wireframe models. There are also interfaces to the
netCDF library (portable structured binary files), to MPI (Message
Passing Interface, message-based parallel programming), and to BSPlib
(Bulk Synchronous Parallel programming).

%package devel
Summary:	Various Python modules for scientific computing, header files
Group: 		Development/Python
Requires: 	python-devel %{name} = %{version}

%description devel
This package contain headers file associated with the %{name} package.

%prep
%setup -q -n %{tarname}-%{version}
%patch0 -p0

%build
%__python setup.py build

%install
%__python setup.py install --root=%{buildroot}

export PYTHONPATH=%{buildroot}%{py_platsitedir}
export PYINCLUDE=`pwd`/Include
pushd Src/MPI
%ifarch x86_64
sed -i 's/lib\/python/lib64\/python/' compile.py
%endif
cat compile.py | sed 's/-I/-I$PYINCLUDE -I/' > compile-new.py
%__python compile-new.py

%__install -m 755 mpipython %{buildroot}%{_bindir}

cat <<EOF>impipython
#!/bin/bash
mpirun -np 2 `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)+'/Scientific/BSP/console.py'"` $*
EOF

popd

%files
%doc LICENSE README README.MPI README.BSP Doc/CHANGELOG Doc/Reference Doc/BSP_Tutorial.pdf Examples/ Src/MPI/impipython
%{py_platsitedir}/Scientific/*
%{py_platsitedir}/*.egg-info
%defattr(755,root,root)
%{_bindir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/python%{py_ver}/Scientific/




%changelog
* Sat Nov 06 2010 Funda Wang <fwang@mandriva.org> 2.8-5mdv2011.0
+ Revision: 593993
- rebuild for py2.7

* Thu Feb 18 2010 Emmanuel Andry <eandry@mandriva.org> 2.8-4mdv2010.1
+ Revision: 507529
- rebuild for new netcdf

* Wed Aug 12 2009 Funda Wang <fwang@mandriva.org> 2.8-3mdv2010.0
+ Revision: 415365
- rebuild for new libtorque

* Thu Mar 19 2009 Lev Givon <lev@mandriva.org> 2.8-2mdv2009.1
+ Revision: 358154
- Fix bug 48269.

* Wed Mar 18 2009 Lev Givon <lev@mandriva.org> 2.8-1mdv2009.1
+ Revision: 357437
- Update to 2.8.

* Fri Jan 02 2009 Funda Wang <fwang@mandriva.org> 2.6.1-4mdv2009.1
+ Revision: 323326
- fix file list

* Fri Aug 01 2008 Thierry Vignaud <tv@mandriva.org> 2.6.1-4mdv2009.0
+ Revision: 259777
- rebuild

* Fri Jul 25 2008 Thierry Vignaud <tv@mandriva.org> 2.6.1-3mdv2009.0
+ Revision: 247631
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 2.6.1-1mdv2008.1
+ Revision: 136460
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Lev Givon <lev@mandriva.org>
    - Update to 2.6.1.


* Tue Feb 20 2007 Lev Givon <lev@mandriva.org> 2.6-1mdv2007.0
+ Revision: 123082
- Update to latest stable release 2.6.
  Add python-numeric install dependency.

* Tue Dec 05 2006 Nicolas LÃ©cureuil <neoclust@mandriva.org> 2.4.9-6mdv2007.1
+ Revision: 90634
- Rebuild against new Python
- import python-scientific-2.4.9-5mdk

* Wed Dec 21 2005 Michael Scherer <misc@mandriva.org> 2.4.9-5mdk
- Fix BuildRequires
- fix rpmbuildupdatability

* Tue Dec 20 2005 Michael Scherer <misc@mandriva.org> 2.4.9-4mdk
- fix BuildRequires

* Tue Jun 21 2005 Lehmann Gaëtan <gaetan.lehmann@jouy.inra.fr> 2.4.9-3mdk
- buildrequires netcdf-devel
- use mkrel
- fix some lint

* Thu Feb 03 2005 Michael Scherer <misc@mandrake.org> 2.4.9-2mdk
- add BuildRequires

* Mon Nov 29 2004 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 2.4.9-1mdk
- initial contrib release.

