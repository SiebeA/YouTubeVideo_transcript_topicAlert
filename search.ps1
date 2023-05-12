param (
    [Parameter(Mandatory = $true)]
    [string]$Pattern,
    [string]$Directory = (Get-Location)
)

$ContextLength = 200  # Number of characters around the match
$LogFile = "search_logs.txt"  # Log file path

# Get the absolute path of the directory
$Directory = Convert-Path $Directory

# Check if the directory exists
if (-not (Test-Path $Directory -PathType Container)) {
    Write-Host "Invalid directory path."
    exit
}

# Get all text files in the directory and subdirectories
$Files = Get-ChildItem -Path $Directory -Filter "*.txt" -Recurse

# Iterate over the text files
foreach ($File in $Files) {
    $FilePath = $File.FullName
    $Content = Get-Content -Path $FilePath -Raw

    # Search for the pattern in the file contents
    $Matches = [regex]::Matches($Content, $Pattern)

    if ($Matches.Count -gt 0) {
        Write-Host "`nPattern found in file: $FilePath"
        $Matches | ForEach-Object {
            $StartIndex = $_.Index - $ContextLength
            if ($StartIndex -lt 0) { $StartIndex = 0 }
            $EndIndex = $_.Index + $_.Length + $ContextLength
            if ($EndIndex -gt $Content.Length) { $EndIndex = $Content.Length }

            $Context = $Content.Substring($StartIndex, $EndIndex - $StartIndex)

            # Log the match and context
            Add-Content -Path $LogFile -Value "Match: $($_.Value)"
            Add-Content -Path $LogFile -Value "Context:"
            Add-Content -Path $LogFile -Value $Context
            Add-Content -Path $LogFile -Value ""

            Write-Host "Match: $($_.Value)"
            Write-Host "Context:"
            Write-Host $Context
            Write-Host ""
        }
    }
    else {
        Write-Host "Pattern not found in file: $FilePath"
    }
}
