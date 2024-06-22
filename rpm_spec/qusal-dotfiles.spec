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

Name:           qusal-dotfiles
Version:        0.0.1
Release:        1%{?dist}
Summary:        Ben Grande's Dotfiles

Group:          qusal
Packager:       Ben Grande
Vendor:         Ben Grande
License:        AGPL-3.0-or-later AND BSD-2-Clause AND CC-BY-SA-3.0 AND CC-BY-SA-4.0 AND GFDL-1.3-or-later AND GPL-2.0-only AND GPL-3.0-only AND GPL-3.0-or-later AND MIT AND Vim
URL:            https://github.com/ben-grande/qusal
BugURL:         https://github.com/ben-grande/qusal/issues
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       qubes-mgmt-salt
Requires:       qubes-mgmt-salt-dom0


%description
Configuration and scripts targeting:

-   Usability:
    -   Vi keybindings for application movement
    -   Emacs keybindings for command-line editing
    -   XDG Specification to not clutter $HOME
-   Portability:
    -   POSIX compliant code
    -   Drop-in configuration files
    -   Tested in Qubes OS Dom0, Debian, Fedora, OpenBSD
-   Tasks:
    -   GUI: x11, gtk
    -   SCM: git, tig, git-shell
    -   Keys: gpg, ssh
    -   Networking: curl, urlview, wget, w3m
    -   Productivity: tmux, vim
    -   Shell: sh, bash, zsh, less, dircolors

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
install -m 755 -d \
  %{buildroot}/srv/salt/qusal \
  %{buildroot}%{_docdir}/%{name} \
  %{buildroot}%{_defaultlicensedir}/%{name}
install -m 644 %{name}/LICENSES/* %{buildroot}%{_defaultlicensedir}/%{name}/
install -m 644 %{name}/README.md %{buildroot}%{_docdir}/%{name}/
rm -rv %{name}/LICENSES %{name}/README.md
cp -rv %{name} %{buildroot}/srv/salt/qusal/%{name}

%check

%dnl %pre

%post
if test "$1" = "1"; then
  ## Install
  true
elif test "$1" = "2"; then
  ## Upgrade
  true
fi

%preun
if test "$1" = "0"; then
  ## Uninstall
  true
elif test "$1" = "1"; then
  ## Upgrade
  true
fi

%postun
if test "$1" = "0"; then
  ## Uninstall
  true
elif test "$1" = "1"; then
  ## Upgrade
  true
fi

%files
%defattr(-,root,root,-)
%license %{_defaultlicensedir}/%{name}/*
%doc %{_docdir}/%{name}/README.md
%dir /srv/salt/qusal/%{name}
/srv/salt/qusal/%{name}/*
%dnl TODO: missing '%ghost', files generated during %post, such as Qrexec policies.

%changelog
* Thu Jun 20 2024 Ben Grande <ben.grande.b@gmail.com> - 0e2bb5b
- fix: update dotfiles module

* Mon Jun 17 2024 Ben Grande <ben.grande.b@gmail.com> - b5ae221
- fix: update dotfiles module

* Mon Jun 17 2024 Ben Grande <ben.grande.b@gmail.com> - 1a72665
- feat: add split-gpg2 configuration

* Fri Jun 14 2024 Ben Grande <ben.grande.b@gmail.com> - fcad8cb
- feat: update dotfiles module

* Tue Jun 04 2024 Ben Grande <ben.grande.b@gmail.com> - a4848e1
- fix: update dotfiles module

* Tue May 14 2024 Ben Grande <ben.grande.b@gmail.com> - d148599
- doc: nested list indentation

* Tue Apr 30 2024 Ben Grande <ben.grande.b@gmail.com> - 5722a25
- fix: discover non-root username at runtime

* Tue Apr 23 2024 Ben Grande <ben.grande.b@gmail.com> - 69745df
- fix: update dotfiles module

* Tue Mar 19 2024 Ben Grande <ben.grande.b@gmail.com> - 4097af2
- fix: update dotfiles module

* Thu Mar 14 2024 Ben Grande <ben.grande.b@gmail.com> - 8a0c004
- fix: update dotfiles module

* Mon Mar 11 2024 Ben Grande <ben.grande.b@gmail.com> - 49fb733
- fix: update dotfiles module

* Fri Feb 23 2024 Ben Grande <ben.grande.b@gmail.com> - 5605ec7
- doc: prefix qubesctl with sudo

* Fri Feb 23 2024 Ben Grande <ben.grande.b@gmail.com> - f513f64
- feat: better dom0 terminal usability

* Sun Feb 18 2024 Ben Grande <ben.grande.b@gmail.com> - f735474
- fix: update dotfiles module

* Sun Feb 18 2024 Ben Grande <ben.grande.b@gmail.com> - a91f488
- fix: update dotfiles module

* Sun Feb 04 2024 Ben Grande <ben.grande.b@gmail.com> - f27db69
- fix: update dotfiles module

* Wed Jan 31 2024 Ben Grande <ben.grande.b@gmail.com> - b5d7371
- fix: thunar requires xfce helpers to find terminal

* Mon Jan 29 2024 Ben Grande <ben.grande.b@gmail.com> - 6efcc1d
- chore: copyright update

* Fri Jan 26 2024 Ben Grande <ben.grande.b@gmail.com> - a04960c
- feat: initial split-mail setup

* Sun Jan 21 2024 Ben Grande <ben.grande.b@gmail.com> - d75a59f
- fix: update dotfiles module

* Thu Jan 18 2024 Ben Grande <ben.grande.b@gmail.com> - 0dd627b
- fix: update dotfiles module

* Fri Jan 12 2024 Ben Grande <ben.grande.b@gmail.com> - 6828e83
- fix: update dotfiles module

* Thu Dec 28 2023 Ben Grande <ben.grande.b@gmail.com> - bd54499
- fix: update dotfiles module

* Wed Dec 27 2023 Ben Grande <ben.grande.b@gmail.com> - 652b4f0
- fix: update dotfiles module

* Thu Dec 21 2023 Ben Grande <ben.grande.b@gmail.com> - a27493c
- fix: update dotfiles module

* Tue Nov 21 2023 Ben Grande <ben.grande.b@gmail.com> - 20115a2
- fix: udpate dotfiles module

* Mon Nov 20 2023 Ben Grande <ben.grande.b@gmail.com> - 83c17c4
- fix: update dotfiles module

* Mon Nov 13 2023 Ben Grande <ben.grande.b@gmail.com> - 5eebd78
- refactor: initial commit