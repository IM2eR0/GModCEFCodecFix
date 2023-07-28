#!/usr/bin/env python3

# GModCEFCodecFix
#
# Copyright 2020-2023, Solstice Game Studios (www.solsticegamestudios.com)
# LICENSE: GNU General Public License v3.0
#
# Purpose: Automatically patches Garry's Mod's internal Chromium Embedded Framework to enable Proprietary Video/Audio codec support
#
# Contact:
#	Discord: https://www.solsticegamestudios.com/chat.html
#	Email: contact@solsticegamestudios.com

# Chinese Fix: OriginalSnow

import sys
import os
from subprocess import Popen

if sys.version_info.major != 3:
	sys.exit("ERROR: You're using a version of Python that's not supported. You must use Python 3.")

if sys.platform == "linux":
	import psutil
	import shutil

# Hold up, gotta check if it's running in a Terminal or not on Linux
possibleTerminals = [
	"x-terminal-emulator",
	"gnome-terminal",
	"terminator",
	"xfce4-terminal",
	"konsole",
	"xterm",
	"urxvt",
	"rxvt",
	"termit",
	"Eterm",
	"aterm",
	"uxterm",
	"roxterm",
	"termite",
	"lxterminal",
	"mate-terminal",
	"terminology",
	"st",
	"qterminal",
	"lilyterm",
	"tilix",
	"terminix",
	"kitty",
	"guake",
	"tilda",
	"alacritty",
	"hyper",
	"foot",
	"kgx"
]
termNotFoundError = "GModCEFCodecFix could not find a suitable Terminal Emulator!\n\tIf one is installed, Contact Us about this:\n- Discord: https://www.solsticegamestudios.com/chat.html\n- Email: contact@solsticegamestudios.com"

if sys.platform == "linux":
	if os.path.isfile("ERROR_TerminalNotFound.txt"):
		os.remove("ERROR_TerminalNotFound.txt")

	if not sys.__stdin__.isatty():
		print("ERROR: GModCEFCodecFix must run in a Terminal! Attempting to open it in one...")

		foundTerm = False
		for termEXE in possibleTerminals:
			if shutil.which(termEXE) != None:
				print("Found Terminal: " + termEXE + ", attempting to re-launch...")
				Popen([termEXE, "-e", *sys.argv], stdin=None, stdout=None, stderr=None, close_fds=True)
				foundTerm = True
				break

		if not foundTerm:
			with open("ERROR_TerminalNotFound.txt", "w") as termNotFoundFile:
				termNotFoundFile.write(termNotFoundError)

		sys.exit(not foundTerm and "Terminal not found! Writing error info to ERROR_TerminalNotFound.txt...")

# Set up At-Exit handler so it doesn't just close immediately when it's done
import atexit

launchSuccess = False
autoMode = False

@atexit.register
def exitHandler():
	if not launchSuccess or autoMode is False:
		input("按下回车键继续...")

# Set the title so it's not just some boring path
if sys.platform == "win32":
	os.system("title Garry's Mod: CEF Codec (Night) 支持程序")
else:
	print("\33]0;Garry's Mod: CEF Codec 支持程序\a", end='', flush=True)

import urllib.request
import requests
import colorama
from termcolor import colored
from time import sleep
from socket import gaierror

colorama.init()

# Spit out the Software Info
contactInfo = "\n\nGMod CEF Codec官网地址:\n- https://www.solsticegamestudios.com/forums/threads/60/\n\n国内发行版联系方式:\n- 交流群: 105969906\n- 邮箱: i@teasmc.cn\n- 论坛：https://teasmc.cn\n"

contactInfo2 = "\n国内发行版联系方式:\n\t> 交流群: 105969906\n\t> 邮箱: i@teasmc.cn\n> 论坛：https://teasmc.cn\n"

downloadLink = "GModCEFCodecFix 最新版下载链接：https://gmodcef-1301161699.cos.ap-beijing.myqcloud.com/GModCefCodecFiles/GModCEFCodecFix.exe"


print(colored("GMod CEF Codec (Night) 支持程序\n原作者: Solstice Game Studios\n修复: 初雪 OriginalSnow\n", "cyan"))
print(colored(contactInfo2 + "\n", "cyan"))


