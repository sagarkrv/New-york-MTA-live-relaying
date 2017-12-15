git pull
git branch clean_up
git checkout clean_up
git rm -r --cached final_project
git commit -m "rm"
git checkout master
git merge clean_up
git branch -d clean_up
git push

