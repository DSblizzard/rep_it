# coding: utf-8
# line 122

# Abbreviations:
# Ext - extended
# Mod - modifier
# Sh - shortcut

from utils import *
from ctypes import *
MapVirtualKeyA = windll.user32.MapVirtualKeyA #
from win32api import *
from win32con import *
from win32process import GetWindowThreadProcessId
from win32ui import GetForegroundWindow
import pythoncom, pyHook
from pyHook.HookManager import HookConstants
from time import sleep
from subprocess import Popen


global G

class TG():
	pass

Macros1Dict = {} # called by shortcut; Deprecated? ##
Macros2Dict = {} # called by key sequence
Macros1KeysDict = {}
Macros2KeysDict = {}
DefaultSide = "l" ##

PyHookDict = {"Oem_1": ";", "Oem_2": "/", "Oem_3": "`", "Oem_4": "[", "Oem_5": "\\", "Oem_6": "]", "Oem_7": "'", "Oem_Comma": ",", "Oem_Period": ".", "Oem_Minus": "-", "Oem_Plus": "=", "Snapshot": "prtsc", "Subtract": "sub", "Add": "add", "Multiply": "mul", "Divide": "div", "Lmenu": "lalt", "Rmenu": "ralt", "Apps": "apps", "Capital": "caps", "Lcontrol": "lctrl", "Rcontrol": "rctrl", "Delete": "del", "Return": "enter", "Escape": "esc", "Insert": "ins", "Numlock": "num", "Lshift": "lshift", "Next": "pgdn", "Prior": "pgup", "Rshift": "rshift", "Lwin": "lwin", "Rwin": "rwin"}

global BaseMods, ExtMods
BaseMods = ["alt", "ctrl", "shift", "win"]
LeftMods = ["lalt", "lctrl", "lshift", "lwin"]
RightMods = ["ralt", "rctrl", "rshift", "rwin"]
ExtMods = LeftMods + RightMods
AllMods = BaseMods + ExtMods #

ShiftDict = {"~": "`", "_": "-", "+": "=", "|": "\\", "{": "[", "}": "]", ":": ";", "\"": "'", "<": ",", ">": ".", "?": "/"}
ShiftDigits = ")!@#$%^&*("
for i in range(10):
	ShiftDict[ShiftDigits[i]] = str(i)

RevShiftDict = {}
for Key in ShiftDict:
	RevShiftDict[ShiftDict[Key]] = Key

RusAlphabetInEnLayout = "F,DULE`;PBQRKVYJGHCNEA[WXIO]SM'.Z"
RusEnLayoutDict = {}
for i in nums(RusAlphabetUpper):
	RusEnLayoutDict[RusAlphabetUpper[i]] = RusAlphabetInEnLayout[i]
	RusEnLayoutDict[RusAlphabetLower[i]] = RusAlphabetInEnLayout[i]

def key_dict():
	KeyDict = {";": 0xba, "=": 0xbb, ",": 0xbc, "-": 0xbd, ".": 0xbe, "/": 0xbf, "`": 0xc0, "[": 0xdb, "\\": 0xdc, "]": 0xdd, "'": 0xde, "+": VK_ADD, "*": VK_MULTIPLY, "add": VK_ADD, "lalt": VK_LMENU, "ralt": VK_RMENU, "apps": VK_APPS, "back": VK_BACK, "caps": VK_CAPITAL, "lctrl": VK_LCONTROL, "rctrl": VK_RCONTROL, "del": VK_DELETE, "down": VK_DOWN, "end": VK_END, "enter": VK_RETURN, "esc": VK_ESCAPE, "home": VK_HOME, "ins": VK_INSERT, "left": VK_LEFT, "num": VK_NUMLOCK, "pgdn": VK_NEXT, "pgup": VK_PRIOR, "prtsc": VK_SNAPSHOT, "right": VK_RIGHT, "scroll": VK_SCROLL, "lshift": VK_LSHIFT, "rshift": VK_RSHIFT, "space": VK_SPACE, "tab": VK_TAB, "up": VK_UP, "lwin": VK_LWIN, "rwin": VK_RWIN}
	for i in range(12): # F1 .. F12
		KeyDict["f" + str(i + 1)] = 0x70 + i
	for i in range(10): # 0 .. 9
		Ord = ord("0") + i
		KeyDict[chr(Ord)] = Ord
		KeyDict[ShiftDigits[i]] = Ord
	for i in range(26): # A .. Z, a .. z
		KeyDict[chr(ord("a") + i)] = ord("A") + i
	for ShiftKey, Key in ShiftDict.items():
		KeyDict[ShiftKey] = KeyDict[Key]
	for RusKey, EnKey in RusEnLayoutDict.items():
		KeyDict[RusKey] = EnKey
	return KeyDict

