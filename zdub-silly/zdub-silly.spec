%global debug_package %{nil}

%define lib_name      silly
%define lib_ver       1.1.1
%define lib_gitver    1.1.1
%define lib_semver    1.1.1
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
License:        ISC
URL:            https://gitlab.com/AntonMeep/silly
Source0:        https://code.dlang.org/packages/%{lib_name}/%{lib_gitver}.zip

BuildRequires:  setgittag
BuildRequires:  git
BuildRequires:  ldc
BuildRequires:  dub


%description
An actual description of %{lib_name}
#FIXME: generate an actual description


%package devel
Provides:       %{name}-static = %{version}-%{release}
Summary:        Support to use %{lib_name} for developing D applications
Group:          Development/Libraries

Requires:       zdub-dub-settings-hack


%description devel
Sources to use the %{lib_name} library on dub using the
zdub-dub-settings-hack method.


%prep
%autosetup -n silly-v%{lib_gitver} -p1
setgittag --rm -f v%{lib_gitver}


%build


%check


%install
mkdir -p %{buildroot}%{_includedir}/zdub/%{lib_name}/%{lib_gitver}
cp -r . %{buildroot}%{_includedir}/zdub/%{lib_name}/%{lib_gitver}/%{lib_name}


%files devel
%license LICENSE
%{_includedir}/zdub/%{lib_name}/%{lib_gitver}/%{lib_name}/


%changelog
%autochangelog
