# coding: utf-8
# utils.py

#ifm(not MInclude,
from ls_utils import *
#)

#ErrorsPath = "Errors.txt"
#InPath = "In.txt"
#OutPath = "Out.txt"
#try:
#	ErrorsFile = open(ErrorsPath, "w")
#	InFile = open(InPath, "r")
#	OutFile = open(OutPath, "w")
#except:
#	pass ##

s0 = "0"
s9 = "9"
Blank = " "
Colon = ":"
Comma = ","
Dash = "-"
DoubleQuote = "\""
EmptyStr = "" #
Minus = "-"
MulSign = "*"
NewLine1 = "\n"
NewLine2 = "\r\n"
NewLine = NewLine1 #

LParen = "("
RParen = ")"
Plus = "+"
Quote = "\'"
Semicolon = ";"
Slash = "/"
LSqBr = "["
RSqBr = "]"
Star = "*"
Tab = "\t"
Underscore = "_"
UpArrow = "^"


#-- debugging functions --#

def msg(*Args):
	print(Args)

def profile(f, S = ""):
	Time0 = now()
	f()
	Time1 = now()
	write(S)
	Res = Time1 - Time0
	print(Res)
	return Res

def dec(N):
	return N - 1

def inc(N):
	return N + 1

def sqr(N):
	return N * N

def is_space(Ch): #
	return Ch in [" ", "\t", "\r", "\n"]

def is_fn(U):
	return type(U) == type(is_fn)

def is_prim(U):
	return is_int(U) or is_str(U)

def nums(List):
	return range(len(List))

def nums1(List):
	return range(1, len(List))



# list fns

def append_in_set(L, Val):
	if not Val in L:
		append(L, Val)

def prepend(List, Val):
	insert(List, 0, Val)

def index_from(List, N, Val):
	return index(List, Val, N, -1)

# "safe" elt
def selt(List, Num, Subst = None):
	if (Num >= 0 and Num < len(List)) or (Num < 0 and -Num - 1 < len(List)): #
		return List[Num]
	else:
		return Subst

def make_list(*Args):
	return list(Args)

def list_join(List):
	Res = []
	for Sub in List:
		extend(Res, Sub)
	return Res

def max_pos(List):
	return index(List, max(List))

def min_pos(List):
	return index(List, min(List))

def del_val(List, Val):
	N = index(List, Val)
	if N > -1:
		delete(List, N)

# shallow copy
def copy(Dest, Src):
	clear(Dest)
	extend(Dest, Src)

def list_in_order(List, OrderList):
	Res = []
	for Num in OrderList:
		append(Res, List[Num])
	return Res

def min_nonneg_pos(List):
	if len(List) == 0:
		return -1
	MinPos = max_pos(List)
	Min = List[MinPos]
	if Min < 0:
		return -1
	for i in nums(List):
		if 0 <= List[i] < Min:
			MinPos = i
			Min = List[MinPos]
	return MinPos

def first_nonneg_pos(List):
	for i in nums(List):
		if List[i] >= 0:
			return i
	return -1

def sort_by_list(MainList, ListForSorting): #
	OrderOfList = order_of_list(ListForSorting)
	copy(ListForSorting, list_in_order(ListForSorting, OrderOfList))
	copy(MainList, list_in_order(MainList, OrderOfList))



# dict fns

def append_to_dict_elt(Dict, Key, Val):
	if Key in Dict:
		append(Dict[Key], Val)
	else:
		Dict[Key] = [Val]


# string fns

def is_digit(Ch):
	return(s0 <= Ch <= s9)

def is_en_letter(S):
	return is_small_en_letter(S) or is_en_capital(S)

def is_rus_letter(S):
	return is_small_rus_letter(S) or is_rus_capital(S)

def is_small_letter(S):
	return is_small_en_letter(S) or is_small_rus_letter(S)

def is_capital(S):
	return is_en_capital(S) or is_rus_capital(S)

def is_letter(S):
	return is_small_letter(S) or is_capital(S)

def substr_from(S, Start):
	return substr(S, Start, len(S))

def substr_to(S, End):
	return substr(S, 0, End)

def starts_with(S, Sub, Pos = 0):
	return substr(S, Pos, Pos + len(Sub)) == Sub

def ends_with(S, Sub):
	return substr_from(S, len(S) - len(Sub)) == Sub

def find_all(S, Sub, Start = 0, End = -1, IsOverlapped = 0):
	Res = []
	if End == -1:
		End = len(S)
	if IsOverlapped:
		DeltaPos = 1
	else:
		DeltaPos = len(Sub)
	Pos = Start
	while 1:
		Pos = find(S, Sub, Pos, End)
		if Pos == -1:
			break
		append(Res, Pos)
		Pos += DeltaPos
	return Res

