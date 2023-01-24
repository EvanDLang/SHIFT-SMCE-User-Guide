## Questions
Before you ask a question, it is best to search for existing [Issues](https://github.com/EvanDLang/SHIFT-SMCE-User-Guide/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/EvanDLang/SHIFT-SMCE-User-Guide/issues/new).
- Provide as much context as you can about what you're running into.

We will then take care of the issue as soon as possible.



## Making Contributions

### Suggesting Enhancements

If you have suggestions on how to improve the documentation visit  [GitHub issues](/issues) to  make suggestions


### Contributions

If you want to submit changes to the documentation or add additional examples, follow the following guidelines:
  - New documentation can be added as an rst file or as a Jupyter notebook.
    - rst files are stored in source/pages and notebooks in source/notebooks
  - Make sure new notebooks are formatted with title and the code is well commented.
  - Execute the notebook prior to uploading (notebooks are not run when the docs are built).
  - Add new files to source/index.rst
  - After adding a new file, run make html (.\make.bat html if in PowerShell) in the docs directory to make sure there are no bugs
  - If additional libraries are required, update docs/environment.yml
  - Outline all changes made in the commit message

