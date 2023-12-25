from os import getcwd


from WolBD import *
from WebFonction import *

bd=BD_WOL()
hostname="a"
x=bd.get_A_By_B("pc","*","hostname",hostname)
print(x)

##ip="1.1.1.1"
##mac="AAAAAAAAAAAA"
##thread_demarrer=MyThread(mythread_pc,args=(ip,mac))
##thread_demarrer.start()
##thread_demarrer.join()
##print("down")
