# SPDX-FileCopyrightText: 2023 - 2024 Benjamin Grande M. S. <ben.grande.b@gmail.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

## Reproducibility.
%define source_date_epoch_from_changelog 1
%define use_source_date_epoch_as_buildtime 1
%define clamp_mtime_to_source_date_epoch 1
# Changelog is trimmed according to current date, not last date from changelog.
%define _changelog_trimtime 0
%define _changelog_trimage 0
%global _buildhost %{name}
# Python bytecode interferes when updates occur and restart is not done.
%undefine __brp_python_bytecompile

Name:           @PROJECT@
Version:        @VERSION@
Release:        1%{?dist}
Summary:        @SUMMARY@

Group:          @GROUP@
Packager:       @PACKAGER@
Vendor:         @VENDOR@
License:        @LICENSE@
URL:            @URL@
BugURL:         @BUG_URL@
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       qubes-mgmt-salt
Requires:       qubes-mgmt-salt-dom0
@REQUIRES@

%description
@DESCRIPTION@

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
install -m 755 -d \
  %{buildroot}@FILE_ROOTS@ \
  %{buildroot}%{_docdir}/%{name} \
  %{buildroot}%{_defaultlicensedir}/%{name}
install -m 644 %{name}/LICENSES/* %{buildroot}%{_defaultlicensedir}/%{name}/
install -m 644 %{name}/README.md %{buildroot}%{_docdir}/%{name}/
rm -rv %{name}/LICENSES %{name}/README.md
cp -rv %{name} %{buildroot}@FILE_ROOTS@/%{name}

%check

%dnl %pre

%post
if test "$1" = "1"; then
  ## Install
  @POST_INSTALL@
elif test "$1" = "2"; then
  ## Upgrade
  @POST_UPGRADE@
fi

%preun
if test "$1" = "0"; then
  ## Uninstall
  @PREUN_UNINSTALL@
elif test "$1" = "1"; then
  ## Upgrade
  @PREUN_UPGRADE@
fi

%postun
if test "$1" = "0"; then
  ## Uninstall
  @POSTUN_UNINSTALL@
elif test "$1" = "1"; then
  ## Upgrade
  @POSTUN_UPGRADE@
fi

%files
%defattr(-,root,root,-)
%license %{_defaultlicensedir}/%{name}/*
%doc %{_docdir}/%{name}/README.md
%dir @FILE_ROOTS@/%{name}
@FILE_ROOTS@/%{name}/*
%dnl TODO: missing '%ghost', files generated during %post, such as Qrexec policies.

%changelog
@CHANGELOG@
