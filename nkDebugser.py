#!/usr/bin/env python

# yeah, I'm aware debugging/tracking/logging already
#   exists in Python, but this is a learning experience, dig?
######################################################
#  Import from here for debugging/tracing stuff
#   (how/what to import: _______________________)
#
#       Things to do/think about:
#       * @decorators? 
#       * colors!
#       * various flags.... 
#       * introspection to figure out how many levels down and do tabs accordingly
#       * pretty printing namespaces and stuff
#       * set this on/off
#       * how do I just print the variable I want to print out......  like instead of print("locals(): "+locals())
#
#       also... so, dealing with (legacy) code....
#       besides talking to a human, iterations are key, I think, so can I somehow accomodate/encourage that here? 
#######################################################


#SO THIS IS THE FIRST PLACE THAT YOU LEARN ABOUT CLASS STUFFF!!!!!!!!!!!!!
#   AND HOW TO IMPORT YOUR OWN STUFF!!!!!!!!!!!

#  (and some notes on OOP stuff, too)

import sys
import inspect
import pprint

####################################################################
#  how to import/use  (although I may change names/etc. as I build this)
#       to just print in color:
#           import nkDebugser
#           nkd = nkDebugser.DebugserColors()   # although don't want to pass this in, see all the notes on introspection below
#           nkd.dPrint("printme","blue")
#
#
####################################################################


class DebugserColors(object):   # if not inheriting from another class -- inherit from object!
    """ Stuff for printing color debug statements """
    
    #def __init__(self,_name_of_thing_to_debug):
    def __init__(self):
        """   Initialize/constructor

        Keyword arg (for now... since kinda using this to practice OOP,
                    choice of object blah may be weird):
        _name_of_thing_to_debug -- the actual script running from command line,
            i.e. sys.argv[0]
        
        # although there must be a better way to introspect this actually
        """ 
        self._name_of_thing_to_debug = inspect.stack()[1][3]
       
        # and now......  the colors:
        self._colors_dict={ "red": '\033[91m',
                            "blue": '\033[94m',
                            "blue": '\033[94m',
                            "magenta": '\033[95m',
                            "green": '\033[32m',
                            "yellow":'\033[93m',
                            "gray": '\033[90m',
                            "aqua": '\033[96m',
                            "lightGray": '\033[97m',
                            "clearBlackHilite": '\033[7m', # font color for everything Hilite'd is black, except for this one (font color == background color of shell)
                            "grayHilite": '\033[47m',
                            "redHilite": '\033[101m',
                            "aquaHilite": '\033[106m'   ,
                            "yellowHilite": '\033[103m',
                            "greenHilite": '\033[42m',
                            "blueHilite": '\033[46m',
                            "blackBlinking": '\033[5m',
                            "blackBold": '\033[1m',
                            "endc": '\033[0m'  # back to normal (for the shell, not black necessarily)
                            }

#    def debuggingWhat(self):
#        """ what I'm debugging. dunno if care about this, actually """
#        #return inspect.stack()[1][3]
#        return self._name_of_thing_to_debug


   # def disable(self):
   #     self.MAGENTA= self.BLUE = self.GREEN = self.RED = self.YELLOW=self.ENDC= ''

    def dPrint(self,print_str="",color_str="red"):
        """Print colored statements for debugging.
            
            Keyword arguments:
            print_str -- string to print (default '')
            color_str -- string: name of color (default 'red')
        """
        print(self._colors_dict[color_str] + print_str + self._colors_dict["endc"])


        ####################################################################################################### 
        #        OK, forget this actually. This is too hard and stupid in Python, I guess... because there may be more than one object with the same name!
        #        The code here ( http://stackoverflow.com/a/6797755) plays with globals, but if there are identical values, you'd get multiple var names!!  
        #        So, suck it up, it's dumb. 
        #
        #        So:  forget fastPrint. But keep ultPrint.  Just add another argument to ultPrint, which is 
        #                   the name of the variable you actually have to pass in manually, poor baby
        ####################################################################################################### 

