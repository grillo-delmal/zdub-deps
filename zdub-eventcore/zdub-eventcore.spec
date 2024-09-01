%global debug_package %{nil}

%define lib_name      eventcore
%define lib_ver       0.9.31
%define lib_gitver    0.9.31
%define lib_semver    0.9.31
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
License:        MIT
URL:            https://github.com/vibe-d/eventcore
Source0:        https://code.dlang.org/packages/%{lib_name}/%{lib_gitver}.zip

BuildRequires:  git
BuildRequires:  ldc
BuildRequires:  dub
BuildRequires:  jq
BuildRequires:  zdub-taggedalgebraic-static


%description
An actual description of %{lib_name}
#FIXME: generate an actual description


%package devel
Provides:       %{name}-static = %{version}-%{release}
Summary:        Support to use %{lib_name} for developing D applications
Group:          Development/Libraries

Requires:       zdub-dub-settings-hack
Requires:       zdub-taggedalgebraic-static


%description devel
Sources to use the %{lib_name} library on dub using the
zdub-dub-settings-hack method.


%prep
%autosetup -n %{lib_name}-%{lib_gitver} -p1
[ -f dub.sdl ] && dub convert -f json
mv -f dub.json dub.json.base
jq '. += {"version": "0.9.31"}' dub.json.base > dub.json.ver
jq 'walk(if type == "object" then with_entries(select(.key | test("preBuildCommands*") | not)) else . end)' dub.json.ver > dub.json

mv dub.json dub.json.async
jq 'walk(if type == "object" then with_entries(select(.key | test("libasync") | not)) else . end)' dub.json.async > dub.json

mv LICENSE.txt LICENSE


%check
dub build \
    --config=epoll \
    --cache=local --temp-build \
    --skip-registry=all \
    --compiler=ldc2 \
    --deep
dub clean


%install
mkdir -p %{buildroot}%{_datadir}/dub/%{lib_name}/%{lib_gitver}
cp -r . %{buildroot}%{_datadir}/dub/%{lib_name}/%{lib_gitver}/%{lib_name}


%files devel
%license LICENSE
%{_datadir}/dub/%{lib_name}/%{lib_gitver}/%{lib_name}/


%changelog
%autochangelog
