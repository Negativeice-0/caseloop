# scripts/test_ollama.ps1
Write-Host "🤖 Testing Local Ollama Connection..." -ForegroundColor Cyan

$body = @{
    model = "llama3"
    prompt = "Say hello to CaseLoop!"
    stream = $false
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method Post -ContentType "application/json" -Body $body
    Write-Host "✅ Success! Ollama Response:" -ForegroundColor Green
    Write-Host $response.response -ForegroundColor Yellow
} catch {
    Write-Host "❌ Error connecting to Ollama: $_" -ForegroundColor Red
}