def str_lcount(S, Sub, Start = 0):
	Res = 0
	while starts_with(S, Sub, Start):
		Res += 1
		Start += len(Sub)
	return Res

def del_substr(S, Start, End):
	return substr_to(S, Start) + substr_from(S, End)

def replace_all(S, Substr0, Substr1, Start = 0, End = -1):
	if End == -1:
		End = len(S)
	return substr_to(S, Start) + replace(S, Substr0, Substr1, Start, End) + substr_from(S, End)

def is_substr(S, Sub, Start):
	return starts_with(S, Sub, Start)

def match_str(S, Pos, Sub):
	Len = len(Sub)
	if substr(S, Pos, Pos + Len) == Sub:
		Pos += Len
		IsMatch = 1
	else:
		#error(Sub + " in " + S + " not found!")
		IsMatch = 0
	return Pos, IsMatch

def match_pos(S, Pos, Sub):
	return match_str(S, Pos, Sub)[0]

def match_strs(S, Pos, Subs):
	for SubNum in nums(Subs):
		NewPos, IsMatch = match_str(S, Pos, Subs[SubNum])
		if IsMatch:
			return SubNum, NewPos
	return -1, Pos

# read from S[Pos] up to Sub
def read_up_to(S, Pos, Sub):
	Lex = ""
	Len = len(Sub)
	S1 = substr_from(S, Pos)
	PosSub = find(S1, Sub)
	if PosSub < 0:
		error(Sub + " not found!") #
	Lex = substr(S, Pos, Pos + PosSub)
	return Lex, Pos + PosSub

def read_up_to__match(S, Pos, Sub):
	Lex, Pos = read_up_to(S, Pos, Sub)
	Pos, IsMatch = match_str(S, Pos, Sub)
	return Lex, Pos

def rem_spaces(S):
	SOut = ""
	for i in range(len(S)):
		Ch = elt(S, i)
		if not is_space(Ch):
			SOut += Ch
	return SOut

def read_spaces(S, Pos):
	while is_space(selt(S, Pos)):
		Pos += 1
	return Pos

def split_once(S, SepList):
	Res = []
	PosList = []
	SepNumList = []
	for i in nums(SepList):
		Sep = SepList[i]
		append(PosList, find(S, Sep))
		append(SepNumList, i)
	sort_by_list(SepNumList, PosList)
	NonnegPos = first_nonneg_pos(PosList)
	if NonnegPos >= 0:
		append(PosList, len(S))
		Res = [substr_to(S, PosList[NonnegPos])]
		for i in range(NonnegPos, len(PosList) - 1):
			append(Res, SepNumList[i], substr(S, PosList[i] + len(SepList[SepNumList[i]]), PosList[i + 1]))
	else:
		Res = [S]
	return Res

def multisplit(S, SepList):
	SepPosListList = []
	SLen = len(S)
	SepNumList = []
	ListCount = 0
	IsOverlapped = 1
	for i in nums(SepList):
		Sep = SepList[i]
		SepPosList = find_all(S, Sep, 0, SLen, IsOverlapped)
		if SepPosList != []:
			append(SepNumList, i)
			append(SepPosListList, SepPosList)
			ListCount += 1
	if ListCount == 0:
		return [S]
	MinPosList = []
	for i in range(ListCount):
		append(MinPosList, SepPosListList[i][0])
	SepEnd = 0
	MinPosPos = min_pos(MinPosList)
	Res = []
	while 1:
		append(Res, substr(S, SepEnd, MinPosList[MinPosPos]))
		append(Res, [SepNumList[MinPosPos], MinPosList[MinPosPos]])
		SepEnd = MinPosList[MinPosPos] + len(SepList[SepNumList[MinPosPos]])
		while 1:
			MinPosPos = min_pos(MinPosList)
			if MinPosList[MinPosPos] < SepEnd:
				delete(SepPosListList[MinPosPos], 0)
				if len(SepPosListList[MinPosPos]) == 0:
					delete(SepPosListList, MinPosPos)
					delete(MinPosList, MinPosPos)
					delete(SepNumList, MinPosPos)
					ListCount -= 1
					if ListCount == 0:
						break
				else:
					MinPosList[MinPosPos] = SepPosListList[MinPosPos][0]
			else:
				break
		if ListCount == 0:
			break
	append(Res, substr_from(S, SepEnd))
	return Res

