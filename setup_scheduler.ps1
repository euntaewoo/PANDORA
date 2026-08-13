# ============================================================
# setup_scheduler.ps1 - Windows 작업 스케줄러 등록 스크립트
# 관리자 권한으로 PowerShell 실행 후 이 스크립트를 실행하세요
# 실행: .\setup_scheduler.ps1
# ============================================================

$TaskName    = "Antigravity-HarnessSync"
$PythonPath  = "C:\Users\euntaewoo\AppData\Local\Programs\Python\Python312\python.exe"
$ScriptPath  = "C:\Users\euntaewoo\.agent\harness\harness_sync.py"
$Description = "Antigravity 하네스 파일을 GitHub PANDORA에서 자동 동기화"

# 기존 작업 제거 (있을 경우)
Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

# 트리거: 매일 오전 9시 + PC 시작 시
$TriggerDaily  = New-ScheduledTaskTrigger -Daily -At "09:00AM"
$TriggerBoot   = New-ScheduledTaskTrigger -AtStartup

# 실행 액션
$Action = New-ScheduledTaskAction `
    -Execute $PythonPath `
    -Argument $ScriptPath `
    -WorkingDirectory "C:\Users\euntaewoo\.agent\harness"

# 설정: 네트워크 연결 시에만 실행, 배터리 무관
$Settings = New-ScheduledTaskSettingsSet `
    -RunOnlyIfNetworkAvailable `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

# 작업 등록
Register-ScheduledTask `
    -TaskName    $TaskName `
    -Description $Description `
    -Trigger     @($TriggerDaily, $TriggerBoot) `
    -Action      $Action `
    -Settings    $Settings `
    -RunLevel    Highest `
    -Force

Write-Host ""
Write-Host "✅ 작업 스케줄러 등록 완료!"
Write-Host "   작업명: $TaskName"
Write-Host "   실행 시점: PC 시작 시 + 매일 오전 9시"
Write-Host "   로그 파일: C:\Users\euntaewoo\.agent\harness\sync_log.txt"