KeyDict = key_dict()

def is_modifier(Key):
	return Key in AllMods #

def key_state(Key):
	return GetKeyState(KeyDict[Key]) # GetAsyncKeyState

def is_pressed(Key):
	if Key in BaseMods:
		return is_pressed("l" + Key) or is_pressed("r" + Key)
	KeyState = key_state(Key)
	return KeyState < 0

def to_base_mod(ExtMod):
	return ExtMod[1:]

def cur_modifiers_sum(): #
	Res = 0
	N = 1
	for Mod in BaseMods:
		if is_pressed(Mod): #
			Res += N
		N *= 2
	return Res

def modifiers_sum(Mods): #
	Res = 0
	N = 1
	for Mod in BaseMods:
		if ("l" + Mod in Mods) or ("r" + Mod in Mods):
			Res += N
		N *= 2
	return Res

def set_mode(argMode, IsPrint = 1):
	global G
	G.Mode = argMode
	if IsPrint:
		print "Mode:", G.Mode

def hook():
	global G
	G.HM = pyHook.HookManager()
	G.HM.KeyDown = on_key_down
	G.HM.KeyUp = on_key_up
	G.HM.HookKeyboard()
	pythoncom.PumpMessages()

def shs_to_events(Shs):
	Events = []
	for Sh in Shs:
		Key = ""
		Mods = []
		for i in nums(BaseMods):
			PlusPos = find(Sh, "+")
			if PlusPos < 1:
				Key = Sh
				break
			append(Mods, ext_mod(substr_to(Sh, PlusPos)))
			Sh = substr_from(Sh, PlusPos + 1)
		Event = [Key, Mods]
		append(Events, Event)
	return Events

def new_macro1(Name, Count, Shortcut, Events): # , DisplayKeys
	global Macros1Dict, Macros1KeysDict
	Key = Shortcut[0][0]
	ModSum = modifiers_sum(Shortcut[0][1])
	append_to_dict_elt(Macros1KeysDict, Key, ModSum)
	Macros1Dict[(Key, ModSum)] = [Name, Count, Shortcut, Events] # , DisplayKeys
	if len(Name) > 0:
		G.MainMacroDict[replace_all(Name, " ", "_")] = [1, (Key, ModSum)]

def event_to_shortcut_str(Event):
	Res = ""
	for Mod in Event[1]:
		Res += to_base_mod(Mod) + "+"
	MainKey = Event[0]
	if MainKey == "":
		Res = Res[:-1]
	else:
		Res += MainKey
	return Res

def new_macro2(Name, Count, Shortcut, Events): # , DisplayKeys
	global Macros2Dict
	RevShortcutKeys = []
	for Event in reversed(Shortcut):
		append(RevShortcutKeys, event_to_shortcut_str(Event)) # Event[0]
	LastKeys = []
	Len = len(RevShortcutKeys)
	for i in range(3):
		if Len > i:
			append(LastKeys, RevShortcutKeys[i])
	RevShortcutKeysTuple = tuple(RevShortcutKeys)
	append_to_dict_elt(Macros2KeysDict, tuple(LastKeys), RevShortcutKeysTuple)
	Macros2Dict[RevShortcutKeysTuple] = [Name, Count, Shortcut, Events] # , DisplayKeys
	if len(Name) > 0:
		G.MainMacroDict[replace_all(Name, " ", "_")] = [2, RevShortcutKeysTuple]

def new_macro(Name, Count, Shortcut, Events): # , DisplayKeys
	if len(Shortcut) == 1:
		new_macro1(Name, Count, Shortcut, Events)
	else:
		new_macro2(Name, Count, Shortcut, Events)

