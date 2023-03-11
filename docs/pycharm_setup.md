# General setup
- Install **File Watchers** plugin

## Isort setup
- Go to **Preferences or Settings -> Tools -> File Watchers** and click **+** to add new watcher
  - Name: Isort
  - File type: Python
  - Scope: Project Files
  - Program: isort
  - Arguments: -sp $ContentRoot$/setup.cfg $FilePath$
  - Output paths to refresh: $FilePath$
  - Uncheck _Auto-save edited files to trigger the watcher_
  - Uncheck _Trigger the watcher on external changes_

## Black setup
- Go to **Preferences or Settings -> Tools -> File Watchers** and click **+** to add new watcher
  - Name: Black
  - File type: Python
  - Scope: Project Files
  - Program: location of black, get it by running `which black`
  - Arguments: $FilePath$
  - Output paths to refresh: $FilePath$
  - Working directory: $ProjectFileDir$
  - Uncheck _Auto-save edited files to trigger the watcher_
  - Uncheck _Trigger the watcher on external changes_

## Pytest setup
In **Preferences or Settings -> Tools -> Python Integrated Tools** set _Default test runner_ to
pytest
