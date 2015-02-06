%define tarname ScientificPython

Summary:	Various Python modules for scientific computing
Name:		python-scientific
Version:	2.9.2
Release:	2
License:	CeCILL-C
Group:		Development/Python
Url:		http://dirac.cnrs-orleans.fr/ScientificPython/
Source0:	https://sourcesup.renater.fr/frs/download.php/4153/%{tarname}-%{version}.tar.gz
Patch0:		setup.py.patch
BuildRequires:	openmpi
BuildRequires:	python-numpy-devel
BuildRequires:	pkgconfig(netcdf)
BuildRequires:	pkgconfig(ompi)
BuildRequires:	pkgconfig(python)
Requires:	python-numpy
Requires:	openmpi

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

%files
%doc LICENSE README README.MPI README.BSP Doc/CHANGELOG Doc/Reference Doc/BSP_Tutorial.pdf Examples/ Src/MPI/impipython
%attr(755,root,root) %{_bindir}/*
%{py_platsitedir}/Scientific/*
%{py_platsitedir}/*.egg-info

#----------------------------------------------------------------------------

%package devel
Summary:	Various Python modules for scientific computing, header files
Group:		Development/Python
Requires:	pkgconfig(python)
Requires:	%{name} = %{EVRD}

%description devel
Headers file associated with the python-scientific package.

%files devel
%{_includedir}/python%{py_ver}/Scientific/

#----------------------------------------------------------------------------

%prep
%setup -q -n %{tarname}-%{version}
%patch0 -p0

# fix encoding
iconv -f ISO-8859-1 -t UTF-8 LICENSE -o LICENSE-utf8
touch -r LICENSE LICENSE-utf8
mv LICENSE-utf8 LICENSE

%build
python setup.py build

%install
python setup.py install --skip-build  --root=%{buildroot}

export PYTHONPATH=%{buildroot}%{py_platsitedir}
export PYINCLUDE=`pwd`/Include

pushd Src/MPI
%ifarch x86_64
sed -i 's/lib\/python/lib64\/python/' compile.py
%endif
cat compile.py | sed 's/-I/-I$PYINCLUDE -I/' > compile-new.py
python compile-new.py

install -m 755 mpipython %{buildroot}%{_bindir}

cat <<EOF>impipython
#!/bin/bash
mpirun -np 2 `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)+'/Scientific/BSP/console.py'"` $*
EOF

popd


