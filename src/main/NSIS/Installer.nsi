!include MUI2.nsh
!include FileFunc.nsh

;--------------------------------
;Perform Machine-level install, if possible

!define MULTIUSER_EXECUTIONLEVEL Highest
;Add support for command-line args that let uninstaller know whether to
;uninstall machine- or user installation:
!define MULTIUSER_INSTALLMODE_COMMANDLINE
!include MultiUser.nsh
!include LogicLib.nsh

Function .onInit
  !insertmacro MULTIUSER_INIT
  ;Do not use InstallDir at all so we can detect empty $InstDir!
  ${If} $InstDir == "" ; /D not used
      ${If} $MultiUser.InstallMode == "AllUsers"
          StrCpy $InstDir "C:\%{app_name}-v%{version}"
      ${Else}
          StrCpy $InstDir "$LOCALAPPDATA\%{app_name}"
      ${EndIf}
  ${EndIf}
FunctionEnd

Function un.onInit
  !insertmacro MULTIUSER_UNINIT
FunctionEnd

;--------------------------------
;General

  Name "%{app_name}"
  OutFile "..\%{installer}"

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Pages

  !define MUI_WELCOMEPAGE_TEXT "This wizard will guide you through the installation of %{app_name} v%{version}.$\r$\n$\r$\nImportant:$\r$\nWhen chosing the installation directory, make sure that you do not overwrite any previous versions. Remove them or use another folder for installation.$\r$\nCurrenty, no spaces in the installation path are allowed.$\r$\n$\r$\nClick Next to continue."
  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
    !define MUI_FINISHPAGE_NOAUTOCLOSE
    !define MUI_FINISHPAGE_RUN
    !define MUI_FINISHPAGE_RUN_CHECKED
    !define MUI_FINISHPAGE_RUN_TEXT "Run %{app_name}"
    !define MUI_FINISHPAGE_RUN_FUNCTION "LaunchLink"
  !insertmacro MUI_PAGE_FINISH

  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

!define UNINST_KEY \
  "Software\Microsoft\Windows\CurrentVersion\Uninstall\%{app_name}"
Section
  SetOutPath "$InstDir"
  File /r "..\%{app_name}\*"
  WriteRegStr SHCTX "Software\%{app_name}" "" $InstDir
  WriteRegStr SHCTX "Software\%{app_name}" "Version" "%{version}"
  WriteUninstaller "$InstDir\uninstall.exe"
;create desktop shortcut
  CreateShortCut "$DESKTOP\%{app_name}.lnk" "$InstDir\%{app_name}.exe" ""

;create start-menu items
  CreateDirectory "$SMPROGRAMS\%{app_name}"
  CreateShortCut "$SMPROGRAMS\%{app_name}.lnk" "$InstDir\%{app_name}.exe"
 
;write uninstall information to the registry
  WriteRegStr SHCTX "${UNINST_KEY}" "DisplayName" "%{app_name}"
  WriteRegStr SHCTX "${UNINST_KEY}" "UninstallString" \
    "$\"$InstDir\uninstall.exe$\" /$MultiUser.InstallMode"
  WriteRegStr SHCTX "${UNINST_KEY}" "QuietUninstallString" \
    "$\"$InstDir\uninstall.exe$\" /$MultiUser.InstallMode /S"
  WriteRegStr SHCTX "${UNINST_KEY}" "Publisher" "%{author}"
  WriteRegStr SHCTX "${UNINST_KEY}" "DisplayVersion" "%{version}"
  ${GetSize} "$InstDir" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD SHCTX "${UNINST_KEY}" "EstimatedSize" "$0"

SectionEnd

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  RMDir /r "$InstDir"

;Delete Shortcuts
  Delete "$DESKTOP\%{app_name}.lnk"
  Delete "$SMPROGRAMS\%{app_name}\*.*"
  RmDir  "$SMPROGRAMS\%{app_name}"
  
  DeleteRegKey /ifempty SHCTX "Software\%{app_name}"
  DeleteRegKey SHCTX "${UNINST_KEY}"

SectionEnd

Function LaunchLink
  !addplugindir "."
  ShellExecAsUser::ShellExecAsUser "open" "$SMPROGRAMS\%{app_name}.lnk"
FunctionEnd