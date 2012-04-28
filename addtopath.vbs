' Add to system path persistently
' NOTE: This script is designed to preserve the existing path, in contrast to
' using something like setx where you only have access to the expanded PATH
' over both system and user environment variables. This script will modify
' the system path environment, preserving nested environment variables.

Set wshShell = CreateObject( "WScript.Shell" )
Set wshSystemEnv = wshShell.Environment( "SYSTEM" )
newpaths = ""

syspaths = Split(wshSystemEnv("PATH"), ";")
for each x in syspaths
    if newpaths = "" then
        newpaths = x
    else
        newpaths = newpaths & ";" & x
    end if
next

addedpaths = ""
for i = 0 to WScript.Arguments.Unnamed.Count - 1
    newpaths = newpaths & ";" & WScript.Arguments.Unnamed.Item(i)
    if addedpaths = "" then
        addedpaths = WScript.Arguments.Unnamed.Item(i)
    else
        addedpaths = addedpaths & "; " & WScript.Arguments.Unnamed.Item(i)
    end if
next

WScript.Echo "Added " & addedpaths & " to system path"
wshSystemEnv("PATH") = newpaths
