PACKAGE=BabyCam

install:
	python3 setup.py develop

uninstall: clean
	echo $(PACKAGE) successfully uninstalled!
	
clean:
	rm -rf build dist $(PACKAGE).egg-info docs-api tmp .cache
	rm /usr/local/bin/babystream 
	find . -name "*.pyc" -exec rm -rf {} \;

