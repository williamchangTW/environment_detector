# build file paths if necessary
import os, sys, subprocess
# install every necessary packet
# TODO
# Data File that include every necessary
def path_check():
    if os.path.exists("data") == False:
        os.popen("mkdir data")
    # Model file must include in this file
    if os.path.exists("model") == False:
        os.popen("mkdir model")
    # Store template data when something error ocuured(i,e. log)
    if os.path.exists("tmp") == False:
        os.popen("mkdir tmp")
    # checkpoint
    if os.path.exists("ckpt") == False:
        os.popen("mkdir ckpt")
    # training middle result files
    if os.path.exists("ckpt/training_A/") == False:
        os.popen("mkdir ckpt/training_A/")
    if os.path.exists("ckpt/training_B/") == False:
        os.popen("mkdir ckpt/training_B/")
    # correct files
    if os.path.exists("data/cor") == False:
        os.popen("mkdir data/cor")
    if os.path.exists("model/cor") == False:
        os.popen("mkdir model/cor")
    # debug files
    if os.path.exists("log") == False:
        os.popen("mkdir log")

# check packages version
class environment_check:
    def __init__(self, 
                 package = None,
                 version = None):
        self = self
        self.package = package
        self.version = version
    def packages(self):
        return dict(package.split('==') for package in subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode().split())
    def install(self): 
        subprocess.call([sys.executable, '-m', 'pip', 'install', self.package])
    def upgrade(self): 
        subprocess.call([sys.executable, '-m', 'pip', 'install', self.package, '==', self.version, '—force-reinstall'])
    def downgrade(self): 
        subprocess.call([sys.executable, '-m', 'pip', 'install', self.package, '==', self.version, '—force-reinstall'])



if __name__ == "__main__":
    # lib check 
    lib = ("numpy", "psutil", "tensorflow", "Keras", "h5py")
    ver = ["1.17.0", "5.6.3", "1.14.0", "2.3.0", "2.9.0"]
    for i in range(0, 4):
        if lib[i] not in environment_check(package = lib[i], version = ver[i]).packages().keys:
            environment_check(package= lib[i], version = ver[i]).install()
        elif environment_check(package= lib[i], version = ver[i]).packages() < ver[i]:
            environment_check(package= lib[i], version = ver[i]).upgrade()
        elif environment_check(package= lib[i], version = ver[i]).packages() > ver[i]:
            environment_check(package= lib[i], version = ver[i]).downgrade()
    # path check
    path_check()
        