def kb_event(Arg0, Arg1, Arg2, Arg3):
	keybd_event(Arg0, Arg1, Arg2, Arg3)

def key_down(Key):
	VirtualKey = KeyDict[Key]
	if Key in ExtMods: #
		ExtKey = 1
	else:
		ExtKey = 0
	kb_event(VirtualKey, MapVirtualKeyA(VirtualKey, 0), ExtKey, 0) # MapVirutalKeyW for unicode strings

def key_up(Key):
	if Key in RightMods:
		VirtualKey = KeyDict[Key]
		KeyUp = KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP
		kb_event(VirtualKey, MapVirtualKeyA(VirtualKey, 0), KeyUp, 0)
	else:
		VirtualKey = KeyDict[Key]
		KeyUp = KEYEVENTF_KEYUP
		kb_event(VirtualKey, MapVirtualKeyA(VirtualKey, 0), KeyUp, 0)

def sorted_mods(Mods): #
	Res = []
	for Mod in ExtMods:
		if Mod in Mods:
			append(Res, Mod)
	return Res

def rmods_up(Mods):
	RevSortedMods = reversed(sorted_mods(Mods))
	for Key in RevSortedMods:
		VirtualKey = KeyDict["r" + to_base_mod(Key)]
		KeyUp = KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP
		kb_event(VirtualKey, MapVirtualKeyA(VirtualKey, 0), KeyUp, 0)

def press_key(Key, Mods = []):
	global G
	SortedMods = sorted_mods(Mods)
	RevSortedMods = reversed(SortedMods)
	for Mod in SortedMods:
		key_down(Mod)
	if Key != "":
		key_down(Key)
		key_up(Key)
	for Mod in RevSortedMods:	
		key_up(Mod)
	if len(Mods) > 0: #
		rmods_up(Mods)
		#modifiers_up() #
	sleep(G.DelayAfterPress)

def modifiers_up(): #
	global G
	OrigMode = G.Mode
	set_mode("wait", IsPrint = 0)
	#if PressedMods[Key]: ##
	for Key in reversed(LeftMods): ##
		VirtualKey = KeyDict[Key]
		KeyUp = KEYEVENTF_KEYUP
		kb_event(VirtualKey, MapVirtualKeyA(VirtualKey, 0), KeyUp, 0)
	for Key in reversed(RightMods): ##
		VirtualKey = KeyDict[Key]
		KeyUp = KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP
		kb_event(VirtualKey, MapVirtualKeyA(VirtualKey, 0), KeyUp, 0)
	set_mode(OrigMode, IsPrint = 0)

def lctrl_lalt_pressed():
	return G.PressedMods["lalt"] and G.PressedMods["lctrl"] and not G.PressedMods["lshift"] and not G.PressedMods["lwin"]

def check_meta_commands():
	global G
	if G.Mode == "wait":
		IsReturn = 1
	else:
		IsReturn = 0
	if lctrl_lalt_pressed():
		if G.CurKey in ["f1", "f2"]:
			if G.Mode == "hook":
				if G.CurKey == "f1":
					G.DisplayKeys = 0
				else:
					G.DisplayKeys = 1
				modifiers_up()
				set_mode("start record1")
			elif G.Mode == "record1":
				G.HotKeys = G.PressedKeys[:]
				G.PressedKeys = []
				modifiers_up()
				set_mode("start record2")
		elif G.CurKey == "f3":
			if G.Mode == "record2":
				sHotKeys = unparse_keys(G.HotKeys)
				EventsKeys = G.PressedKeys[:]
				sEvents = unparse_keys(EventsKeys)
				Name = ""
				Count = 1
				new_macro(Name, Count, shs_to_events(G.HotKeys), shs_to_events(EventsKeys)) # , G.DisplayKeys
				G.MacrosS += "\n<Name>\n<Shortcut>" + sHotKeys + "\n<Events>" + sEvents + "\n"
				write_file("macros.txt", G.MacrosS)
				G.PressedKeys = []
				set_mode("end record2")
			elif G.Mode == "wait":
				set_mode("hook")
			else:
				reload_all()
		elif G.CurKey == "f4":
			IsReturn = 1
			set_mode("wait") #
			reload_all()
		elif G.CurKey == "e":
			Popen(["start", "notepad", "macros.txt"], shell = True)
	return IsReturn