# Get CEFCodecFix's version and compare it with the version we have on the website
localVersion = 20230622
remoteVersion = 0
systemProxies = urllib.request.getproxies()

if systemProxies:
	print("System Proxies:\n" + str(systemProxies) + "\n")

try:
	versionOnline = requests.get("https://gmodcef-1301161699.cos.ap-beijing.myqcloud.com/GModCefCodecFiles/version.txt", proxies=systemProxies)
	if versionOnline.status_code == 200:
		remoteVersion = int(versionOnline.text)

		if remoteVersion > localVersion:
			print(colored("你当前正在使用的 GModCEFCodecFix 版本号为：" + str(localVersion) ,"yellow"))
			print(colored("在线版本号："+ str(remoteVersion) +"!\n", "yellow"))
			print(colored("你当前使用的 GModCEFCodecFix 版本已过时！请及时更新！\n\n", "red"))
			print(colored("警告：你当前使用的版本是强制跳过SHA256校验版，请谨慎使用该版本！如非必须请使用正常版本\n", "red"))
		else:
			print(colored("你当前正在使用的 GModCEFCodecFix 版本号为："+ str(localVersion) +"!", "yellow"))
			print(colored("在线版本号："+ str(remoteVersion) +"!\n\n", "yellow"))
			print(colored("警告：你当前使用的版本是强制跳过SHA256校验版，请谨慎使用该版本！如非必须请使用正常版本\n", "red"))

		secsToContinue = 10
		while secsToContinue:
			print(colored("\t将在 " + str(secsToContinue) + " 秒后继续...", "yellow"), end="\r")
			sleep(1)
			secsToContinue -= 1
		sys.stdout.write("\033[K\n")

except Exception as e:
	sys.exit(colored("错误: 无法连接至在线更新服务器!\n\t错误代码: " + str(versionOnline.status_code) + contactInfo, "red"))

# Let's start the show
from time import perf_counter
import vdf
from requests.structures import CaseInsensitiveDict
from steam.utils.appcache import parse_appinfo
from steamid import SteamID
from hashlib import sha256
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from bsdiff4 import file_patch

# Specific platform imports
if sys.platform == "win32":
	import winreg
else:
	from pathlib import Path
if sys.platform == "linux":
	from xdg import XDG_DATA_HOME

if len(sys.argv) >= 3:
	# sys.argv[0] is always the script/exe path
	if sys.argv[1] == "-a":
		try:
			autoMode = int(sys.argv[2])
			print(colored("自动模式: 已启用\n", "cyan"))
		except ValueError:
			print(colored("警告: 自动模式配置文件出错，请手动选择启动项目\n", "yellow"))

timeStart = perf_counter()

# Find Steam
steamPath = None
steamPathHints = {}
if sys.platform == "win32":
	# Windows
	try:
		reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
		steamKey = winreg.OpenKey(reg, "Software\\Valve\\Steam")
		steamPathValue = winreg.QueryValueEx(steamKey, "SteamPath")
		steamPath = steamPathValue[0].replace("/", "\\")
	except:
		# We wanna make sure it doesn't crash and burn while looking for the Registry Key, but we also wanna handle it below
		pass

	steamPathHints["win32"] = "Is it installed properly and been run at least once?"
elif sys.platform == "darwin":
	# macOS
	homeDir = str(Path.home())
	if os.path.isdir(os.path.join(homeDir, "Library", "Application Support", "Steam")):
		steamPath = os.path.join(homeDir, "Library", "Application Support", "Steam")

	steamPathHints["darwin"] = "Is it installed somewhere other than " + os.path.join(homeDir, "Library", "Application Support", "Steam") + " ?"
else:
	# Linux
	homeDir = str(Path.home())
	dataDir = str(XDG_DATA_HOME)

	if os.path.isdir(os.path.join(homeDir, ".steam", "steam")):
		steamPath = os.path.join(homeDir, ".steam", "steam")
	elif os.path.isdir(os.path.join(homeDir, ".var", "app", "com.valvesoftware.Steam", ".steam", "steam")):
		steamPath = os.path.join(homeDir, ".var", "app", "com.valvesoftware.Steam", ".steam", "steam")
	elif os.path.isdir(os.path.join(dataDir, "Steam")):
		steamPath = os.path.join(dataDir, "Steam")

	steamPathHints["linux"] = "Is it installed somewhere other than " + os.path.join(homeDir, ".steam", "steam") + " or " + os.path.join(dataDir, "Steam") + " ?"

