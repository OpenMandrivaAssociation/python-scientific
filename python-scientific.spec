%define module	scientific
%define name   	python-%{module}
%define version 2.6.1

Summary: 	Various Python modules for scientific computing
Name: 		%{name}
Version: 	%{version}
Release: 	%mkrel 4
Source: 	ScientificPython-%{version}.tar.bz2
License: 	BSD-like
Group: 		Development/Python
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	python-numeric
BuildRequires: 	python python-devel
BuildRequires: 	netcdf-devel python-numeric-devel
Url: 		http://dirac.cnrs-orleans.fr/ScientificPython/

%description
ScientificPython is a collection of Python modules that are useful
for scientific computing. In this collection you will find modules
that cover basic geometry (vectors, tensors, transformations, vector
and tensor fields), quaternions, automatic derivatives, (linear)
interpolation, polynomials, elementary statistics, nonlinear
least-squares fits, unit calculations, Fortran-compatible text
formatting, 3D visualization via VRML, and two Tk widgets for simple
line plots and 3D wireframe models.

%package devel
Summary:	Various Python modules for scientific computing, header files
Group: 		Development/Python
Requires: 	python-devel %{name} = %{version}

%description devel
This package contain headers file associated with the %{name} package.

%prep
%setup -q -n ScientificPython-%{version}

%build
%__python setup.py build

%install
%__python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README README.MPI README.BSPlib Doc/Reference Doc/BSP_Tutorial.pdf
%{py_platsitedir}/Scientific/*
%{py_platsitedir}/*.egg-info
%defattr(755,root,root)
%{_bindir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/python%pyver/Scientific/


