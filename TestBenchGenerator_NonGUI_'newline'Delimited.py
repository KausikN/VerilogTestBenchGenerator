#--Imports------------------------------------------------------------------
import re
import random
#---------------------------------------------------------------------------

#--Initialisations----------------------------------------------------------
first_input = True

fields = 'Verilog Code Location (with filename)', 'Verilog Module Name', 'Destination Folder', 'Clock Delay', 'Time Delay', 'No of Test Cases'

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
clockdelay = 5
nooftestcases = 5

alltestcases = False

testbenchcode_format = ['`include "^vtb_modulename^.v"', 'module ^vtb_modulename^_tb;', '^vtb_inputs^', '^vtb_outputs^', 
	'initial begin\n\t$dumpfile("^vtb_modulename^_tb.vcd");\n\t$dumpvars(0, ^vtb_modulename^_tb);\n\t^vtb_monitor^\nend', 
	'^vtb_modulename^ ^vtb_modulename^_(^vtb_inputsparams^, ^vtb_outputsparams^);', 
	'^vtb_clkname^\n', 
	'initial begin\n^vtb_inputinit^\n^vtb_inputchange^\nend', 
	'endmodule']

format_values = [['^vtb_modulename^', ''], ['^vtb_inputs^', ''], ['^vtb_inputsparams^', ''], ['^vtb_outputs^', ''],  ['^vtb_outputsparams^', ''], ['^vtb_monitor^', ''],  ['^vtb_inputinit^', ''],  ['^vtb_inputchange^', ''], 
				['^vtb_clockdelay^', ''], ['^vtb_clkname^', '']]

clock_inp_names = ['clk', 'clock']

#---------------------------------------------------------------------------

#--Functions----------------------------------------------------------------
#--1--
def fetch_inputs(fields):
	global first_input
	input_dict = {}

	for field in fields:
		text  = input(field + ": ")
		if field == "EnterArrayTypeDataFieldHere":
			text = text.split(",")
		input_dict[field] = text
	print(input_dict)

	first_input = False

	global inputfileloc
	global modulename
	global destfolder
	global timedelay
	global clockdelay
	global nooftestcases
	global alltestcases

	if input_dict["Verilog Code Location (with filename)"] != '':
		inputfileloc = input_dict["Verilog Code Location (with filename)"]
	if input_dict["Verilog Module Name"] != '':
		modulename = input_dict["Verilog Module Name"]
	if input_dict["Destination Folder"] != '':
		destfolder = input_dict["Destination Folder"]
	if input_dict["Time Delay"] != '':
		timedelay = int(input_dict["Time Delay"])
	if input_dict["Clock Delay"] != '':
		clockdelay = int(input_dict["Clock Delay"])
	if input_dict["No of Test Cases"] != '':
		nooftestcases = int(input_dict["No of Test Cases"])
	elif input_dict["No of Test Cases"] == '':
		alltestcases = True

	InputOutputVerilogParser(filepath=inputfileloc, destfolder=destfolder)

#--2--
def FileContents(filepath):
	f = open(filepath, "r")
	return f.read()

def VectorSize(name):
	name = name.strip()

	if re.search('^\[', name):
		lval = re.findall('^\[(.*):', name)[0]
		rval = re.findall('^\[.*:(.*)\]', name)[0]
		return (abs(int(rval) - int(lval)) + 1)
	return 1

def ArraySize(name):
	name = name.strip()

	if re.search('^\[', name):
		name = re.findall('^\[.*:.*\](.*)', name)[0]
		return ArraySize(name)
		# if re.search('\[', name):
		# 	name = re.findall('^.+\[.*:.*\]', name)[0]
		# 	return VectorSize(name)
		# return 1

	elif re.search('\[', name):
		name = re.findall('^.+(\[.*:.*\])', name)[0]
		return VectorSize(name)
	return 1

def RemoveVectorArray(name):
	name = name.strip()

	if re.search('^\[.*:.*\].*', name):
		name = re.findall('^\[.*:.*\](.*)', name)[0]
		return RemoveVectorArray(name)

	elif re.search('\[', name):
		name = re.findall('^(.+)(\[.*:.*\])', name)[0]
		return name.strip()
	return name.strip()

