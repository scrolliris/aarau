catalog-update:
	./bin/linguine-lite update message en
.PHONY: catalog-update

catalog-compile:
	./bin/linguine-lite compile message en
.PHONY: catalog-compile

catalog: | catalog-compile
.PHONY: catalog

clean:
	find . ! -readable -prune -o -print ! -path "./.git/*" ! -path "./tmp/_cache*" | \
	grep -E "(\.mo)" | xargs rm -rf

.DEFAULT_GOAL = catalog
default: catalog
