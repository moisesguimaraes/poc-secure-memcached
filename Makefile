.PHONY: clean certs

all: certs

clean:
	git clean -fdX

certs:
	$(MAKE) -C certs
