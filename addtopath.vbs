' Add to system path persistently
' NOTE: This script is designed to preserve the existing path, in contrast to
' using something like setx where you only have access to the expanded PATH
' over both system and user environment variables. This script will modify
' the system path environment, preserving nested environment variables.

Set wshShell = CreateObject( "WScript.Shell" )
if WScript.Arguments.Named.Exists("user") then
    Set wshEnv = wshShell.Environment("USER")
    env = "user"
else
    Set wshEnv = wshShell.Environment( "SYSTEM" )
    env = "system"
end if

newpaths = ""

syspaths = Split(wshEnv("PATH"), ";")
for each x in syspaths
    if newpaths = "" then
        newpaths = x
    else
        newpaths = newpaths & ";" & x
    end if
next

addedpaths = ""
for i = 0 to WScript.Arguments.Unnamed.Count - 1
    exists = false
	for each x in syspaths
	    if x = WScript.Arguments.Unnamed.Item(i) then
	        exists = true
	    end if
	next
	
	if exists = false then	    
		newpaths = newpaths & ";" & WScript.Arguments.Unnamed.Item(i)
		if addedpaths = "" then
			addedpaths = WScript.Arguments.Unnamed.Item(i)
		else
			addedpaths = addedpaths & "; " & WScript.Arguments.Unnamed.Item(i)
		end if
	end if
next

if addedpaths <> "" then
	WScript.Echo "Added " & addedpaths & " to " & env & " path"
	wshEnv("PATH") = newpaths
end if