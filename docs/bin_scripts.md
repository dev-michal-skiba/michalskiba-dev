# `bin/build_image`
Script to build Docker image of michalskiba.dev Django app.

# `bin/run_app`
Script to run michalskiba.dev Django app in Docker container along with postgresql database
which is also ran in Docker container. When image is missing for database, it will pull and create
one. If image is missing for Django app, script will fail. You need to run `build_image` first.

# `bin/run_lint_checks`
Script to run lint checks in docker container. On any of the checks' error, script
exits with status code 1 and shows what step failed. It is used as pre-commit hook to assure
that committed changes pass code style requirements.

# `bin/run_tests`
Script to run tests for the michalskiba.dev Django app in docker container. When no argument
provided, it will run tests for the whole project. When argument is specified, it will run tests
for provided directory (starting from the repository root directory). Script checks two things:
whether tests pass and whether test coverage is over 90%. If any of these checks fail, script will
exit with status code 1. It is used as pre-commit hook to assure that committed changes pass all
tests and that test cover most of the codebase.

# `bin/manage/manage`
Script to run `python manage.py [ARGS]` on Django app running in Docker container. It will
propagate `ARGS`

# `bin/manage/detect_new_raw_files`
Script to run `detect_new_raw_files` Django command on app running in docker container

# `bin/manage/makemigrations`
Script to run `makemigartions` Django default command on app running in docker container

# `bin/manage/migrate`
Script to run `migrate` Django default command on app running in docker container