if steamPath:
	steamPath = os.path.normcase(os.path.realpath(steamPath))
	print("Steam 路径:\n" + steamPath + "\n")
else:
	sys.exit(colored("错误: Steam 路径未找到!\n" + steamPathHints[sys.platform] + contactInfo, "red"))

# Find Steam Library Folders Config
steamLibraryFoldersConfigPath = os.path.join(steamPath, "steamapps", "libraryfolders.vdf")
if not os.path.isfile(steamLibraryFoldersConfigPath):
	sys.exit(colored("错误: Steam Library Config未找到!" + contactInfo, "red"))

with open(steamLibraryFoldersConfigPath, "r", encoding="UTF-8", errors="ignore") as steamLibraryFoldersConfigFile:
	steamLibraryFoldersConfig = vdf.load(steamLibraryFoldersConfigFile, mapper=CaseInsensitiveDict)
	steamLibraryFoldersConfig = steamLibraryFoldersConfig["LibraryFolders"]

# Get Steam Libraries
steamLibraries = []
steamLibraries.append(steamPath) # Default

for configKey in steamLibraryFoldersConfig:
	try:
		int(configKey) # Try to convert it to an int as a test
		configVal = steamLibraryFoldersConfig[configKey]

		# Figure out if this is a string path or assume it's an array
		# Also don't allow duplicates
		configPath = configVal if isinstance(configVal, str) else configVal["path"]
		configPath = os.path.normcase(os.path.realpath(configPath))

		if configPath not in steamLibraries:
			steamLibraries.append(configPath)
	except (FileNotFoundError, ValueError):
		continue

if len(steamLibraries) == 0:
	sys.exit(colored("错误: Steam Libraries 未找到!" + contactInfo, "red"))

print("Steam Libraries:")
print(steamLibraries)

# Find most recent Steam User, which is probably the one they're using/want
steamLoginUsersPath = os.path.join(steamPath, "config", "loginusers.vdf")
if not os.path.isfile(steamLoginUsersPath):
	sys.exit(colored("错误: Steam 用户文件未找到!" + contactInfo, "red"))

steamUser = {"Timestamp": 0}
with open(steamLoginUsersPath, "r", encoding="UTF-8", errors="ignore") as steamLoginUsersFile:
	steamLoginUsers = vdf.load(steamLoginUsersFile, mapper=CaseInsensitiveDict)
	steamLoginUsers = steamLoginUsers["users"]

	for userSteamID64 in steamLoginUsers:
		curSteamUser = steamLoginUsers[userSteamID64]

		if str(steamLoginUsers[userSteamID64]["mostrecent"]) == "1":
			steamUser = {"steamID64": userSteamID64, "AccountName": curSteamUser["AccountName"], "PersonaName": curSteamUser["PersonaName"], "Timestamp": int(curSteamUser["Timestamp"])}
			break
		elif int(steamLoginUsers[userSteamID64]["Timestamp"]) > steamUser["Timestamp"]:
			steamUser = {"steamID64": userSteamID64, "PersonaName": curSteamUser["PersonaName"], "Timestamp": int(curSteamUser["Timestamp"])}

if steamUser["Timestamp"] > 0:
	steamUser["steamID3"] = SteamID(steamUser["steamID64"]).steam3()
	print("\nSteam 当前登录: " + steamUser["PersonaName"] + " (" + steamUser["steamID64"] + " / " + steamUser["steamID3"] + ")")
else:
	sys.exit(colored("错误: 未获取到Steam在线状态，你启动Steam了吗?" + contactInfo, "red"))

# Find GMod
foundGMod = False
gmodPath = ""
possibleGModPaths = [
	["steamapps", "common", "GarrysMod"],
	["steamapps", steamUser["AccountName"], "GarrysMod"]
]
for path in steamLibraries:
	for curGModPath in possibleGModPaths:
		curGModPath = os.path.join(path, *curGModPath)
		if os.path.isdir(curGModPath):
			if foundGMod:
				sys.exit(colored("错误: 侦测到多个GMod安装路径!\n请移除未使用的版本:\n\t" + gmodPath + "\n\t" + curGModPath + contactInfo, "red"))
			else:
				foundGMod = True
				gmodPath = curGModPath

