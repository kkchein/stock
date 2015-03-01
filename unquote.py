#def get_site( stkID = 2330, month = 1, day = 1, year = 1985, start = 0, num =30):
#        return 'https://www.google.com/finance/historical?q=TPE:' + \
#                str( stkID ) + '&startdate=' + \
#                str(day) + '/' + str(month) + '/' + str(year) + \
#               '&start=' + str(start) + '&num=' + str(num)
#print(get_site())

import urllib.parse
import tkinter

root=tkinter.Tk()
root.grid()
label1=tkinter.Label(root)
label1["text"]="Quote:"
label1.grid(row=0, column=0)
input1=tkinter.Entry(root)
input1["width"]=100
input1.grid(row=0, column=1)

label2=tkinter.Label(root)
label2["text"]="Unquote:"
label2.grid(row=1, column=0)
input2=tkinter.Entry(root)
input2["width"]=100
input2.grid(row=1, column=1)

def convert_unquot ():
    oristr=input1.get()
    #print("ori:"+oristr)
    rstr=urllib.parse.unquote(oristr)
    #print("final:"+rstr)
    input2.delete(0, tkinter.END)
    input2.insert(0, rstr)

button1=tkinter.Button(root)
button1["text"]="convert"
button1["command"]=convert_unquot
button1.grid(row=2, column=0)


#print("https://www.google.com/finance/historical?q=TPE:2330&startdate=1/1/1985&start=0&num=30")
#url='https://www.google.com/finance/historical?q=TPE%3A2330&startdate=1%2F1%2F1985&start=0&num=30&ei=7ajAVOCSGc6yiALLl4HoAg'
#print(urllib.parse.unquote(url))
root.mainloop()

