%global debug_package %{nil}

%define lib_name      inui
%define lib_ver       1.2.2
%define lib_gitver    1.2.2
%define lib_semver    1.2.2
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
License:        BSD-2-Clause
URL:            https://github.com/Inochi2D/%{lib_name}
Source0:        https://code.dlang.org/packages/%{lib_name}/%{lib_gitver}.zip

BuildRequires:  git
BuildRequires:  ldc
BuildRequires:  dub
BuildRequires:  jq
BuildRequires:  zdub-bindbc-sdl-static
BuildRequires:  zdub-fghj-static
BuildRequires:  zdub-i18n-d-static
BuildRequires:  zdub-i2d-imgui-static
BuildRequires:  zdub-i2d-opengl-static
BuildRequires:  zdub-inmath-static
BuildRequires:  zdub-inochi2d-static
BuildRequires:  zdub-tinyfiledialogs-static


%description
An actual description of %{lib_name}
#FIXME: generate an actual description


%package devel
Provides:       %{name}-static = %{version}-%{release}
Summary:        Support to use %{lib_name} for developing D applications
Group:          Development/Libraries

Requires:       zdub-dub-settings-hack
Requires:       zdub-bindbc-sdl-static
Requires:       zdub-fghj-static
Requires:       zdub-i18n-d-static
Requires:       zdub-i2d-imgui-static
Requires:       zdub-i2d-opengl-static
Requires:       zdub-inmath-static
Requires:       zdub-inochi2d-static
Requires:       zdub-tinyfiledialogs-static


%description devel
Sources to use the %{lib_name} library on dub using the
zdub-dub-settings-hack method.


%prep
%autosetup -n %{lib_name}-%{lib_gitver} -p1
[ -f dub.sdl ] && dub convert -f json
mv -f dub.json dub.json.base
jq '. += {"version": "%{version}"}' dub.json.base > dub.json.ver
jq 'walk(if type == "object" then with_entries(select(.key | test("preBuildCommands*") | not)) else . end)' dub.json.ver > dub.json


%check
dub build \
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
