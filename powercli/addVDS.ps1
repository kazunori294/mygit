Param(
	[Parameter(Mandatory=$True)][string]$vc,
	[Parameter(Mandatory=$True)][string]$targethostname,
	[Parameter(Mandatory=$True)][string]$vdstype,
	[Parameter(Mandatory=$True)][string]$user	
)

$vi = Connect-VIserver -Server $vc -User $user -Password xxxx

$esx = Get-VMHost -Name $targethostname

$pnics = $esx.ExtensionData.Config.Network.pnic
$vsws = $esx.ExtensionData.Config.Network.vswitch
$dvsws = $esx.ExtensionData.Config.Network.proxyswitch

foreach ($pnic in $pnics){
	$frag = 0
	foreach ($vsw in $vsws){
		$vsw_pnics = $vsw.pnic
		foreach ($vsw_pnic in $vsw_pnics){
			if($pnic.key -eq $vsw_pnic){
				$frag = 1
			}
			else{		
				foreach ($dvsw in $dvsws){
					$dvsw_pnics = $dvsw.pnic
					foreach ($dvsw_pnic in $dvsw_pnics){
						if($pnic.key -eq $dvsw_pnic){
							$frag = 1
						}
					}
				}
			}
		}
	}
	if($frag -eq 0){
		$vmhostNetworkAdapter = $esx | Get-VMHostNetworkAdapter -Physical -Name $pnic.device
		if($vdstype -eq "admin"){
			$targetvds = Get-VDSwitch -Name admin*
			$esxvds = $esx | Get-VDSwitch -Name admin*
		}
		elseif($vdstype -eq "service"){
			$targetvds = Get-VDSwitch -Name cloud*
			$esxvds = $esx | Get-VDSwitch -Name cloud*
		}
		if($esxvds -eq $null){
			$targetvds | Add-VDSwitchVMHost -VMHost $esx -Confirm:$false
		}
		$targetvds | Add-VDSwitchPhysicalNetworkAdapter -VMHostNetworkAdapter $vmhostNetworkAdapter -Confirm:$false
		Write-Host $pnic.device on $esx.Name Connected to $targetvds.Name		
	}
	else{
		Write-Host $pnic.device on $esx.Name is already used
	}
}

Disconnect-VIserver -Confirm:$false
