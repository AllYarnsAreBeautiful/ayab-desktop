import sys   # std lib
import Image # for image operations
from optparse import OptionParser # argument parsing


def print_main_menu():
   """Print the main menu"""
    print "==================="
    print "=   AYAB CONTROL  ="
    print "==================="    
    print "= andz & chris007 ="
    print "=       v1        ="
    print "==================="
    print "Image: " + filename  
    print img.format, img.size, img.mode
    print ""
    print "1 - reqInfo"
    print "2 - reqStart"
    print "3 - cnfLine"
    print ""
    print "4 - show image"
    print "5 - print image"
    print ""
    print "0 - Exit"


def mainFunction():
   """ main """
   return


if __name__ == "__main__":

   if (len(sys.argv) < 2):
      print "Usage: ayab_control.py <FILE>"
      os.system("exit")
   else:
      filename = sys.argv[1]
      if filename != '':
         img = Image.open(filename)
         mainFunction()
      else:
         print "Please check the filename"