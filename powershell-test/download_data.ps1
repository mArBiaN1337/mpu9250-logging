# Script para baixar conteúdo de um servidor web ESP32 e salvar como CSV.

# --- Configuração ---
$IP = "192.168.137.55"
$Port = "80"
$URL = "http://$IP`:$Port"
$OutputFileName = "imu_data_downloaded_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv"

Write-Host "--- Iniciando Download Simples de Dados ---"
Write-Host "URL Alvo: $URL"
Write-Host "Ficheiro de Saída: $OutputFileName"

# --- Lógica Principal Simples (IWR) ---
try {
    # 1. Tenta baixar o conteúdo como texto bruto.
    # Usamos Invoke-WebRequest, que é o comando mais simples.
    # O -UseBasicParsing é importante para ignorar processamento desnecessário.
    $Response = Invoke-WebRequest -Uri $URL -TimeoutSec 10 -UseBasicParsing
    
    # 2. Obtém o conteúdo de texto da resposta.
    # O .Content contém o corpo da resposta (seu CSV), após o PowerShell processar os cabeçalhos.
    $Content = $Response.Content
    
    # 3. Salva o conteúdo no arquivo.
    # Usamos codificação ASCII para máxima compatibilidade com o ESP32.
    $Content | Out-File -FilePath $OutputFileName -Encoding ASCII -Force

    Write-Host "Sucesso! Dados brutos salvos em: $OutputFileName"

}
catch {
    Write-Error "Ocorreu um erro durante o download:"
    Write-Error $_
    Write-Host "Falha ao conectar ou baixar dados de $URL. Verifique o IP/Porta e a conectividade de rede."
    Write-Host "Tente novamente ou reinicie o ESP32."
}
Write-Host "--- Download Finalizado ---"
