env:
	conda env export --no-builds

pkg:
	tar -czf ../obrien.tar.gz .
