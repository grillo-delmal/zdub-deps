%global debug_package %{nil}

%define lib_name      i2d-imgui
%define lib_ver       0.8.0
%define lib_gitver    0.8.0
%define lib_semver    0.8.0
%define lib_dist      0
%define lib_commit    0000000
%define lib_short     0000000
%define cimgui_commit 49bb5ce65f7d5eeab7861d8ffd5aa2a58ca8f08c
%define cimgui_short  49bb5ce
%define imgui_commit  dd5b7c6847372016f45d5b5abda687bd5cd19224
%define imgui_short   dd5b7c6

%if 0%{lib_dist} > 0
%define lib_suffix ^%{lib_dist}.git%{lib_short}
%endif

Name:           zdub-%{lib_name}
Version:        %{lib_ver}%{?lib_suffix:}
Release:        %autorelease
Summary:        %{lib_name} library for D
Group:          Development/Libraries
License:        BSL-1.0 and MIT
URL:            https://github.com/Inochi2D/%{lib_name}
Source0:        https://code.dlang.org/packages/%{lib_name}/%{lib_gitver}.zip
Source1:        https://github.com/Inochi2D/cimgui/archive/%{cimgui_commit}/cimgui-%{cimgui_short}.tar.gz
Source2:        https://github.com/Inochi2D/imgui/archive/%{imgui_commit}/imgui-%{imgui_short}.tar.gz

BuildRequires:  git
BuildRequires:  ldc
BuildRequires:  dub
BuildRequires:  jq
BuildRequires:  zdub-bindbc-sdl-static
BuildRequires:  zdub-i2d-opengl-static
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  freetype-devel
BuildRequires:  SDL2-devel


%description
An actual description of %{lib_name}
#FIXME: generate an actual description


%package devel
Provides:       %{name}-static = %{version}-%{release}
Summary:        Support to use %{lib_name} for developing D applications
Group:          Development/Libraries

Requires:       zdub-dub-settings-hack
Requires:       zdub-bindbc-sdl-static
Requires:       zdub-i2d-opengl-static

Requires:       cmake
Requires:       gcc
Requires:       gcc-c++
Requires:       freetype-devel
Requires:       SDL2-devel


%description devel
Sources to use the %{lib_name} library on dub using the
zdub-dub-settings-hack method.


%prep
%autosetup -n %{lib_name}-%{lib_gitver} -p1
[ -f dub.sdl ] && dub convert -f json
mv -f dub.json dub.json.base
jq '. += {"version": "0.8.0"}' dub.json.base > dub.json.ver
jq 'walk(if type == "object" then with_entries(select(.key | test("preBuildCommands*") | not)) else . end)' dub.json.ver > dub.json

# cimgui

tar -xzf %{SOURCE1}
rm -r deps/cimgui
mv cimgui-%{cimgui_commit} deps/cimgui

tar -xzf %{SOURCE2}
rm -r deps/cimgui/imgui
mv imgui-%{imgui_commit} deps/cimgui/imgui

rm -rf deps/freetype
rm -rf deps/glbinding
rm -rf deps/glfw
rm -rf deps/SDL
rm -rf deps/cimgui/imgui/examples/

# FIX: Make i2d-imgui submodule checking only check cimgui
rm .gitmodules
cat > .gitmodules <<EOF
[submodule "deps/cimgui"]
	path = deps/cimgui
	url = https://github.com/Inochi2D/cimgui.git
EOF
mkdir deps/cimgui/.git

# Build i2d-imgui deps
mkdir -p deps/build_linux_x64_cimguiStatic
mkdir -p deps/build_linux_x64_cimguiDynamic

%ifarch x86_64
    cmake -DSTATIC_CIMGUI= -S deps -B deps/build_linux_x64_cimguiStatic
    cmake --build deps/build_linux_x64_cimguiStatic --config Release
    cmake -S deps -B deps/build_linux_x64_cimguiDynamic
    cmake --build deps/build_linux_x64_cimguiDynamic --config Release
%endif
%ifarch aarch64
    cmake -DSTATIC_CIMGUI= -S deps -B deps/build_linux_aarch64_cimguiStatic
    cmake --build deps/build_linux_aarch64_cimguiStatic --config Release
    cmake -S deps -B deps/build_linux_aarch64_cimguiDynamic
    cmake --build deps/build_linux_aarch64_cimguiDynamic --config Release
%endif

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
# Dependency licenses
install -d ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}-devel/./deps/cimgui/
install -p -m 644 ./deps/cimgui/LICENSE \
    ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}-devel/./deps/cimgui/LICENSE
install -d ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}-devel/./deps/imgui/
install -p -m 644 ./deps/cimgui/imgui/LICENSE.txt \
    ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}-devel/./deps/imgui/LICENSE.txt


%files devel
%license LICENSE
%{_datadir}/dub/%{lib_name}/%{lib_gitver}/%{lib_name}/
%{_datadir}/licenses/%{name}-devel/*


%changelog
%autochangelog
