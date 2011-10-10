# coding: utf-8
# ls_utils.py (language-specific utilities)

# ifm(not MInclude,
from __future__ import division, print_function, unicode_literals
#)
import sys, codecs, string, time
from copy import deepcopy
from platform import python_version
#import psyco, operator, cPickle, os


#psyco.full()
IsPy2 = (python_version()[0] == "2")
IsPy3 = (python_version()[0] == "3")
RusAlphabetLower = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
RusAlphabetUpper = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
try:
	if IsPy2:
		RusAlphabetLower = RusAlphabetLower.decode("utf-8")
		RusAlphabetUpper = RusAlphabetUpper.decode("utf-8")
except:
	pass

write = sys.stdout.write
cp = deepcopy #

gDbgList = [] # for debugging purposes ##

def e(): #
	exit()

def now():
	return int(time.clock() * 1000)

def error(S): ##
	print(S)
	#writef(ErrorsFile, S)
	raise Exception(S)

def info(U, UStr):
	print("type_name(" + UStr + "):", type_name(U))
	print("dir(" + UStr + "):", dir(U))
	print(UStr + ":", U)
	print()

def suppress_output():
	import os
	Stdout = sys.stdout
	sys.stdout = open(os.devnull, "w")
	return Stdout

def restore_output(Stdout):
	sys.stdout = Stdout

def cur_dir():
	import os
	return os.getcwd()

def ch_dir(Dir):
	import os
	return os.chdir(Dir)

def caller(Up = 0):
	# return: (file, line, func, text)
	try:
		F = traceback.extract_stack(limit = Up + 2) ##
		if F:
			return F[0]
	except:
		if __debug__:
			traceback.print_exc() ##
		pass
	# running with psyco?
	return ("", 0, "", None)

def el(): #
	File, Line, Fn, Text = caller(1)
	print("error: file: " + File + ", line: " + str(Line) + ", function: " + Fn)

def cmp_to_key(CmpFn):
	class K(object):
		def __init__(self, Obj, *Args):
			self.Obj = Obj
		def __lt__(self, Other):
			return CmpFn(self.Obj, Other.Obj) < 0
		def __gt__(self, Other):
			return CmpFn(self.Obj, Other.Obj) > 0
		def __eq__(self, Other):
			return CmpFn(self.Obj, Other.Obj) == 0
		def __le__(self, Other):
			return CmpFn(self.Obj, Other.Obj) <= 0
		def __ge__(self, Other):
			return CmpFn(self.Obj, Other.Obj) >= 0
		def __ne__(self, Other):
			return CmpFn(self.Obj, Other.Obj) != 0
	return K

def equal(U0, U1):
	return U0 == U1

def rnd(N):
	import random
	return random.randint(0, N - 1)

def type_name(U):
	return type(U).__name__

def is_int(U):
	return isinstance(U, int)

def is_str(U):
	if IsPy2:
		Res = isinstance(U, str) or isinstance(U, unicode)
	else:
		Res = isinstance(U, str)
	return Res

def is_dict(U):
	return isinstance(U, dict)

def is_list(U):
	return isinstance(U, list)

def is_tuple(U):
	return isinstance(U, tuple)

def is_id(U):
	return U.isidentifier()



# list fns

def elt(List, Num):
	return List[Num]

def extend(List, *Lists):
	for L in Lists:
		List.extend(L)
	return List

def append(List, *Vals):
	extend(List, Vals)
	return List

def insert(List, Num, Val):
	List.insert(Num, Val)

def clear(List):
	del List[:]

def index(List, Val, Start = 0, End = -1):
	if End == -1:
		End = len(List)
	try:
		Res = List[Start : End].index(Val) + Start
	except:
		Res = -1
	return Res

def pop(List, *Args):
	if len(Args) == 0:
		return List.pop()
	elif len(Args) == 1:
		Num = Args[0]
		return List.pop(Num)

def order_of_list(List):
	List1 = []
	for i in range(len(List)):
		append(List1, [i, List[i]])
	Order = list(map(lambda Elt: Elt[0], sorted(List1, key = lambda Elt1: Elt1[1])))
	return Order

def delete(ListOrDict, Pos):
	del(ListOrDict[Pos])

def join(L, Sep = " "):
	S = "".join(Elt + Sep for Elt in L)
	if len(Sep) > 0:
		S = S[:-len(Sep)]
	return S

def del_all(U, Val):
	Res = [Elt for Elt in U if Elt != Val]
	if not is_list(U):
		Res = join(Res, "")
	return Res

# "safe" del in lists, dicts
def sdel(U, N): #
	try:
		del(U[N])
	except:
		pass

def in_(Elt, List):
	return Elt in List



# string fns

def lower(S):
	return S.lower()

def upper(S):
	return S.upper()

def strip(S):
	return S.strip()

def is_lower(S):
	return S.islower()

def is_upper(S):
	return S.isupper()

def is_small_en_letter(S):
	return len(S) == 1 and ("a" <= S <= "z")

def is_en_capital(S):
	return len(S) == 1 and ("A" <= S <= "Z")

def is_small_rus_letter(S):
	return len(S) == 1 and (S in RusAlphabetLower)

def is_rus_capital(S):
	return len(S) == 1 and (S in RusAlphabetUpper)

def find(S, Sub, Start = 0, End = -1):
	if End == -1:
		End = len(S)
	try:
		Res = S.find(Sub, Start, End)
	except IndexError:
		Res = -1
	return Res

def rfind(S, Sub, Start = 0, End = -1):
	if End == -1:
		End = len(S)
	Res = S.rfind(Sub, Start, End)
	return Res

def substr(S, Start, End):
	if End < 0:
		End = 0
	return S[Start : End]

def str_count(S, Sub, Start = 0, End = -1):
	if End == -1:
		End = len(S)
	return substr(S, Start, End).count(Sub)

def replace(S, Sub0, Sub1, Start = 0, End = -1):
	if End == -1:
		End = len(S)
	return substr(S, Start, End).replace(Sub0, Sub1)

def split(S, Sep = ""):
	if Sep == "":
		return S.split()
	else:
		return S.split(Sep)

def is_nat_str(S): #
	return S.isdigit()



def ar(Size, Val = 0):
	return [Val for i in range(Size)]


# file fns

def close(File):
	File.close()

def read(File):
	S = File.read(-1)
	return S

def writef(File, *Ss):
	SRes = ""
	for S in Ss:
		SRes += S
	File.write(SRes)

def open_file(Path, Mode = "r"):
	File = codecs.open(Path, Mode, "utf-8") ##
	return File

def read_file(Path):
	#File = open(Path, "r")
	File = codecs.open(Path, "r", "utf-8") ##
	S = File.read(-1)
	File.close()
	return S

def write_file(Path, *Ss):
	#File = open(Path, "w")
	File = codecs.open(Path, "w", "utf-8")
	SRes = ""
	for S in Ss:
		SRes += S
	File.write(SRes)
	File.close()

