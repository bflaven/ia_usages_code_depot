# ia_usages_code_depot


I have restructured the repository. My concern is to keep track of the food for thought.

**Bonanzas are prompts not code anymore!**

**For more check https://github.com/bflaven/ia_usages**


My wish is to keep a prompt's corpus which provides "food for thought" and I need to have access. According to me, Prompts are now more valuable than code! Even though code or prompt can potentially expose sensitive information or constitute an infraction against some clients or some employers!  That is the price to pay.


**GIT COMMANDS REMINDER**

```bash
# GIT

# suppose you have set a personal access token
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token


# go to the directory
cd /Users/brunoflaven/Documents/03_git/ia_usages_code_depot

# create the directory
git remote add origin fastapi_database
# know your branch
git branch


# check for status
git status


# for any change just type this command
git add .

# add a commit with a message
git commit -am "add usecase"
git commit -am "add files"
git commit -am "update files"
git commit -am "add files and update readme"
git commit -am "add to .svg the Musk\'s Favorite Letter X"
git commit -am "add .gitignore"
git commit -am "add docker files"
git commit -am "update readme"
git commit -am "add some code in grammar_correction_language_tool_python"
git commit -am "add some code in code_grammar_correction_language_tool_python"
git commit -am "add some code in code_leonvanzyl_langchain_python_tutorial and code_grammar_correction_language_tool_python"
git commit -am "move some code to ia_usages_code_depot"
git commit -am "change path"
git commit -am "update directory"
git commit -am "update directory and add readme"
git commit -am "update readme with python code"

# push to github if your branch on github is master
# git push origin master
git push

# Repair Permissions
cd /Users/brunoflaven/Documents/03_git/ia_usages_code_depot


# groupname is staff on a mac
sudo chgrp -R groupname .
sudo chmod -R g+rwX .
sudo find . -type d -exec chmod g+s '{}' +




```