if foundGMod:
	print("\n已找到GMDO:\n" + gmodPath + "\n")
else:
	sys.exit(colored("错误: 未找到GMOD!" + contactInfo, "red"))

# Find GMod Manifest
foundGModManifest = False
gmodManifestPath = ""
gmodManifestStr = ""
possibleGModManifestPaths = [
	["steamapps", "appmanifest_4000.acf"],
	["appmanifest_4000.acf"]
]
for path in steamLibraries:
	for curGModManifestPath in possibleGModManifestPaths:
		curGModManifestPath = os.path.join(path, *curGModManifestPath)
		if os.path.isfile(curGModManifestPath) and os.path.getsize(curGModManifestPath) > 0:
			curGModManifestStr = ""
			with open(curGModManifestPath, "r", encoding="UTF-8", errors="ignore") as gmodManifestFile:
				curGModManifestStr = gmodManifestFile.read().strip().replace("\x00", "")

			if curGModManifestStr:
				if foundGModManifest:
					sys.exit(colored("错误: 查询到多个Garry's Mod Mainifest!\n请移除多余的无效版本:\n\t" + gmodManifestPath + "\n\t" + curGModManifestPath + contactInfo, "red"))
				else:
					foundGModManifest = True
					gmodManifestPath = curGModManifestPath
					gmodManifestStr = curGModManifestStr

if foundGModManifest:
	print("已找到 Garry's Mod Mainifest:\n" + gmodManifestPath + "\n")
else:
	sys.exit(colored("错误: 找不到有效的 Garry's Mod Manifest!" + contactInfo, "red"))

# Get GMod Branch
gmodManifest = vdf.loads(gmodManifestStr, mapper=CaseInsensitiveDict)
gmodBranch = "betakey" in gmodManifest["AppState"]["UserConfig"] and gmodManifest["AppState"]["UserConfig"]["betakey"] or "main"

print("Garry's Mod 版本:\n" + gmodBranch + "\n")

# Make sure GMod is in a good state (fully installed, not updating)
gmodState = gmodManifest["AppState"]["StateFlags"]
if gmodState != "4" or gmodManifest["AppState"]["ScheduledAutoUpdate"] != "0":
	sys.exit(colored("错误: Garry's Mod 还未准备好！\n\t请确保 Garry's Mod 处于可用状态, 未在安装（或更新）, 并且文件未损坏！" + contactInfo, "red"))

print("Garry's Mod 状态:\n" + gmodState + "\n")

# Get GMod's Steam AppInfo
osTypeMap = {
	"win32": "windows",
	"darwin": "macos",
	"linux": "linux"
}

print("正在获取 GMod AppInfo...")

steamAppInfoPath = os.path.join(steamPath, "appcache", "appinfo.vdf")
if not os.path.isfile(steamAppInfoPath):
	sys.exit(colored("错误: Steam AppInfo 文件未找到!" + contactInfo, "red"))

# Get GMod Executable Paths
gmodEXELaunchOptions = []
with open(steamAppInfoPath, "rb") as steamAppInfoFile:
	_, steamAppInfo = parse_appinfo(steamAppInfoFile)

	gmodLaunchConfig = None
	for app in steamAppInfo:
		if app["appid"] == 4000:
			gmodLaunchConfig = app["data"]["appinfo"]["config"]["launch"]
			break

	print("\t平台: " + sys.platform)

	for option in gmodLaunchConfig:
		option = gmodLaunchConfig[option]

		if option["config"]["oslist"] == osTypeMap[sys.platform] and ("betakey" not in option["config"] or option["config"]["betakey"] == gmodBranch):
			pathParts = [os.sep]
			pathParts.extend(gmodPath.replace("\\", "/").split("/"))
			pathParts.extend(option["executable"].replace("\\", "/").split("/"))
			pathParts.insert(2, os.sep)

			print("\t" + os.path.join(*pathParts))

			# os.path.isfile failed sometimes
			try:
				with open(os.path.join(*pathParts), "rb"):
					print("\t\tEXE 已找到")
					gmodEXELaunchOptions.append(option)
			except OSError as e:
				print("\t\t[Errno " + str(e.errno) + "] " + e.strerror)
			except Exception as e:
				print("\t\t" + str(e))

