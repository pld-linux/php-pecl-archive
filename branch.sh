#!/bin/sh
set -e
pecl=archive
git=https://git.php.net/repository/pecl/file_formats/$pecl.git
tag=RELEASE_1_0_4
out=branch.diff

d=$-
filter() {
	set -$d
	# drop package.xml (does not apply)
	filterdiff -x '*/package.xml' | \
	# remove revno's for smaller diffs
	sed -e 's,^\([-+]\{3\} .*\)\t(revision [0-9]\+)$,\1,'
}

if [ -d $pecl ]; then
	cd $pecl
	git pull --rebase
	cd ..
else
	git clone $git
fi

export GIT_DIR=$(pwd)/$pecl/.git
git diff $tag..master | filter > $out.tmp

if cmp -s $out{,.tmp}; then
	echo >&2 "No new diffs..."
	rm -f $out.tmp
	exit 0
fi
mv -f $out{.tmp,}
