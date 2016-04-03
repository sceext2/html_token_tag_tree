# makefile, httt/

target: clean_py
.PHONY: target

clean_py:
	- find . | grep "__pycache__" | xargs rm -r
.PHONY: clean_py

# end makefile