def event_key(Event):
	Key = Event.Key
	if Key in PyHookDict:
		Key = PyHookDict[Key]
	else:
		Key = lower(Key)
	return Key

def lang():
	hWnd = GetForegroundWindow().GetSafeHwnd()
	ThreadId, ProcessId = GetWindowThreadProcessId(hWnd)
	KbLayout = GetKeyboardLayout(ThreadId)
	LangCode = hex(int(KbLayout))[-3:]
	if hex(int(KbLayout))[-3:] == "409":
		Res = "en"
	else:
		Res = "ru"
	return Res

def pressed_shortcut_str():
	global G
	Res = ""
	for Mod in ExtMods:
		if G.PressedMods[Mod]:
			Res += "+" + to_base_mod(Mod)
	if G.CurKey != "":
		Res += "+" + G.CurKey
	return Res[1:]

def on_key_down(Event):
	global G
	G.CurKey = event_key(Event)
	if G.CurKey in ExtMods:
		G.PressedMods[G.CurKey] = 1
	else:
		G.PressedMainKey = G.CurKey
	if G.Mode == "play":
		return True
	elif G.Mode == "start play":
		return False #
	elif G.Mode == "start record1":
		G.WasDown = 1
		set_mode("record1")
		return bool(G.DisplayKeys)
	elif G.Mode == "start record2":
		G.WasDown = 1
		set_mode("record2")
		return True
	IsReturn = check_meta_commands()
	if IsReturn:
		return True
	if G.Mode == "hook":
		if G.CurKey in Macros1KeysDict:
			CurModsSum = cur_modifiers_sum() ##
			if CurModsSum in Macros1KeysDict[G.CurKey]:
				G.MacroBlock = Macros1Dict[(G.CurKey, CurModsSum)]
				G.CurHotKey = G.CurKey
				set_mode("start play")
				return False
		if not is_modifier(G.CurKey):
			G.Last10Keys = [pressed_shortcut_str()] + G.Last10Keys[:-1]
			for i in range(3): # opt
				LastKeys = tuple(G.Last10Keys[ : 3 - i])
				if LastKeys in Macros2KeysDict:
					break
			if LastKeys in Macros2KeysDict: #
				for RevShortcutKeys in Macros2KeysDict[LastKeys]:
					if tuple(G.Last10Keys[: len(RevShortcutKeys)]) == RevShortcutKeys:
						G.MacroBlock = Macros2Dict[RevShortcutKeys]
						G.CurHotKey = G.CurKey
						set_mode("start play")
						return True
		return True
	elif G.Mode == "record1":
		G.WasDown = 1
		return bool(G.DisplayKeys)
	elif G.Mode == "record2":
		G.WasDown = 1
		return True
	elif G.Mode == "end record2":
		set_mode("hook")
		return False
	elif G.Mode in ["start record1", "start record2", "wait"]: #
		return False
	elif G.Mode == "record2":
		if G.CurKey == "pause" or G.SleepRecordingRemain > 0:
			return False
		else:
			return True
	else:
		return True # pass the event to other handlers

def play_macro():
	global G
	Count = G.MacroBlock[1]
	Events = G.MacroBlock[3]
	for i in range(Count):
		modifiers_up()
		for Event in Events:
			Key = Event[0]
			Mods = Event[1]
			if Key == "sleep":
				G.WasSleep = 1
				sleep(Mods[0])
			elif Key == "sl":
				G.SavedLang = lang() ##
			elif Key in ["en", "ru", "rl"]:
				Lang = lang() ##
				if (Key == "en" and Lang == "ru") \
						or (Key == "ru" and Lang == "en") \
						or (Key == "rl" and Lang != G.SavedLang and Lang != ""):
					press_key("", ["lalt", "lshift"]) #
					#LoadKeyboardLayout("0x09", 1) # LANG_ENGLISH, 0x0C09
					#LoadKeyboardLayout("LANG_RUSSIAN", 1) # LANG_RUSSIAN, 0x0419, 67699721
			elif Key in G.MainMacroDict:
				MacroType = G.MainMacroDict[Key][0]
				if MacroType == 1:
					Key1, ModsSum = G.MainMacroDict[Key][1]
					G.MacroBlock = Macros1Dict[(Key1, ModsSum)]
				elif MacroType == 2:
					RevShortcutKeys = G.MainMacroDict[Key][1]
					G.MacroBlock = Macros2Dict[RevShortcutKeys]
				play_macro()
			elif selt(Key, 0) == "s" and is_nat_str(Key[1:]):
				G.WasSleep = 1
				sleep(int(Key[1:]) / 10)
			else:
				press_key(Key, Mods)
	modifiers_up()

