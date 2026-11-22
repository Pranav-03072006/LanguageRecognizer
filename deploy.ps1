# Quick Deployment Helper for GitHub & Vercel
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  PolyGlot AI - Deploy to GitHub & Vercel " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Check if origin remote is set
$remote = git remote get-url origin 2>$null
if (-not $remote) {
    git remote add origin "https://github.com/Pranav-03072006/LanguageRecognizer.git"
    Write-Host "[✓] Added origin: https://github.com/Pranav-03072006/LanguageRecognizer.git" -ForegroundColor Green
}

Write-Host "`nStep 1: Pushing to GitHub (https://github.com/Pranav-03072006/LanguageRecognizer)..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[✓] Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "`nStep 2: Deploying to Vercel..." -ForegroundColor Yellow
    Write-Host "Option A: Go to https://vercel.com/new and import 'LanguageRecognizer' (Automated CI/CD)" -ForegroundColor Cyan
    Write-Host "Option B: Running Vercel CLI login & deploy:" -ForegroundColor Cyan
    vercel
} else {
    Write-Host "`n[!] Push failed. Please ensure the repository 'LanguageRecognizer' exists on GitHub at:" -ForegroundColor Red
    Write-Host "    https://github.com/new (Repository name: LanguageRecognizer)" -ForegroundColor Yellow
}