gmodEXELaunchOptionsLen = len(gmodEXELaunchOptions)
if gmodEXELaunchOptionsLen > 0:
	print("侦测到 GMod EXE 启动设置: " + str(gmodEXELaunchOptionsLen) + "\n")
else:
	sys.exit(colored("错误: 无法侦测 GMod EXE 启动设置!" + contactInfo, "red"))

# Get the User Launch Options for GMod
steamUserLocalConfigPath = os.path.join(steamPath, "userdata", steamUser["steamID3"].split(":")[2][:-1], "config", "localconfig.vdf")
if not os.path.isfile(steamUserLocalConfigPath):
	sys.exit(colored("错误: Steam 用户本地文件未找到!" + contactInfo, "red"))

gmodUserLaunchOptions = ""
with open(steamUserLocalConfigPath, "r", encoding="UTF-8", errors="ignore") as steamUserLocalConfigFile:
	steamUserLocalConfig = vdf.load(steamUserLocalConfigFile, mapper=CaseInsensitiveDict)
	steamUserLocalConfig = steamUserLocalConfig["UserLocalConfigStore"]["Software"]["Valve"]["Steam"]
	gmodLocalConfig = steamUserLocalConfig["Apps"]["4000"]
	if "LaunchOptions" in gmodLocalConfig:
		gmodUserLaunchOptions = " " + gmodLocalConfig["LaunchOptions"]

# Some stupid guides include this
if "-nochromium" in gmodUserLaunchOptions:
	print(colored("警告: Garry's Mod 启动项中含有 -nochromium！CEF 将无法继续工作！不过我们仍然会尝试为您修复！\n\t请前往 Steam > Garry's Mod > 属性 > 启动选项 中移除它\n\t此外，如果你安装了 gmod-lua-menu，请卸载它！", "red"))

	secsToContinue = 7
	while secsToContinue:
		print(colored("\t将在 " + str(secsToContinue) + " 秒后继续...", "yellow"), end="\r")
		sleep(1)
		secsToContinue -= 1

	sys.stdout.write("\033[K\n")

# Get CEFCodecFix Manifest
try:
	manifestRequest = requests.get("https://gmodcef-1301161699.cos.ap-beijing.myqcloud.com/GModCefCodecFiles/manifest.json", proxies=systemProxies)

	if manifestRequest.status_code != 200:
		sys.exit(colored("错误: CEFCodecFix Manifest 载入失败（或无法连接至服务器）! 状态码: " + str(manifestRequest.status_code) + contactInfo, "red"))
except Exception as e:
	sys.exit(colored("错误: CEFCodecFix Manifest 载入失败（或无法连接至服务器）! 异常: " + str(e) + contactInfo, "red"))

manifest = manifestRequest.json()

if not sys.platform in manifest:
	sys.exit(colored("错误: 你当前的操作系统不兼容 CEFCodecFix! \n程序即将退出！" + contactInfo, "red"))

if not gmodBranch in manifest[sys.platform]:
	sys.exit(colored("错误: 不支持该 Garry's Mod 的分支! 请将 GMod 切换为 x86-64 测试版后再试" + contactInfo, "red"))
	
# Check File Status
manifest = manifest[sys.platform][gmodBranch]
print("CEFCodecFix Manifest 监测成功!\n正在检索文件列表...")

def getFileSHA256(filePath):
	fileSHA256 = sha256()

	try:
		with open(filePath, "rb") as cefFile:
			while True:
				fileData = cefFile.read(10485760) # Read about 10MB at a time
				if not fileData:
					break
				fileSHA256.update(fileData)
	except Exception as e:
		# Probably some read/write issue
		return False, str(e)

	return True, fileSHA256.hexdigest().upper()

