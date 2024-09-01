branch=$$BRANCH

deploy:
	git checkout -b $branch
	git add .
	git commit -m $$COMMIT
	git push origin $branch

pull:
	git checkout main
	git pull