#--3--
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
	# contents = contents.split(";")
	# iterindex = 0
	# for i in contents:
	# 	contents[iterindex] = i + ";"
	# 	iterindex+=1
	print("\n\nCONTENTS: ", contents, "\n\n")
	for line in contents:
		print ("Line(wos): ", line)
		line = line.strip()	
		print ("Line(ws): ", line)

		if re.search('module\s+', line):
			modulename = re.findall('module\s+(.*)\(', line)[0].strip()

		if re.search('input\s+', line):
			val = re.findall('input\s+(.*);', line)[0].strip()
			if re.search('^\[', val) == None:
				print ("Input: ", val, " -- ", val.split(","))
				inps = val.split(",")
				inpssize = []
				i=0
				for o in inps:
					inps[i] = o.strip()

					inpssize.append([VectorSize(inps[i]), ArraySize(inps[i])])

					i+=1

				inputs_withsizes.extend(inps)
				inputs_sizes.extend(inpssize)
			else:
				vectorprefix = re.findall('^(\[.*:.*\]).*', val)[0]
				val = re.findall('^\[.*:.*\](.*)', val)[0]

				print ("Input: ", val, " -- ", val.split(","))
				inps = val.split(",")
				inpssize = []
				i=0
				for o in inps:
					inps[i] = vectorprefix + o.strip()

					inpssize.append([VectorSize(inps[i]), ArraySize(inps[i])])

					i+=1

				inputs_withsizes.extend(inps)
				inputs_sizes.extend(inpssize)


		if re.search('output\s+', line):
			val = re.findall('output\s+(.*);', line)[0].strip()

			if re.search('^\[', val) == None:
				print ("Output: ", val, " -- ", val.split(","))
				outs = val.split(",")
				outssize = []
				i=0
				for o in outs:
					outs[i] = o.strip()

					outssize.append([VectorSize(outs[i]), ArraySize(outs[i])])

					i+=1
				
				outputs_withsizes.extend(outs)
				outputs_sizes.extend(outssize)

			else:
				vectorprefix = re.findall('^(\[.*:.*\]).*', val)[0]
				val = re.findall('^\[.*:.*\](.*)', val)[0]

				print ("Output: ", val, " -- ", val.split(","))
				outs = val.split(",")
				outssize = []
				i=0
				for o in outs:
					outs[i] = vectorprefix + o.strip()

					outssize.append([VectorSize(outs[i]), ArraySize(outs[i])])

					i+=1
				
				outputs_withsizes.extend(outs)
				outputs_sizes.extend(outssize)

	for inp in inputs_withsizes:
		inputs.append(RemoveVectorArray(inp))

	for out in outputs_withsizes:
		outputs.append(RemoveVectorArray(out))

	print ("Inputs with sizes: ", inputs_withsizes)
	print ("Inputsize: ", inputs_sizes)
	print ("Outputs with sizes: ", outputs_withsizes)
	print ("Outputsize: ", outputs_sizes)

	print("Inputs: ", inputs)
	print("Outputs: ", outputs)

	AssignFormatValues()

	CreateOutputFile()

