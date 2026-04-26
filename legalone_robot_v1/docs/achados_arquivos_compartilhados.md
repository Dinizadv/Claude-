# Achados dos arquivos compartilhados

## 1. Configurações JSON atuais
Os arquivos de configuração compartilhados contêm:
- usuário
- senha
- três URLs de relatórios no domínio `ballao.novajus.com.br`

As credenciais **não** foram reproduzidas neste documento.

Foi identificado que os relatórios apontam para:
- TimeSheet GenericReport
- processos GenericReport
- contratos/ContratoHonorarioGenericReport

## 2. Executável atual
O executável `roboWeb.exe` contém referência a `selenium`, o que indica fortemente que o robô atual foi empacotado em Python com PyInstaller e usa automação de navegador.

## 3. Workbook “Gerenciador de revisão de horas 30042025.xlsm”
Planilhas identificadas:
- ROTINAS
- COLABORADORES
- TABELAS
- CONFIGURAÇÕES
- Geral
- Work1 ROTINAS
- Work2 COLABORADORES
- BD COLABORADORES

Pontos relevantes:
- configuração de links L1, L2 e L3 dentro da própria planilha;
- modelo de geração por fases;
- tabela de colaboradores e regras de disparo;
- forte indício de integração com revisões e comunicações internas.

## 4. Workbook “F0 Tabelas e Timesheet.xlsm”
Planilhas identificadas:
- Instruções
- AtuColabs
- ImpNegL1
- TabsGeral
- TabsNegocia
- ImpTSheet L1
- TimeSheet
- Roteiros

Campos centrais observados em `ImpTSheet L1` e `TimeSheet`:
- ID
- Cliente Principal
- Negociação
- Descrição negociação
- Pasta
- Nome da Pasta
- Data de início
- Duração
- Executante
- Tipo | Subtipo
- Descrição
- Cobrável
- Obs do Executante
- Gerente de conta
- Grupo

Esses campos são bons candidatos para a camada de entrada do lançador determinístico.

## 5. Implicação prática
Os arquivos já existentes permitem montar a V1 do robô em torno de três camadas:
1. planilha de entrada normalizada;
2. validador determinístico;
3. executor Selenium.

O ponto ainda não inferível apenas pelos arquivos é o mapeamento confiável dos seletores HTML da tela de criação/edição da hora trabalhada. Isso exige uma captura da tela real ou inspeção do DOM.
