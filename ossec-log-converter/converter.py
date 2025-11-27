import re
import pandas as pd
import os
import sys

def parse_ossec_log(file_path):
    print(f"Processando: {file_path}...")
    
    # Lista para guardar os alertas processados
    alerts_data = []
    
    # Dicionário temporário para o alerta atual
    current_alert = {}
    
    # Padrões de Regex (Expressões Regulares) para capturar os dados
    # Captura: ** Alert 1732665662.3456: - win,system,error,
    re_header = re.compile(r'\*\* Alert (\d+\.\d+):\s*-(.*)')
    
    # Captura: 2024 Nov 27 00:01:02 (Agent) IP->Log
    re_date_agent = re.compile(r'(\d{4}\s\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s\((.*?)\)\s(.*)')
    
    # Captura: Rule: 18103 (level 5) -> 'Descrição'
    re_rule = re.compile(r'Rule: (\d+) \(level (\d+)\)\s->\s\'(.*?)\'')
    
    # Captura campos genéricos chave: valor (ex: User: Admin)
    re_field = re.compile(r'(\w+):\s+(.*)')

    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 1. Início de um novo alerta
            if line.startswith('** Alert'):
                # Se já existe um alerta sendo processado, salva ele antes de começar o novo
                if current_alert:
                    alerts_data.append(current_alert)
                
                # Reseta para o novo alerta
                current_alert = {
                    'Timestamp_Unix': None,
                    'Groups': None,
                    'Date_Time': None,
                    'Agent': None,
                    'Log_Source': None,
                    'Rule_ID': None,
                    'Level': None,
                    'Description': None,
                    'Full_Log': []
                }
                
                match = re_header.match(line)
                if match:
                    current_alert['Timestamp_Unix'] = match.group(1)
                    current_alert['Groups'] = match.group(2).strip()
                continue

            # Se não começamos um alerta ainda, ignora linhas soltas no topo
            if not current_alert:
                continue

            # 2. Linha de Data e Agente
            match_date = re_date_agent.match(line)
            if match_date:
                current_alert['Date_Time'] = match_date.group(1)
                current_alert['Agent'] = match_date.group(2)
                current_alert['Log_Source'] = match_date.group(3)
                continue

            # 3. Linha da Regra (Rule)
            match_rule = re_rule.match(line)
            if match_rule:
                current_alert['Rule_ID'] = match_rule.group(1)
                current_alert['Level'] = int(match_rule.group(2))
                current_alert['Description'] = match_rule.group(3)
                continue

            # 4. Campos específicos (User, SrcIP, etc) ou Log Bruto
            # Vamos tentar extrair campos chave: valor
            match_field = re_field.match(line)
            if match_field:
                key = match_field.group(1)
                value = match_field.group(2)
                # Adiciona como coluna dinâmica
                current_alert[key] = value
            else:
                # Se não for nada acima, é parte da mensagem bruta do log
                current_alert['Full_Log'].append(line)

        # Adiciona o último alerta do arquivo
        if current_alert:
            alerts_data.append(current_alert)

        # Criação do DataFrame
        df = pd.DataFrame(alerts_data)
        
        # Limpeza final: Junta a lista de logs em uma string única
        if 'Full_Log' in df.columns:
            df['Full_Log'] = df['Full_Log'].apply(lambda x: ' | '.join(x) if isinstance(x, list) else x)

        # Converter colunas de data para formato datetime real (Ajuda muito o Power BI)
        if 'Date_Time' in df.columns:
            df['Date_Time'] = pd.to_datetime(df['Date_Time'], errors='coerce')

        return df

    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")
        return None

# --- Bloco Principal ---
if __name__ == "__main__":
    # Verifica se o arquivo foi passado via "arrastar e soltar" em cima do script
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # Se abriu o script direto, pede o caminho
        input_file = input("Arraste o arquivo .log aqui e dê Enter (ou digite o caminho): ").strip().strip('"')

    if os.path.exists(input_file):
        df_result = parse_ossec_log(input_file)
        
        if df_result is not None:
            # Gera nome do arquivo de saída
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_PowerBI.xlsx"
            
            # Salva em Excel (melhor para Power BI que CSV por causa de quebras de linha)
            df_result.to_excel(output_file, index=False)
            
            print(f"\nSucesso! Arquivo criado: {output_file}")
            print("Agora basta importar este Excel no Power BI.")
    else:
        print("Arquivo não encontrado.")
    
    input("\nPressione Enter para sair...")