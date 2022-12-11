conda_env:
	conda env export --no-builds > conda_environment.yml

pkg:
	tar -czf ../obrien.tar.gz .
