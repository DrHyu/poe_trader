#NoEnv ; Recommended for performance and compatibility with future AutoHotkey releases.

#Warn ; Recommended for catching common errors.

SendMode Input ; Recommended for new scripts due to its superior speed and reliability.

SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.



; While CapsLock is toggled On

; Script will display Mouse Position (coordinates) as a tooltip at Top-Left corner of screen.

; Also allows to copy them (to clipboard) with a PrintScreen button.



#SingleInstance force ; only one instance of script can run

#Persistent ; to make it run indefinitely

settimer start1, 10 ; "0" to make it update position instantly

xx := 0
yy := 0

start1:
	global xx
	global yy
	
	MouseGetPos xx, yy ; get mouse x and y position, store as %xx% and %yy%
	
	if !GetKeyState("capslock","T") ; whether capslock is on or off
	{
		tooltip ; if off, don't show tooltip at all.
	}
	else
	{ ; if on
		CoordMode, ToolTip, Screen ; makes tooltip to appear at position, relative to screen.

		CoordMode, Mouse, Screen ; makes mouse coordinates to be relative to screen.


		tooltip %xx% %yy%, 0, 0 ; display tooltip of %xx% %yy% at coordinates x0 y0.
	}
Return

$f5::
	Clipboard = 
	Return

$f6:: ; assign new function to PrintScreen. If pressed...
	global xx
	global yy
	new_pos = [%xx%, %yy%], ; ...store %xx% %yy% to clipboard.
	clipboard = %clipboard%`r`n%new_pos%

return

$f12::
	Reload