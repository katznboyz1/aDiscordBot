import os, sys
dirs = [
    'utils',
    'utils/logs',
    'utils/tmp',
]
for each in dirs:
    try:
        os.mkdir(each)
    except Exception as error:
        print (error)
modules = [
    'discord',
    'pillow',
    'argparse',
]
pythonPath = sys.executable
for each in modules:
    os.system('{} -m pip install {}'.format(pythonPath, each))
print ('\nDone.\n')