def record_sleep_data():
	global G
	if Key == "pause":
		G.SleepRecordingRemain = 2
		return
	# G.SleepRecordingRemain > 0
	if is_nat_str(Key):
		IsDigit = 1
	elif starts_with(Key, "numpad"):
		Key = Key[6:]
		IsDigit = 1
	else:
		IsDigit = 0
	if IsDigit:
		if G.SleepRecordingStr == "":
			G.SleepRecordingStr = Key
		elif G.SleepRecordingStr[-1] == ".":
			G.SleepRecordingStr += Key
			G.SleepRecordingRemain = 0
	elif Key in [".", ",", "decimal"]:
		if G.SleepRecordingStr == "":
			G.SleepRecordingStr = "0."
		elif find(G.SleepRecordingStr, ".") == -1:
			G.SleepRecordingStr += "."
		G.SleepRecordingRemain = 1

def record(Key):
	global G
	if Key == "pause" or G.SleepRecordingRemain > 0:
		Record2RetVal = False
		record_sleep_data()
		if G.SleepRecordingRemain == 0:
			sKeys = "sleep " + G.SleepRecordingStr
			append(G.PressedKeys, sKeys)
	else:
		Record2RetVal = True
		sKeys = ""
		for Mod in ExtMods:
			if G.PressedMods[Mod]:
				sKeys += "+" + to_base_mod(Mod)
		if Key in ExtMods:
			sKeys += "+" + to_base_mod(Key)
		if G.PressedMainKey != "":
			sKeys += "+" + G.PressedMainKey
		append(G.PressedKeys, sKeys[1:])
	G.PressedMainKey = ""
	return Record2RetVal

def on_key_up(argEvent):
	global G
	Key = event_key(argEvent)
	if Key in ExtMods:
		G.PressedMods[Key] = 0
	if G.Mode in ["record1", "record2"]:
		RetVal = True
		if G.WasDown:
			RetVal = record(Key)
			G.WasDown = 0
		if (G.Mode == "record1" and G.DisplayKeys == 0) or RetVal == False:
			return False
		else:
			return True
	else:
		if G.Mode == "start play":
			if G.CurHotKey == Key:
				set_mode("play")
				play_macro()
				if G.WasSleep:
					G.HM.UnhookKeyboard()
					G.HM.HookKeyboard()
					G.WasSleep = 0
				set_mode("hook")
				return False ##
			else:
				return False
		elif G.Mode in ["start record1", "start record2"]: #
			return False
		return True ##

def unparse_keys(Shortcuts):
	Res = ""
	for Shortcut in Shortcuts:
		if str_count(Shortcut, "shift+") == 1 and str_count(Shortcut, "+") == 1:
			Key = Shortcut[len("shift+"):]
			if is_small_letter(Key):
				Shortcut = upper(Key)
			elif Key in RevShiftDict:
				Shortcut = RevShiftDict[Key]
		Res += " " + Shortcut
	Res = Res[1:] # RawOff +
	return Res

def ext_mod(Mod):
	return DefaultSide + Mod

def handle_letter(Key, Mods):
	if is_en_capital(Key):
		Key = lower(Key) #
		append(Mods, ext_mod("shift"))
	elif is_small_rus_letter(Key):
		Key = lower(KeyDict[Key])
	elif is_rus_capital(Key):
		Key = lower(KeyDict[Key]) #
		append(Mods, ext_mod("shift"))
	return Key

