#!/usr/bin/python
import sys,os
ADD_VAR='installation_dependency.cnfg'


print '''
 _    _  _____  _      _____  _____ ___  ___ _____
| |  | ||  ___|| |    /  __ \|  _  ||  \/  ||  ___|
| |  | || |__  | |    | /  \/| | | || .  . || |__
| |/\| ||  __| | |    | |    | | | || |\/| ||  __|
\  /\  /| |___ | |____| \__/\\ \_/ /| |  | || |___
 \/  \/ \____/ \_____/ \____/ \___/ \_|  |_/\____/

VERSION:  Code Initial Release    2015-09-14

Package installer utility enables you to manage package installment.
'''
#user_input = raw_input("Type your option here: ")
#print 'you just inputed',user_input
#location=raw_input("please input location: Example: /home/download/package-sample.1.0.1.zip")
#print 'location is',location


class installer(object):
    #initalize. Fetch stored confg and dump it to a cache in memory
    def __init__(self):
        self.confg = open(ADD_VAR, 'r')
        self.confg_cache={}
        #print self.confg_cache
        for line in self.confg:
            linelist=line.split(' ')
            self.confg_cache[linelist[0]]=linelist[1]
        self.confg.close()
        self.__asking()


    #Install a package
    def __install(self,package_to_install):
        if package_to_install not in self.confg_cache:
            print 'please put insert dependency rule for %s first'%package_to_install
            return self.__asking()
            
        #check if all dependencies are installed. If not, code will try to install those first for you
        result=True
        for depend in self.confg_cache[package_to_install]:
            if self.__sys_check_installed(depend):
                result=result and self.__install(depend)
        if result:
            return self.__sys_install(package_to_install)
        return False

    #to uninstall a package
    def __uninstall(self,package_to_uninstall):
        dependent_list=[]
        for key in self.confg_cache:
            if key <> package_to_uninstall and package_to_uninstall in self.confg_cache[key] and self.__sys_check_installed(key):
                dependent_list.append(key)
        if len(dependent_list)>0:
            print 'Can not uninstall. Packages below are depended on her%s'%str(dependent_list)
            return
        return self.__sys_uninstall(package_to_uninstall)
        

    #internal function to install a package. return false if installation failed
    def __sys_install(self,package):
        if os.system('apt-get install %s'%package) == 'installed':
            return True
        return False
    
    #internal function to uninstall a package. return false if installation failed
    def __sys_install(self,package):
        os.system('apt-get remove %s'%package)
        
    #internal function to check a package. return false if installation not installed yet
    def __sys_check_installed(self,package):
        if package in os.system('dpkg --get-selections | grep -v deinstall'):
            return True
        return False









    #Fetch all content from cache and print them out
    def __fetch(self):
        print '\n\nPACKAGES DEPENDENCIES SUMMARY'
        for key in self.confg_cache:
            print key,'Depends on',self.confg_cache[key]
        return self.__asking();

    #Add one row to the cache
    def __add_dep(self,package,depends):
        if package in self.confg_cache:
            print 'Invalid input. Duplication rules. Let us try again'
            return self.__asking()       
        self.confg_cache[package]=depends
        return self.__asking()

    #Exit. dump the content of cache back to file store them
    def __exit(self):
        self.confg=open(ADD_VAR, 'w')
        map(lambda x:self.confg.write('%s %s'%(x,self.confg_cache[x])),self.confg_cache)
        self.confg.close()
        print 'Thanks for using. We saved this to file for your next use',self.confg_cache
        return sys.exit()
        
    #User interaction threads.
    def __asking(self):
        print '''
OPTION:
1,List all the package installed and their dependencies
2,Add or Edit rules on package dependencies table
3,Install a package, given package name
4,Uninstall a package, given pakcage name
5,Exit
'''
        input_option = raw_input("Type your option here: ")
        if input_option=='1':
            self.__fetch()
        elif input_option=='2':
            package=raw_input('Package to install: ')
            depends=raw_input('Dependencies. If multiple, seperate by comma; If none, type in NONE:')
            self.__add_dep(package,depends)
        elif input_option=='3':
            #package=raw_input('Package to install: ')
            self.__install(raw_input('Package to install: '))
        elif input_option=='5':
            self.__exit()
        else:
            print 'invalid input'
            self.__asking()

if __name__ == '__main__':
    install_task=installer()
