PACKAGE=BabyCam

install:
	sudo python3 setup.py develop

uninstall: clean
	echo $(PACKAGE) successfully uninstalled!
	
clean:
	sudo rm -rf build dist $(PACKAGE).egg-info docs-api tmp .cache
	sudo find . -name "*.pyc" -exec rm -rf {} \;

