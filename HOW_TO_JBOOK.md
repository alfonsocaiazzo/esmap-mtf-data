# How to create, build, and deploy the Jupyter book

First, be sure that you have read the [documentation](https://jupyterbook.org/) and installed the latest version of Jupyter Book.

- [build the book](https://jupyterbook.org/start/build.html)

- [publish the book](https://jupyterbook.org/start/publish.html)

### Publish

- Install ghp-import: `pip install ghp-import`

- Configure the gh branch using: `ghp-import -n -p -f _build/html` (it must be called from the book root directory)

- To update your online book, you would simply make changes to your book’s content on the master branch of your repository, re-build your book with jupyter-book build mybookname/ and then use `ghp-import -n -p -f mylocalbook/_build/html` as before to push the newly built HTML to the gh-pages branch.

