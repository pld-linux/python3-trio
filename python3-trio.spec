#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	A friendly Python library for async concurrency and I/O
Summary(pl.UTF-8):	Przyjazna biblioteka do współbieżności asynchronicznej i we/wy
Name:		python3-trio
Version:	0.30.0
Release:	1
License:	MIT or Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/trio/
Source0:	https://files.pythonhosted.org/packages/source/t/trio/trio-%{version}.tar.gz
# Source0-md5:	533d80e111a7edb6fab6fd2f81112dfb
Patch0:		trio-intersphinx.patch
URL:		https://pypi.org/project/trio/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:77
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests} || %{with doc}
BuildRequires:	python3-attrs >= 23.2.0
%if "%{py3_ver}" == "3.9"
BuildRequires:	python3-exceptiongroup >= 1.2.1
%endif
BuildRequires:	python3-idna
BuildRequires:	python3-outcome
BuildRequires:	python3-pyOpenSSL >= 22.0.0
BuildRequires:	python3-sniffio >= 1.3.0
BuildRequires:	python3-sortedcontainers
%endif
%if %{with tests}
BuildRequires:	python3-astor
# TODO (not to disable test_gen)
#BuildRequires:	python3-black
BuildRequires:	python3-async_generator >= 1.9
BuildRequires:	python3-jedi
BuildRequires:	python3-pylint
#BuildRequires:	python3-pyright
#BuildRequires:	python3-ruff
BuildRequires:	python3-pytest >= 5.0
BuildRequires:	python3-trustme
%endif
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme >= 3
BuildRequires:	python3-sphinx_codeautolink
BuildRequires:	python3-sphinxcontrib-jquery
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3 >= 6.0
%endif
Requires:	python3-modules >= 1:3.9
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
%patch -P0 -p1

%build
%py3_build_pyproject

%if %{with tests}
# test_gen_exports requires black and ruff
# test_dtls fails almost all the cases
# the rest uses (localhost?) networking
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest src/trio/_core/_tests src/trio/_tests tests -k 'not test_gen_exports and not test_dtls and not test_highlevel_open_tcp_stream and not test_highlevel_socket and not test_highlevel_open_tcp_listeners and not test_highlevel_ssl_helpers and not test_socket and not test_ssl and not test_open_stream_to_socket_listener and not test_run_in_worker_thread_limiter'
%endif
%if %{with doc}
LC_ALL=C.UTF-8 \
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.MIT README.rst
%{py3_sitescriptdir}/trio
%{py3_sitescriptdir}/trio-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