cacheFileFailed = "\n错误: 无法访问 CEFCodecFix 缓存文件.\n请验证 CEFCodecFix 是否有权限访问 CEFCodecFixFiles 文件夹 (请用管理员身份运行)" + contactInfo
gmodFileFailed = "\n错误: 无法访问 Garry's Mod 安装路径.\n请确保 Garry's Mod 已关闭, Steam 没有在更新 Garry's Mod, 并且 CEFCodecFix 有对其文件夹进行修改的能力 (请用管理员身份运行)" + contactInfo
blankFileSHA256 = "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"
filesToWipe = []
filesToUpdate = []
fileNoMatchOriginal = False
def determineFileIntegrityStatus(file):
	global fileNoMatchOriginal
	originalFilePath = os.path.join(gmodPath, file)
	originalFilePath = originalFilePath if os.path.isfile(originalFilePath) else ("NUL" if sys.platform == "win32" else "/dev/null")
	success, fileSHA256OrException = getFileSHA256(originalFilePath)

	if success:
		if fileSHA256OrException != manifest[file]["fixed"]:
			# File needs to be fixed
			if fileSHA256OrException == manifest[file]["original"]:
				# And it matches the original
				filesToUpdate.append(file)
				return True, "\t" + file + ": SHA256通过，等待下载"
			elif manifest[file]["original"] == blankFileSHA256:
				# And it was empty originally, so we're gonna wipe it first
				filesToWipe.append(file)
				filesToUpdate.append(file)
				return True, "\t" + file + ": SHA256校验通过"
			else:
				# And it doesn't match the original...
				# fileNoMatchOriginal = True
				return True, "\t" + file + ": SHA256校验错误（仍将尝试修复）"
		else:
			return True, "\t" + file + ": 检测通过"
	else:
		return False, "\t" + file + ": " + fileSHA256OrException

with ThreadPoolExecutor() as executor:
	for fileIntegrityResultList in executor.map(determineFileIntegrityStatus, manifest):
		success, fileIntegrityResult = fileIntegrityResultList

		if success:
			print(fileIntegrityResult)
		else:
			# Probably some read/write issue
			print(colored(fileIntegrityResult, "yellow"))
			sys.exit(colored(gmodFileFailed, "red"))

# Something's wrong; bail before we break their installation or something
if fileNoMatchOriginal:
	sys.exit(colored("\n错误: 一个或多个文件已损坏（或被修改）\n\t请重新验证 Garry's Mod 游戏完整性!" + contactInfo + "注：出现此条错误时可能代表 GCCF 不适配当前的 GMod 版本，请联系 初雪(微信号：GLXY30) 进行同步更新！", "red"))

if len(filesToUpdate) > 0:
	print("\n正尝试修复文件中...")

	curDir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.normcase(os.path.realpath(__file__)))
	cacheDir = os.path.join(curDir, "GModCEFCodecFixFiles")
	cacheExists = os.path.isdir(cacheDir)

	if not cacheExists:
		os.mkdir(cacheDir)

	for file in filesToUpdate:
		# Download needed patch files to local cache
		cachedFileValid = False
		patchFilePath = os.path.normcase(os.path.realpath(os.path.join(cacheDir, file + ".bsdiff")))

		if cacheExists and os.path.isfile(patchFilePath):
			# Use cached patch files if available, but check the checksums first
			# We don't care about handling an exception here; we'll just overwrite the file
			success, fileSHA256OrException = getFileSHA256(patchFilePath)
			if success and fileSHA256OrException == manifest[file]["patch"]:
				cachedFileValid = True

		if not cachedFileValid:
			patchURL = manifest[file]["patch-url"]
			print("\t下载 > " + patchURL + "...")
			patchURLRequest = requests.get(patchURL, proxies=systemProxies)

			if patchURLRequest.status_code != 200:
				sys.exit(colored("错误: 下载失败 " + file + " | HTTP " + str(patchURLRequest.status_code) + contactInfo, "red"))
			else:
				# Create needed directories if they don't exist already
				os.makedirs(os.path.dirname(patchFilePath), exist_ok = True)
				with open(patchFilePath, "wb") as newCEFPatch:
					newCEFPatch.write(patchURLRequest.content)

	for file in filesToUpdate:
		print("\t校验文件 > " + file + "...")

		originalFilePath = os.path.join(gmodPath, file)
		patchFilePath = os.path.normcase(os.path.realpath(os.path.join(cacheDir, file + ".bsdiff")))
		fixedFilePath = originalFilePath # The original file path might be different from the fixed file path

		# Wipe any original files that need wiping
		if file in filesToWipe:
			try:
				os.remove(originalFilePath)
			except Exception as e:
				# Probably some read/write issue
				print(colored("\t异常 (删除) > " + str(e), "yellow"))
				sys.exit(colored(gmodFileFailed, "red"))

		if not os.path.isfile(originalFilePath):
			print("\t\t文件不存在，跳过...")
			originalFilePath = "NUL" if sys.platform == "win32" else "/dev/null"
 
		# Try and open target files, creating them if they don't exist
		try:
			os.makedirs(os.path.dirname(fixedFilePath), exist_ok = True)
			open(fixedFilePath, "a+b").close()
		except Exception as e:
			print(colored("\t异常 (修复) > " + str(e), "yellow"))
			sys.exit(colored(gmodFileFailed, "red"))

		if os.access(patchFilePath, os.R_OK):
			if not os.access(fixedFilePath, os.W_OK):
				sys.exit(colored(gmodFileFailed, "red"))
		else:
			sys.exit(colored(cacheFileFailed, "red"))

		try:
			file_patch(originalFilePath, fixedFilePath, patchFilePath)
		except Exception as e:
			# Probably some read/write issue
			print(colored("\t异常 > " + str(e), "yellow"))
			sys.exit(colored(gmodFileFailed, "red"))
