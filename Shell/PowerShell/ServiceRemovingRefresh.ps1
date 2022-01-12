<#
**** Refresh windows removing service,and stop its process.
**** Programmer:Harold.Duan
**** Date:20220111
**** Reason:Refreshing removing service.
#>
function Read-InputBoxDialog([string]$Message, [string]$WindowTitle, [string]$DefaultText)
{
    Add-Type -AssemblyName Microsoft.VisualBasic
    return [Microsoft.VisualBasic.Interaction]::InputBox($Message, $WindowTitle, $DefaultText)
}

# Get the service name by console input
$srvc_name = Read-InputBoxDialog "Please input the removing service name..." "Service Name" "ServiceTest"
Write-Output "You input service name is $srvc_name!"

# Get the service object search by service name
$srvc = Get-WmiObject -Class Win32_Service | Where-Object {$_.Name –eq $srvc_name}

# Service object is not exists
if(!($srvc)){
    Write-Output "Can not find the removing service [$srvc_name]'s PID!"
}else{
    # Get the service object process id
    # Write-Output $srvc.ProcessId
    $srvc_pid = $srvc.ProcessId
    Write-Output "Get the removing service [$srvc_name]'s PID is $srvc_pid!"
    Write-Output "Stopping the removing service's process..."
    # Stopping the process by PID
    Stop-Process -Id $srvc_pid
    Write-Output "Refresh removing service is done!"
}