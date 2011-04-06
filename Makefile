# Noddy Makefile for dist
# $Id: Makefile 282 2005-06-07 19:14:23Z lcars $

VERSION = 0.3.4

bindir = /usr/sbin
sysconfdir = /etc
docdir = /usr/share/doc/tenshi-${VERSION}
libdir = /var/lib/tenshi
tenshi_user = tenshi
tenshi_group = tenshi

DOCS = README INSTALL CREDITS LICENSE COPYING Changelog
SAMPLES = tenshi.conf tenshi.gentoo-init tenshi.solaris-init tenshi.ebuild
BIN = Makefile tenshi
MAN = tenshi.8

DIST_DIR = tenshi-${VERSION}
TARBALL = tenshi-${VERSION}.tar.gz

FILES = ${DOCS} ${SAMPLES} ${BIN} ${MAN}

all: ${FILES}

clean:
	rm -rf tenshi-*.tar.gz

dist: ${TARBALL}

${TARBALL}:
	mkdir -p ${DIST_DIR}
	cp ${FILES} ${DIST_DIR}
	tar czvf tenshi-${VERSION}.tar.gz ${DIST_DIR}
	rm -rf ${DIST_DIR}

install:
	install -D tenshi ${DESTDIR}${bindir}/tenshi
	[ -f ${DESTDIR}${sysconfdir}/tenshi/tenshi.conf ] || \
		install -o tenshi -g root -m 0640 -D tenshi.conf ${DESTDIR}${sysconfdir}/tenshi/tenshi.conf
	install -d ${DESTDIR}${docdir}
	install -m 0644 ${DOCS} ${DESTDIR}${docdir}/
	install -o tenshi -g root -m 750 -d ${DESTDIR}${libdir}
