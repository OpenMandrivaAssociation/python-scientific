%define tarname	ScientificPython
%define name   	python-scientific
%define version 2.8
%define release %mkrel 1

Summary: 	Various Python modules for scientific computing
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source: 	%{tarname}-%{version}.tar.lzma
Patch0:		setup.py.patch
License: 	CeCILL-C
Group: 		Development/Python
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	python-numpy, openmpi
BuildRequires: 	netcdf-devel, python-numpy-devel, openmpi-devel, openmpi
Url: 		http://dirac.cnrs-orleans.fr/ScientificPython/
%py_requires -d

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
%__rm -rf %{buildroot}
%__python setup.py install --root=%{buildroot}

export PYTHONPATH=%{buildroot}%{py_sitedir}
export PYINCLUDE=`pwd`/Include
pushd Src/MPI
cat compile.py | sed 's/-I/-I$PYINCLUDE -I/' > compile-new.py
%__python compile-new.py

%__install -m 755 mpipython %{buildroot}%{_bindir}

cat <<EOF>impipython
#!/bin/bash
mpirun -np 2 `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)+'/Scientific/BSP/console.py'"` $*
EOF

popd

%clean
%__rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc LICENSE README README.MPI README.BSP Doc/CHANGELOG Doc/Reference Doc/BSP_Tutorial.pdf Examples/ Src/MPI/impipython
%{py_platsitedir}/Scientific/*
%{py_platsitedir}/*.egg-info
%defattr(755,root,root)
%{_bindir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/python%pyver/Scientific/


