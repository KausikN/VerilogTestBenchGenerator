#--Imports------------------------------------------------------------------
import tkinter as tk
import json
#---------------------------------------------------------------------------

#--Initialisations----------------------------------------------------------
first_input = True

json_filename = "input_params.json"

fields = 'Verilog Code Location (with filename)', 'Verilog Module Name', 'Destination Folder', 'Time Delay'

inputfileloc = ''
modulename = ''
destfolder = ''

inputs = []
inputs_sizes = []
inputs_withsizes = []

outputs = []
outputs_sizes = []
outputs_withsizes = []

timedelay = 5

testbenchcode = ''

testbenchcode_format = ['`include "^vtb_modulename^.v"', 'module ^vtb_modulename^_tb;', 'reg ^vtb_inputs^;', 'wire ^vtb_outputs^;', 
	'initial begin\n\t$dumpfile("^vtb_modulename^_tb.vcd");\n\t$dumpvars(0, ^vtb_modulename^_tb);\n\t^vtb_monitor^\nend', 
	'^vtb_modulename^ ^vtb_modulename^_(^vtb_inputsparams^, ^vtb_outputsparams^);', 
	'initial begin\n\t^vtb_inputinit^\n\t^vtb_inputchange^\nend', 
	'endmodule']

format_values = [['^vtb_modulename^', ''], ['^vtb_inputs^', ''], ['^vtb_inputsparams^', ''], ['^vtb_outputs^', ''],  ['^vtb_outputsparams^', ''], ['^vtb_monitor^', ''],  ['^vtb_inputinit^', ''],  ['^vtb_inputchange^', '']]

#---------------------------------------------------------------------------

#--Functions----------------------------------------------------------------
#--1--
def makeform(root, fields):
	entries = []
	for field in fields:
		row = tk.Frame(root)
		lab = tk.Label(row, width=15, text=field, anchor='w')
		ent = tk.Entry(row)
		row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
		lab.pack(side=tk.LEFT)
		ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
		entries.append((field, ent))
	return entries

#--2--
def fetch_inputs(entries):
	global first_input
	input_json = {}

	for entry in entries:
		field = entry[0]
		text  = entry[1].get()
		if field == "EnterArrayTypeDataFieldHere":
			text = text.split(",")
		input_json[field] = text
	print(input_json)
	# JSONHandler(data=input_json, json_filename=json_filename, option='a')
	first_input = False

	global inputfileloc
	global modulename
	global destfolder

	inputfileloc = input_json["Verilog Code Location (with filename)"]
	modulename = input_json["Verilog Module Name"]
	destfolder = input_json["Destination Folder"]
	timedelay = input_json["Time Delay"]

	InputOutputVerilogParser(filepath=inputfileloc, destfolder=destfolder)


#--3--
def JSONHandler(data={}, json_filename="input_params.json", option='r'):
	global first_input
	new_json = {}
	if option == 'c': # Clear
		f = open(json_filename, 'w+')
		f.write("")
		f.close()
		JSONHandler('a')
		first_input = True
		return 1

	elif option == 'r': # Read
		f = open(json_filename, 'r')
		json_str = f.read()
		f.close()
		if json_str == "":
			first_input = True
			return {}
		else:
			json_contents = json.loads(json_str)
			return json_contents

	elif option == 'a': # Append

		prev_json = JSONHandler('r')
		if first_input == True:
			for field in fields:
				new_json[field] = [data[field]]
		else :
			new_json = prev_json
			for field in fields:
				new_json[field].insert(0, data[field])
		print(new_json)

		json_str = json.dumps(new_json)
		f = open(json_filename, 'w+')
		f.write(json_str)
		f.close()
		return 2

#--4--
def FileContents(filepath):
	f = open(filepath, "r")
	return f.read()

def VectorSize(name):
	name = name.strip()
	if name.startswith('['):
		lval = name[1:name.find(':')]
		rval = name[name.find(':')+1:name.find(']')]
		return abs(int(rval) - int(lval) + 1)
	return 1

def ArraySize(name):
	name = name.strip()
	if name.startswith('['):
		name = name[name.find(']'):]
		if name.find('[') >= 0:
			name = name[name.find('['):]
			return VectorSize(name)
		return 1

	if name.find('[') >= 0:
		name = name[name.find('['):]
		return VectorSize(name)
	return 1

#--5--
def InputOutputVerilogParser(filepath, destfolder):
	global inputs
	global inputs_withsizes
	global outputs
	global outputs_withsizes
	global inputs_sizes
	global outputs_sizes
	global modulename

	contents = FileContents(filepath)
	contents = contents.split("\n")
	# print ("Contents: ", contents)
	for line in contents:
		print ("Line(wos): ", line)
		line = line.strip()	
		print ("Line(ws): ", line)				# C:\LinuxTerminalDocuments\COE17B010\VLSI\PracticeCourse\FlipFlops\Counter\Sync\Combined\UpDownSync.v

		# index = line.find("module ")
		# if index >= 0:
		# 	i=index
		# 	while line[i] != '(':
		# 		i++
		# 	modulename = line[index+7:i]

		index = line.find("input ")
		print ("InputIndex: ", index)
		if index >= 0:
			i=index
			while line[i] != ';':
				i+=1
			print ("Input: ", line[index+len("input "):i], " -- ", line[index+len("input "):i].split(","))
			inps = line[index+len("input "):i].split(",")
			inpssize = []
			i=0
			for o in inps:
				inps[i] = o.strip()

				inpssize.append([VectorSize(inps[i]), ArraySize(inps[i])])

				i+=1

			inputs_withsizes.extend(inps)
			inputs_sizes.extend(inpssize)

		index = line.find("output ")
		print ("OutputIndex: ", index)
		if index >= 0:
			i=index
			while line[i] != ';':
				i+=1
			print ("Output: ", line[index+len("output "):i], " -- ", line[index+len("output "):i].split(","))
			outs = line[index+len("output "):i].split(",")
			outssize = []
			i=0
			for o in outs:
				outs[i] = o.strip()

				outssize.append([VectorSize(outs[i]), ArraySize(outs[i])])

				i+=1
			
			outputs.extend(outs)
			outputs_sizes.extend(outssize)

	print ("Inputs: ", inputs)
	print ("Outputs: ", outputs)
	print ("Inputsize: ", inputs_sizes)
	print ("Outputsize: ", outputs_sizes)

#--6--
def AssignFormatValues():
	global format_values
	global modulename

	for f in format_values:
		if f[0] == '^vtb_modulename^':
			f[1] = modulename
		if f[0] == '^vtb_inputs^':
			for 


#---------------------------------------------------------------------------

#--Main Code----------------------------------------------------------------

root = tk.Tk()
ents = makeform(root, fields)
root.bind('<Return>', (lambda event, e=ents: fetch_inputs(e)))   
b1 = tk.Button(root, text='Done',
	command=(lambda e=ents: fetch_inputs(e)))
b1.pack(side=tk.LEFT, padx=5, pady=5)
b2 = tk.Button(root, text='Quit', command=root.quit)
b2.pack(side=tk.LEFT, padx=5, pady=5)
root.mainloop()