def parse_RawOff_str(S):
	Keys = split(S)
	KeysWithMods = []
	SkipCount = 0
	for i in nums(Keys):
		if SkipCount > 0:
			SkipCount -= 1
			continue
		Key = Keys[i]
		Mods = []
		if len(Key) != 1:
			KeysTogether = split(Key, "+")
			Key = ""
			for Key2 in KeysTogether:
				if Key2 in BaseMods:
					append(Mods, ext_mod(Key2)) ##
				else:
					Key = Key2
					if Key in ShiftDict:
						append(Mods, ext_mod("shift"))
			if Key == "sleep":
				SkipCount = 1
				Mods = [float(Keys[i + 1])]
		elif Key in ShiftDict:
			append(Mods, ext_mod("shift"))
		else:
			Key = handle_letter(Key, Mods)
		append(KeysWithMods, [Key, Mods])
	return KeysWithMods

def parse_RawOn_str(S):
	Res = []
	for Key in S:
		Mods = []
		if Key == " ":
			Key = "space"
		elif Key == "\t":
			Key = "tab"
		elif Key == "\n":
			Key = "enter"
		elif Key in ShiftDict:
			append(Mods, ext_mod("shift"))
		else:
			Key = handle_letter(Key, Mods)
		append(Res, [Key, Mods])
	return Res

def parse_keys_str(S):
	Ms = multisplit(S, ["<r+>", "<r->"])
	if Ms[0] != "":
		Res = parse_RawOff_str(Ms[0]) #
	else:
		Res = []
	for i in range( int( (len(Ms) - 1) / 2 ) ):
		Substr = Ms[2 * i + 2]
		if Ms[2 * i + 1][0] == 0:
			extend(Res, parse_RawOn_str(Substr))
		else:
			extend(Res, parse_RawOff_str(Substr))
	return Res

def parse_in_str(S):
	# Name, Shortcut and Events are required
	NameTag = "<Name>"
	CommentTag = "<Comment>"
	CountTag = "<Count>"
	ShortcutTag = "<Shortcut>"
	EventsTag = "<Events>"
	Blocks0 = split(S, NameTag)
	TagList = [CountTag, ShortcutTag, EventsTag]
	IndexDict = {}
	for i in nums(TagList):
		IndexDict[TagList[i]] = i
	for Block in Blocks0:
		if Block != "":
			Split = split_once(Block, TagList)
			Name = Split[0].rstrip("\n")
			Count = 1
			for i in range((len(Split) - 1) // 2):
				TagNum = Split[2 * i + 1]
				Sub = Split[2 * i + 2].rstrip("\n")
				if TagNum == IndexDict[CountTag]:
					Count = int(Sub)
				elif TagNum == IndexDict[ShortcutTag]:
					Shortcut = parse_keys_str(Sub)
				elif TagNum == IndexDict[EventsTag]:
					Events = parse_keys_str(Sub)
			new_macro(Name, Count, Shortcut, Events)

def reload_all():
	global G
	G = TG()
	G.CurHotKey = ""
	G.CurKey = ""
	G.DelayAfterPress = 0.002
	G.SleepRecordingRemain = 0
	G.MacroBlock = []
	G.MainMacroDict = {}
	G.PressedMainKey = ""
	G.PressedMods = {}
	G.SavedLang = ""
	G.SleepRecordingStr = ""
	G.WasSleep = 0
	for Key in ExtMods:
		G.PressedMods[Key] = int(is_pressed(Key))
	G.Last10Keys = []
	for i in range(10):
		append(G.Last10Keys, "")
	G.PressedKeys = []
	G.HotKeys = []
	G.MacrosS = read_file("macros.txt")
	G.MacrosS = del_all(G.MacrosS, "\r")
	parse_in_str(G.MacrosS)
	set_mode("hook")

reload_all()

#sleep(2)
#kb_event(KeyDict["shift"], 0x2a, 0, 0)
#VK = KeyDict["caps"]
#kb_event(VK, MapVirtualKeyA(VK, 0), 0, 0)
#kb_event(VK, MapVirtualKeyA(VK, 0), KEYEVENTF_KEYUP, 0)
#kb_event(KeyDict["shift"], 0x2a, KEYEVENTF_KEYUP, 0)

hook()

