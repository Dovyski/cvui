# Clean everything up
rm -rf ./package/cvui/cvui.py
rm -rf ./package/build
rm -rf ./package/cvui.egg-info
rm -rf ./package/dist

# Copy the lastest cvui.py
cp ../cvui.py ./package/cvui/
cd package

# Upgrade everything
python -m pip install --user --upgrade setuptools wheel

# Install twine. It seems that on Windows with Anaconda,
# you need to work a bit more to install it.
#
# Linux:
# 	python -m pip install --user --upgrade twine
#
# Windows:
# 	conda config --add channels conda-forge
# 	conda install twine
conda config --add channels conda-forge
conda install twine

python setup.py sdist bdist_wheel