#    def fastPrint(self,item,color_str="blue"):
        """ Faster alternative to something like print('this is foo: "+`foo`)
            i.e.  quickly print name of variable (or whatever) *and* it's *value*

            Ex: myvar = 10; inst.fastPrint(my_var)
            This should be printed: "my_var: 10"

            Keyword arguments:
            item -- item to print
            color_str --  name of color (default 'blue')
                            (note that leader string will be *highlighted* in color_str; 
                            actual value will be in color_str)
        """
 #       _leader_str =  "===> "+item+": "  
 #       print(self._colors_dict[color_str+"Hilite"] + _leader_str + self._colors_dict["endc"]\
 #               + self._colors_dict[color_str] + `item` + self._colors_dict["endc"]) # note the ` 

    def ultPrint(self,print_str,color_str="green",which_one="long",*item):
        """ My fave right now: includes color, indentation according to how deep, and what-called-what 

            Keyword arguments:
            item -- item to print (some var) -- OPTIONAL
            print_str -- str: name of the variable for the item, but really, could be any print_str
            color_str --  name of color (default 'green')
                            (note that leader string will be *highlighted* in color_str; 
                            actual value will be in color_str)
            which_one -- 'short' (just method names)  or 'long' (also file names) version or "no_trace" (so nothing)
        """
        #_indent = "\t"*self._get_num_tabs()   # actually.....  tabs are way too long, just do a couple spaces or something else:
        _indent = " _ "*self._get_num_tabs()   
        _leader_str =  _indent+"===> "+print_str+": "
        if item:
            _item_str = self._colors_dict[color_str] + `item` + self._colors_dict["endc"]
        else:
            _item_str=""
        if which_one != "no_trace":
            _tree =self._get_what_called_what(which_one,self._get_num_tabs())
        else:
            _tree = ""
        print(self._colors_dict[color_str+"Hilite"] + _leader_str + self._colors_dict["endc"] + _item_str + _tree)


    def _get_num_tabs(self):
        # to determine how many previous calling methods, look at length of stack... and that's how many tabs we need:
        _num_tabs = len(inspect.stack())-2
        return _num_tabs

    def _get_what_called_what(self,which_one="long",indents=0):
        """ Determining where we are/how many levels deep

            Keyword args:
            which_one -- 'short' (just method names)  or 'long' (also file names) version
            indents -- how many to indent (default = 0)
        """
        indices = range(len(inspect.stack()))
        #indices.reverse()  # reverse because I want the most recent one first......  UPDATE: NOPE. it's not quite that straightforward
        if which_one =="short": 
            return "".join( ["\n"+"  "*indents+"< " + inspect.stack()[i][3] for i in indices] ) 
        elif which_one == "long": 
            #return "".join( ["\n"+"   "*indents+"< " + inspect.stack()[i][3]  + "\t(" + inspect.stack()[i][1] + ")"  for i in indices ] )  # not aligned well...
            _aligned_str = ""
            for i in indices:
                # yes, this is bad string concatenation, but I don't care right now. I need readability
                _calling_meth = `inspect.stack()[i][3]`
                _calling_file= "("+`inspect.stack()[i][1]`+")"
                _width = 25 
                _aligned_str = _aligned_str +  "\n"+"   "*indents+"< %s%s" % (_calling_meth.ljust(_width),_calling_file.rjust(_width))
            return _aligned_str


    def availColors(self):
        """ print available color names """
        #print self._colors_dict.keys()
        #print str(self._colors_dict.keys()).replace(",","\n")   # not using pprint... because!
        for color in self._colors_dict:
            self.dPrint(color,color) 
        

    def _testing_color_nums(self,how_many):
        """ Testing what colors/highlites/blinkies/underlines/bolds, etc. are 
            associated with diff nums.
            
            Keyword args:
            how_many -- max int/up to what num to check
        """
        for color_num_thing in range(how_many):
            print color_num_thing, '\033['+`color_num_thing`+'m' + "TESTING COLOR YAY !!!!!!!!!!! "  #yay!!  see the tick marks! makes str!
 
    def _debuggingTheDebugser(self):
        #self._name_of_thing_to_debug
        #self.dPrint("............... calling dir on the instance ...................","blueHilite")
        #print dir(self)
        #self.dPrint("\n............... calling help on the instance ...................","blueHilite")
        #print help(self)

        self.dPrint("\nLater: need something to deal with (changes to) namespaces........","yellowHilite")
       
       
        self.dPrint("\nglobals: ","blueHilite"); pprint.pprint(globals())
        self.dPrint("\nlocals: ","blueHilite"); pprint.pprint(locals())

#        self.dPrint("\ninspect.stack: ","blueHilite"); pprint.pprint(inspect.stack())
#        self.dPrint("\ninspect.stack()[1] -- MOST RECENT: ","blueHilite"); pprint.pprint(inspect.stack()[1])
#        self.dPrint("\ninspect.stack()[0] -- OLDEST: ","blueHilite"); pprint.pprint(inspect.stack()[0])
#        self.dPrint("\ninspect.stack()[0][1]: ","blueHilite"); pprint.pprint(inspect.stack()[0][1])
#        self.dPrint("\ninspect.stack()[0][2]: ","blueHilite"); pprint.pprint(inspect.stack()[0][2])
#        self.dPrint("\ninspect.stack()[0][3]: ","blueHilite"); pprint.pprint(inspect.stack()[0][3])
        
 #       self.dPrint("\n............... need more introspection-y stuffs.. ..........for ex.........","blueHilite")
 #       self.dPrint("\t...how far down the calling stack....","green")
 #       self.dPrint("\t...name of current method....","green")
 #       self.dPrint("\t...what am i debugging/what passed in/ although this is dumb, need to use introspection....","green")
  #      print("\t\t"+self._name_of_thing_to_debug)

   
   
        

if __name__ == "__main__":
    instance = DebugserColors()
    instance.dPrint(".................hi! starting nkDebugser debugsing!............","clearBlackHilite")
    #instance.dPrint("the available colors: ","yellowHilite")
    #instance.availColors()
    #instance._testing_color_nums(10)
    #instance.dPrint("............... ok, testing color nums: ................","red")
    #instance.testing_color_nums(110)  # up to 110 is as interesting as it gets....
    #print "(debugging the debugser) TYPE: ", type(instance)
    #print "(debugging the debugser) instance.dPrint('hello','blue'):  ", instance.dPrint("hello","blue")
    #print "(debugging the debugser) instance.dPrint(sys.argv[0],'blue'):  ", instance.dPrint(sys.argv[0],"blue")
    instance._debuggingTheDebugser()

    myVar = "some str var"
    instance.ultPrint('myVar')
