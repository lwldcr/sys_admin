#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2013/06/12,lwldcr@gmail.com
# simple finacial managing program

import os,sys,datetime

fname = '/Users/brucelee/Documents/Daily/cost.txt'

def menu():
    """Show menu."""
    print '''
==============================
please choose what to do:
 1 show remaining sum
 2 add a record
 3 show last week details
 4 show last two weeks details
 5 show total details
 h show this menu
 q quit program
==============================
'''

def getInput():
    """Get input character."""
    input = raw_input("enter choice:")
    while input not in ['1','2','3','4','5','H','h','Q','q']:
        input = raw_input("enter choice:")
    return input

def cmdHndlr(cmd):
    """Handle given command."""
    if cmd == 'q' or cmd == 'Q':
        raw_input('quiting...')
        sys.exit(0)
    elif cmd == 'h' or cmd == 'H':
        return
    else:
        func = [ remSum, addRec, lastWeek, last2Week, total ]
        func[int(cmd) - 1] ()
    return

def read(option):
    """Read record file."""    
    if not os.path.exists(fname):
        open(fname,'w').close()
    f = open(fname)        
    fs = f.read()
    f.close()
    
    if not fs:
        if option != 4:
            print 'No records yet!'
        return 0
    
    records = fs.split('\n')[:-1]
    rem = float(records[-1].split()[-1])
    if option == 0:        
        print 'Remaining sum:%10.2f' % rem
    elif option == 1:
        today = datetime.date.today()
        delta = datetime.timedelta(7)
        a = [ r for r in records if r.split()[0] >= str(today - delta) ]
        print '%-16s %-16s %-20s %10s %12s' % ('date',
                                               'time',
                                               'description',
                                               'money',
                                               'sum'
                                               )
        for e in a:
            print e
    elif option == 2:
        print '%-16s %-16s %-20s %10s %12s' % ('date',
                                               'time',
                                               'description',
                                               'money',
                                               'sum'
                                               )
        today = datetime.date.today()
        delta = datetime.timedelta(14)
        a = [ r for r in records if r.split()[0] >= str(today - delta) ]
        for e in a:
            print e
    elif option == 3:
        print '%-16s %-16s %-20s %10s %12s' % ('date',
                                               'time',
                                               'description',
                                               'money',
                                               'sum'
                                               )
        for e in records:
            print e
    else:
        pass
    del records
    return rem

def write(rec):
    """Write record file."""
    f = open(fname,'a+')
    f.seek(0,2)
    f.write(rec)
    f.close()
    
def remSum():
    """Show remaining sum."""
    read(0)
    
class record():
    """record class"""
    def __init__(self):
        self.num = raw_input("money:")
        while not self.num[0] in ['+','-'] or not self.num[1:].replace('.','').isdigit():
            self.num = raw_input("money:")
        ops = self.num[0]
        money = float(self.num[1:])

        self.desc = raw_input("description:")
        if ops == '+':
            self.rem = read(4) + money
        else:
            self.rem = read(4) - money
        self.rem = '%.2f' % self.rem
        
        self.date = str(datetime.date.today())
        self.time = str(datetime.datetime.now().time()).split('.')[0]

def addRec():
    """Add a record."""
    rec = record()
    string = '%-16s %-16s %-20s %10s %12s' % (rec.date,
                                              rec.time,
                                              rec.desc,
                                              rec.num,
                                              rec.rem)
    write(string + '\n')
    read(0)
    
def lastWeek():
    """Show last week details."""
    read(1)

def last2Week():
    """Show last 2 weeks details."""
    read(2)

def total():
    """Show total details."""
    read(3)
    
def main():
    """Main loop."""
    while True:
        menu()
        cmd = getInput()
        cmdHndlr(cmd)
        if cmd != 'h' and cmd != 'H':
            raw_input('press Enter to continue...')
            
if __name__ == '__main__':
    main()
