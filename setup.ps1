Write-Host ""
Write-Host "===================================="
Write-Host " School Check Automation"
Write-Host "===================================="
Write-Host ""

$folders = @(
"src",
"src\pages",
"src\services",
"src\database",
"src\models",
"src\utils",
"src\config",
"data",
"data\cache",
"data\exports",
"tests"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
}

$files = @(
"src\__init__.py",
"src\pages\__init__.py",
"src\services\__init__.py",
"src\database\__init__.py",
"src\models\__init__.py",
"src\utils\__init__.py",
"src\config\__init__.py"
)

foreach ($file in $files) {
    if (!(Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
    }
}

Write-Host "Project structure is ready."
Write-Host ""
tree /F
