%global debug_package %{nil}

%define lib_name      dcv
%define lib_ver       0.3.0
%define lib_gitver    0.3.0
%define lib_semver    0.3.0
%define lib_dist      0
%define lib_commit    0000000
%define lib_short     0000000

%if 0%{lib_dist} > 0
%define lib_suffix ^%{lib_dist}.git%{lib_short}
%endif

Name:           zdub-%{lib_name}
Version:        %{lib_ver}%{?lib_suffix:}
Release:        %autorelease
Summary:        %{lib_name} library for D
Group:          Development/Libraries
License:        Apache-2.0
URL:            https://github.com/libmir/dcv
Source0:        https://github.com/libmir/dcv/archive/refs/tags/v%{lib_gitver}/dcv-%{lib_gitver}.tar.gz

BuildRequires:  setgittag
BuildRequires:  git
BuildRequires:  ldc
BuildRequires:  dub
BuildRequires:  zdub-bcaa-static
BuildRequires:  zdub-mir-algorithm-static
BuildRequires:  zdub-mir-random-static


%description
An actual description of %{lib_name}
#FIXME: generate an actual description


%package devel
Provides:       %{name}-static = %{version}-%{release}
Summary:        Support to use %{lib_name} for developing D applications
Group:          Development/Libraries

Requires:       zdub-dub-settings-hack
Requires:       zdub-bcaa-static
Requires:       zdub-mir-algorithm-static
Requires:       zdub-mir-random-static


%description devel
Sources to use the %{lib_name} library on dub using the
zdub-dub-settings-hack method.


%prep
%autosetup -n %{lib_name}-%{lib_gitver} -p1
setgittag --rm -f v%{lib_gitver}


%check
dub build \
    dcv:core \
    --cache=local --temp-build \
    --skip-registry=all \
    --compiler=ldc2 \
    --deep
dub clean


%install
mkdir -p %{buildroot}%{_includedir}/zdub/%{lib_name}/%{lib_gitver}
cp -r . %{buildroot}%{_includedir}/zdub/%{lib_name}/%{lib_gitver}/%{lib_name}


%files devel
%license LICENSE
%{_includedir}/zdub/%{lib_name}/%{lib_gitver}/%{lib_name}/


%changelog
%autochangelog
