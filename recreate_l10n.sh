#!/bin/sh

cd bumblebee_config

mkdir l10n
mkdir l10n/en_US/LC_MESSAGES/ -p
mkdir l10n/it/LC_MESSAGES/ -p

intltool-extract --type=gettext/glade main_window.ui 
intltool-extract --type=gettext/glade conf_window.ui

xgettext --language=Python --keyword=_ --keyword=N_ \
    --output=l10n/bumblebee-config-gtk.pot *.py \
    *.ui.h


# msginit --input=l10n/bumblebee-config-gtk.pot --locale=en_US -o l10n/en_US/LC_MESSAGES/bumblebee-config-gtk.po
# msginit --input=l10n/bumblebee-config-gtk.pot --locale=it -o l10n/it/LC_MESSAGES/bumblebee-config-gtk.po