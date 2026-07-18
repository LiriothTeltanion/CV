param()

$ErrorActionPreference = 'Stop'

$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$source = (Resolve-Path -LiteralPath (Join-Path $root 'assets\social\cv-social-preview.svg')).Path
$output = Join-Path $root 'assets\social\cv-social-preview.png'
$edgeCandidates = @(
    'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    'C:\Program Files\Microsoft\Edge\Application\msedge.exe'
)
$edge = $edgeCandidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1

if (-not $edge) {
    throw 'Microsoft Edge was not found. Install Edge or render the 1280 x 640 SVG with another standards-compliant browser.'
}

$profile = Join-Path ([System.IO.Path]::GetTempPath()) ('kevin-cv-social-render-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $profile | Out-Null

try {
    $uri = [System.Uri]::new($source).AbsoluteUri
    $arguments = @(
        '--headless',
        '--disable-gpu',
        '--disable-crash-reporter',
        '--hide-scrollbars',
        '--force-device-scale-factor=1',
        '--window-size=1280,640',
        "--user-data-dir=$profile",
        "--screenshot=$output",
        $uri
    )
    $process = Start-Process -FilePath $edge -ArgumentList $arguments -Wait -PassThru -WindowStyle Hidden
    if ($process.ExitCode -ne 0) {
        throw "Edge rendering failed with exit code $($process.ExitCode)."
    }
    if (-not (Test-Path -LiteralPath $output -PathType Leaf)) {
        throw "The PNG was not created: $output"
    }
    Write-Host "[OK] Rendered $output"
} finally {
    if (Test-Path -LiteralPath $profile) {
        $resolvedProfile = (Resolve-Path -LiteralPath $profile).Path
        $resolvedTemp = (Resolve-Path -LiteralPath ([System.IO.Path]::GetTempPath())).Path.TrimEnd('\')
        if ($resolvedProfile.StartsWith($resolvedTemp + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
            Remove-Item -LiteralPath $resolvedProfile -Recurse -Force
        }
    }
}
