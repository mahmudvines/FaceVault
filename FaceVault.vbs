' FaceVault.vbs
' Double-click this to launch FaceVault with ZERO visible windows.
' It finds pythonw.exe (the no-console Python) and runs launcher.pyw silently.

Dim shell, fso, scriptDir, pythonw, launcher

Set shell     = CreateObject("WScript.Shell")
Set fso       = CreateObject("Scripting.FileSystemObject")
scriptDir     = fso.GetParentFolderName(WScript.ScriptFullName)
launcher      = scriptDir & "\launcher.pyw"

' Try pythonw.exe locations (no console window version of Python)
Dim candidates(6)
candidates(0) = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python311\pythonw.exe"
candidates(1) = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python312\pythonw.exe"
candidates(2) = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python310\pythonw.exe"
candidates(3) = "C:\Python311\pythonw.exe"
candidates(4) = "C:\Python312\pythonw.exe"
candidates(5) = "C:\Python310\pythonw.exe"
candidates(6) = "pythonw"

pythonw = ""
Dim i
For i = 0 To 6
    If fso.FileExists(candidates(i)) Then
        pythonw = candidates(i)
        Exit For
    End If
Next

' Fallback: try pythonw from PATH
If pythonw = "" Then
    pythonw = "pythonw"
End If

' Launch silently (0 = hidden window, False = don't wait)
shell.Run """" & pythonw & """ """ & launcher & """", 0, False
