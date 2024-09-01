branch="$1"
commit="$2"

deploy:
	git checkout -b $branch
	git add .
	git commit -m $commit
	git push origin $branch
