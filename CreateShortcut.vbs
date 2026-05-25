' CreateShortcut.vbs
' Run this ONCE to create a desktop shortcut for FaceVault.
' After running, you'll have a "FaceVault" icon on your Desktop.

Dim shell, fso, scriptDir, desktop, shortcut, vbsPath

Set shell     = CreateObject("WScript.Shell")
Set fso       = CreateObject("Scripting.FileSystemObject")
scriptDir     = fso.GetParentFolderName(WScript.ScriptFullName)
desktop       = shell.SpecialFolders("Desktop")
vbsPath       = scriptDir & "\FaceVault.vbs"

Set shortcut              = shell.CreateShortcut(desktop & "\FaceVault.lnk")
shortcut.TargetPath       = vbsPath
shortcut.WorkingDirectory = scriptDir
shortcut.Description      = "FaceVault — Local Face Recognition"
shortcut.IconLocation     = "shell32.dll,13"   ' camera-like icon from Windows
shortcut.Save()

MsgBox "✅ FaceVault shortcut created on your Desktop!" & Chr(13) & Chr(13) & _
       "Double-click 'FaceVault' on your Desktop to launch.", _
       64, "FaceVault — Shortcut Created"
