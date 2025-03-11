#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	A friendly Python library for async concurrency and I/O
Summary(pl.UTF-8):	Przyjazna biblioteka do współbieżności asynchronicznej i we/wy
Name:		python3-trio
Version:	0.21.0
Release:	3
License:	MIT or Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/trio/
Source0:	https://files.pythonhosted.org/packages/source/t/trio/trio-%{version}.tar.gz
# Source0-md5:	86b0b3732d70e084a74d1c442ce910d3
URL:		https://pypi.org/project/trio/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-astor
BuildRequires:	python3-async_generator >= 1.9
BuildRequires:	python3-attrs >= 19.2.0
BuildRequires:	python3-idna
BuildRequires:	python3-jedi
BuildRequires:	python3-outcome
BuildRequires:	python3-pylint
BuildRequires:	python3-pytest
BuildRequires:	python3-sniffio
BuildRequires:	python3-sortedcontainers
BuildRequires:	python3-trustme
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Trio project aims to produce a production-quality, permissively
licensed async/await-native I/O library for Python. Like all async
libraries, its main purpose is to help you write programs that do
multiple things at the same time with parallelized I/O.

%description -l pl.UTF-8
Celem projektu Trio jest stworzenie produkcyjnej, mającej liberalną
licencję natywnie asynchronicznej biblioteki we/wy dla Pythona.
Podobnie jak w przypadku wszystkich innych biblioteki asynchroniczne,
głównym celem jest tworzenie programów wykonujących wiele rzeczy
jednocześnie ze zrównoleglonym we/wy.

%package apidocs
Summary:	API documentation for Python trio module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona trio
Group:		Documentation

%description apidocs
API documentation for Python trio module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona trio.

%prep
%setup -q -n trio-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest trio/_core/tests trio/tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/trio/{_core/tests,tests}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.MIT README.rst
%{py3_sitescriptdir}/trio
%{py3_sitescriptdir}/trio-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