def camel(S): #
	if len(S) > 0:
		return upper(S[0]) + substr_from(S, 1)
	else:
		return ""

def find_first(argS, SubList, Start = 0, End = -1): # opt ##
	if End == -1:
		End = len(argS)
	S = substr_from(argS, Start)
	MinPos = End - Start
	ResN = -1
	for i in nums(SubList):
		Pos = find(S, SubList[i])
		if Pos != -1 and Pos < MinPos:
			MinPos = Pos
			ResN = i
	ResPos = MinPos + Start
	if ResPos == End:
		ResPos = -1
	return ResPos, ResN

def find_first_not_in(S, CharList, Start = 0, End = -1):
	if End == -1:
		End = len(S)
	for i in range(Start, End):
		if not S[i] in CharList:
			return i
	return -1

def line_to(S, Pos, argNewLine = ""): #
	if argNewLine != "":
		lNewLine = argNewLine
	else:
		lNewLine = NewLine
	NlPos = rfind(substr_to(S, Pos), lNewLine, 0, Pos)
	if NlPos > -1:
		Res = substr(S, NlPos + len(lNewLine), Pos)
	else:
		Res = substr_to(S, Pos)
	return Res

def spaces_to(S, Pos):
	NlPos = rfind(substr_to(S, Pos), NewLine, 0, Pos)
	if NlPos > -1:
		Line = substr(S, NlPos + len(NewLine), Pos)
	else:
		Line = substr_to(S, Pos)
	NonSpacePos = find_first_not_in(Line, [Blank, Tab])
	if NonSpacePos == -1:
		NonSpacePos = len(Line)
	Res = substr_to(Line, NonSpacePos)
	return Res

def is_whole_word(S, Pos, Id, WordChars = []):
	if Pos == 0:
		L = 1
	else:
		Ch = S[Pos - 1]
		if is_letter(Ch) or Ch in WordChars:
			L = 0
		else:
			L = 1
	End = Pos + len(Id)
	if End == len(S):
		R = 1
	else:
		Ch = S[End]
		if is_letter(Ch) or Ch in WordChars:
			R = 0
		else:
			R = 1
	return L and R

def find_first_at_pos(S, SubList, Pos, SubNum = 0):
	SubCount = len(SubList)
	for i in range(SubNum, SubCount):
		if starts_with(S, SubList[SubNum], Pos):
			return SubNum
	return -1



def spaces_twice(N): #
	S = ""
	for i in range(N):
		S += Blank + Blank
	return S

def _list_to_pretty_str(List, EltNum, TabCount):
	S = spaces_twice(TabCount) + LSqBr + NewLine1 #
	TabCount += 1
	Elt = selt(List, EltNum)
	while not Elt is None:
		if is_prim(Elt):
			S += spaces_twice(TabCount) + str(Elt) + Blank + NewLine1 #
		else:
			S += _list_to_pretty_str(Elt, 0, TabCount)
		EltNum += 1
		Elt = selt(List, EltNum)
	TabCount -= 1
	S += spaces_twice(TabCount) + RSqBr + NewLine1 #
	return S

def list_to_pretty_str(List, Header = ""):
	S = NewLine1 + Header + _list_to_pretty_str(List, 0, 0) + NewLine1
	return S

def pl(List, Header = ""): #pprint_list
	Res = list_to_pretty_str(List, Header)
	write(Res)
	return Res

def ol(List, Header = ""): #out_pretty_list
	write_file(OutPath, pl(List, Header)) #


def pair(Type, Val):
	return [Type, Val]

def pair_type(Pair):
	return Pair[0]

def set_pair_type(Pair, Type):
	Pair[0] = Type

def pair_val(Pair):
	return Pair[1]

def val(Pair): #
	return Pair[1]

def set_pair_val(Pair, Val): #
	Pair[1] = Val


# tree fns

def tree_from_sub_list(Top, SubList):
	return pair(Top, SubList)

def tree(Top, *Subs):
	return tree_from_sub_list(Top, list(Subs))

def top(Tree):
	return Tree[0]

# "safe" top
def s_top(Obj):
	if is_list(Obj) and len(Obj) > 0: #
		return Obj[0]
	else:
		return None

def set_top(Tree, Val):
	Tree[0] = Val

def subs(Tree):
	return Tree[1]

def sub0(Tree):
	return subs(Tree)[0]

def sub_count(Tree):
	return len(subs(Tree))

def nth_sub(Tree, Num):
	return subs(Tree)[Num]

def sub_nums(Tree):
	return range(sub_count(Tree))

