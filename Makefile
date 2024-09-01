branch="$1"
commit="$2"

.PHONY: deploy
deploy:
	git checkout -b $branch
	git add .
	git commit -m $commit
	git push origin $branch

.PHONY: pull
pull:
	git checkout main
	git pull