# Copyright 1999-2004 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $header: $

DESCRIPTION="Log parsing and notification program"
HOMEPAGE="http://www.gentoo.org/~lcars/tenshi"
SRC_URI="http://www.gentoo.org/~lcars/tenshi/${P}.tar.gz"

LICENSE="GPL-2"
SLOT="0"
KEYWORDS="~x86 ~ppc ~sparc"
IUSE=""

RDEPEND="dev-lang/perl
		sys-apps/coreutils"

pkg_preinst() {
    enewgroup tenshi 
	enewuser  tenshi -1 /bin/false /var/lib/tenshi tenshi
	fowners tenshi:root /etc/tenshi/tenshi.conf
	fowners tenshi:root /var/lib/tenshi
}	

src_install() {
	sed -i -e "s:-o tenshi::" Makefile
	emake DESTDIR=${D} install
	doman tenshi.8
	exeinto /etc/init.d
	newexe tenshi.gentoo-init tenshi
	keepdir /var/lib/tenshi
}

pkg_postinst() {
	einfo
	einfo "this app was formerly known as wasabi, the name was changed"
	einfo "due to trademark issues, if you are upgrading from an old"
	einfo "wasabi version please consider removing the 'wasabi' user"
	einfo "which was created by old ebuilds."
	einfo
	einfo "Please also be aware that if upgrading from versions <=0.2"
	einfo "the configuration syntax for time intervals has changed to"
	einfo "crontab style entries, old configurations won't work, please"
	einfo "check the manpage for full details."
	einfo
}
