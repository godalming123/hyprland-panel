#!/usr/bin/env sh
nix-shell -p gobject-introspection gtk3 gtk-layer-shell python310Packages.schedule 'python310.withPackages(ps : with ps; [ pygobject3 ])'