else:
	print("\n今日风景真不错！")

print(colored("\nCEFCodecFix 成功启动! 启动时间: " + str(round(perf_counter() - timeStart, 4)) + " 秒.", "green"))

if gmodEXELaunchOptionsLen == 1:
	gmodEXESelected = 0

	validShouldLaunch = False
	while validShouldLaunch == False:
		print("\n是否启动 Garry's Mod ? (yes/no)")

		if autoMode is not False:
			print(">>> " + colored("自动模式: yes", "cyan"))

		shouldLaunch = "yes" if autoMode is not False else input(">>> ")
		try:
			shouldLaunch = shouldLaunch.lower()
			if shouldLaunch == "yes" or shouldLaunch == "y":
				validShouldLaunch = True
				shouldLaunch = True
			elif shouldLaunch == "no" or shouldLaunch == "n":
				validShouldLaunch = True
				shouldLaunch = False
			else:
				print("选项无效.")
				autoMode = False
		except ValueError:
			print("选项无效.")
			autoMode = False

	if not shouldLaunch:
		sys.exit()

elif sys.platform == "win32":
	# TODO: Proper multi-EXE selection on Linux and macOS

	validGModEXESelection = False
	while validGModEXESelection == False:
		print("\n请输入你想启动的 Garry's Mod 代号 (使用 CTRL+C 退出):")
		optionNum = 0
		for option in gmodEXELaunchOptions:
			print("\t" + str(optionNum) + " | " + option["description"])
			optionNum += 1

		if autoMode is not False:
			print(">>> " + colored("自动模式: 已选择 " + str(autoMode), "cyan"))

		try:
			gmodEXESelected = autoMode if autoMode is not False else input(">>> ")
			try:
				gmodEXESelected = int(gmodEXESelected)
				if gmodEXESelected < gmodEXELaunchOptionsLen:
					validGModEXESelection = True
				else:
					print("选项无效.")
					autoMode = False
			except ValueError:
				print("选项无效.")
				autoMode = False
		except KeyboardInterrupt:
			sys.exit("程序已退出\n")

print("\n>>> " + colored("正在启动 Garry's Mod:", "green"))

if sys.platform == "win32":
	gmodEXE = os.path.join(gmodPath, gmodEXELaunchOptions[gmodEXESelected]["executable"]) + " " + gmodEXELaunchOptions[gmodEXESelected]["arguments"]
	print(gmodEXE + gmodUserLaunchOptions)
	Popen(gmodEXE + gmodUserLaunchOptions, stdin=None, stdout=None, stderr=None, close_fds=True)
elif sys.platform == "darwin":
	print("open steam://rungameid/4000")
	Popen(["open", "steam://rungameid/4000"], stdin=None, stdout=None, stderr=None, close_fds=True)
else:
	linuxGModLaunchCommand = "xdg-open steam://rungameid/4000 >/dev/null 2>&1 &"
	print(linuxGModLaunchCommand)
	Popen(linuxGModLaunchCommand, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

launchSuccess = True