#--4--
def AssignFormatValues():
	global format_values
	global inputs
	global inputs_withsizes
	global outputs
	global outputs_withsizes
	global inputs_sizes
	global outputs_sizes
	global modulename
	global timedelay
	global clockdelay
	global nooftestcases
	global alltestcases

	for f in format_values:
		if f[0] == '^vtb_modulename^':

			f[1] = modulename.strip()

		if f[0] == '^vtb_inputs^':
			s = ''
			for i in inputs_withsizes:
				s = s + 'reg'
				s = s + ' '+ i
				s = s + ';\n'

			f[1] = s

		if f[0] == '^vtb_outputs^':
			s = ''
			for i in outputs_withsizes:
				s = s + 'wire'
				s = s + ' '+ i
				s = s + ';\n'

			f[1] = s

		if f[0] == '^vtb_inputsparams^':
			s = ''
			for i in inputs:
				s = s + ', .'+ i + '(' + i + ')'

			f[1] = re.findall('^, (.*)', s)[0]

		if f[0] == '^vtb_outputsparams^':
			s = ''
			for i in outputs:
				s = s + ', .'+ i + '(' + i + ')'

			f[1] = re.findall('^, (.*)', s)[0]

		if f[0] == '^vtb_monitor^':
			s = '$monitor($time, ": '
			for i in inputs:
				s = s + ', ' + i + ': %b(%d)'		# 2 prints of inp and output needed
			for i in outputs:
				s = s + ', ' + i + ': %b(%d)'

			s = s + '"'

			for i in inputs:
				s = s + ', ' + i 					# As there is %b and %d
				s = s + ', ' + i
			for i in outputs:
				s = s + ', ' + i
				s = s + ', ' + i
			s = s + ');'

			f[1] = s

		if f[0] == '^vtb_inputinit^':
			s = ''
			i=0
			for ip in inputs:
				svec = inputs_sizes[i][0]
				sarr = inputs_sizes[i][1]
				if sarr > 1:
					for j in range(sarr):
						s = s + ip + '[' + str(j) + '] = ' + str(svec) + "'b"
						for k in range(svec):
							s = s + '0'
						s = s + '; '
					s = s + '\n'
				else:
					s = s + ip + ' = ' + str(svec) + "'b"
					for k in range(svec):
						s = s + '0'
					s = s + '; '
					s = s + '\n'

			f[1] = s

		if f[0] == '^vtb_inputchange^':
			if alltestcases:
				f[1] = AllTestCases(timedelay, inputs, inputs_sizes)
			else:
				f[1] = LimitedTestCases(nooftestcases, timedelay, inputs, inputs_sizes)

		if f[0] == '^vtb_clockdelay^':

			f[1] = str(clockdelay)

		if f[0] == '^vtb_clkname^':
			clkname = ''
			for i in clock_inp_names:
				if i in inputs:
					clkname = i
			if clkname != '':
				f[1] = 'always #' + str(clockdelay)  + '\n\t' + clkname + ' = ! ' + clkname + ';'
			else:
				f[1] = ''


	print("FORMAT: ", format_values)

#--5--
def LimitedTestCases(nooftestcases, timedelay, inputs, inputs_sizes):
	s = ''
	for i in range(nooftestcases):
		s = s + '#' + str(timedelay) + ' '
		random.randint(1,2)
		i=0
		for ip in inputs:
			svec = inputs_sizes[i][0]
			sarr = inputs_sizes[i][1]
			if sarr > 1:
				for j in range(sarr):
					s = s + ip + '[' + str(j) + '] = ' + str(svec) + "'b"
					for k in range(svec):
						s = s + str(random.randint(0,1))
					s = s + '; '
				#s = s + '\n'
			else:
				s = s + ip + ' = ' + str(svec) + "'b"
				for k in range(svec):
					s = s + str(random.randint(0,1))
				s = s + '; '
				#s = s + '\n'
		s = s + '\n'
	return s

def AllTestCases(timedelay, inputs, inputs_sizes):
	s = ''
	total_size = 0
	for ip in inputs_sizes:
		total_size = total_size + (ip[0]*ip[1])

	noofcombinations = 2 ** total_size

	totinp = [0]*total_size

	print("\n")

	for i in range(noofcombinations):

		print("TestCase: ", i, "/", noofcombinations)

		s = s + '#' + str(timedelay) + ' '
		totinp = GenNextInput(totinp)

		totinpindex = 0
		index=0
		for ip in inputs:
			svec = inputs_sizes[index][0]
			sarr = inputs_sizes[index][1]
			if sarr > 1:
				for j in range(sarr):
					s = s + ip + '[' + str(j) + '] = ' + str(svec) + "'b"
					for k in range(svec):
						s = s + str(totinp[totinpindex])
						totinpindex+=1
					s = s + '; '
				#s = s + '\n'
			else:
				s = s + ip + ' = ' + str(svec) + "'b"
				for k in range(svec):
					s = s + str(totinp[totinpindex])
					totinpindex+=1
				s = s + '; '
				#s = s + '\n'

		s = s + '\n'

	return s

def GenNextInput(totinp):
	newtotinp = totinp
	i = 0
	for t in totinp:
		if t == 1:
			newtotinp[i] = 0
		elif t == 0:
			newtotinp[i] = 1
			break
		i+=1
	return newtotinp



#--6--
def CreateOutputFile():
	global testbenchcode_format
	global format_values

	global destfolder

	contents = ''
	for c in testbenchcode_format:

		for fv in format_values:
			c = c.replace(fv[0], fv[1])
		contents = contents + c
		contents = contents + '\n'
	print("OutputFileContents: ", contents)

	f = open(destfolder + '\\' + modulename + '_tb.v', 'w+')
	f.write(contents)


#---------------------------------------------------------------------------

#--Main Code----------------------------------------------------------------

fetch_inputs(fields)