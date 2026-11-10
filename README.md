# config-check

![CI](https://github.com/diassdeveloper/config-check/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/diassdeveloper/config-check/actions/workflows/cd.yml/badge.svg)

Validador de arquivos de configuração `.json` e `.yaml`. Ele varre uma pasta,
confere cada arquivo contra regras de campos e tipos, gera um relatório em JSON
e CSV e termina com um código de saída que serve de gatilho para pipelines de CI.

## Como funciona

1. Encontra todos os arquivos `.json`, `.yaml` e `.yml` da pasta e das subpastas.
2. Lê cada arquivo (arquivo vazio ou com sintaxe quebrada vira um erro no relatório).
3. Valida os campos obrigatórios e seus tipos, segundo um arquivo de regras.
4. Escreve `report.json` e `report.csv`.
5. Sai com `0`, `1` ou `2` conforme o resultado.

## Instalação

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

## Uso

```powershell
python -m config_check examples/ok --rules rules.yaml
```

| Argumento | Descrição |
|---|---|
| `directory` | Pasta com os arquivos de configuração |
| `--rules` | Arquivo YAML com as regras (obrigatório) |
| `--output` | Pasta do relatório (padrão: `reports`) |

Mantenha o arquivo de regras **fora** da pasta analisada, senão ele valida a si mesmo.

### Arquivo de regras

Cada linha diz o nome de um campo obrigatório e o tipo esperado.
Tipos aceitos: `int`, `str`, `bool`, `list`, `dict`.

```yaml
port: int
debug: bool
```

Um `bool` (`true`/`false`) não é aceito onde se espera `int`.

### Códigos de saída

| Código | Significado |
|---|---|
| `0` | Todos os arquivos são válidos |
| `1` | Pelo menos um arquivo é inválido ou ilegível |
| `2` | Erro de uso (pasta inexistente ou regras inválidas) |

### Relatório

`report.json`:

```json
{
  "total": 1,
  "with_errors": 1,
  "files": [
    {
      "file": "examples/bad/app.yaml",
      "ok": false,
      "errors": [
        "campo 'port' deve ser do tipo int",
        "campo obrigatório ausente: debug"
      ]
    }
  ]
}
```

`report.csv` tem as colunas `file`, `status` e `error`, com uma linha por erro.

## Docker

```powershell
docker build -t config-check .
docker run --rm `
  -v ${PWD}/examples/ok:/data/configs `
  -v ${PWD}/rules.yaml:/data/rules.yaml `
  -v ${PWD}/reports:/reports `
  config-check /data/configs --rules /data/rules.yaml --output /reports
```

As pastas são montadas por volume: o container lê as configs e escreve o relatório
direto na sua máquina. Em Linux ou macOS, troque `${PWD}` por `$(pwd)`.

## Desenvolvimento

```powershell
pytest
ruff check .
```

## CI

O workflow `.github/workflows/ci.yml` roda a cada push na `main` e em pull requests:
lint com `ruff`, testes com `pytest` e uma execução real da ferramenta sobre
`examples/ok`. Se qualquer etapa falhar, o pipeline fica vermelho.

## CD

O workflow `.github/workflows/cd.yml` é acionado quando uma tag de versão no formato `v*.*.*` é enviada ao GitHub (por exemplo, `v0.2.2`). Primeiro, ele executa o workflow de CI reutilizável; o job de publicação só continua se o CI terminar com sucesso (`needs: ci`).

Depois, o pipeline constrói a imagem Docker e publica no GitHub Container Registry (GHCR), usando a versão da tag (sem o prefixo `v`, por exemplo, `0.2.2`) e também a tag `latest`. Assim, cada release bem-sucedida disponibiliza uma nova versão da imagem para uso.

## Estrutura

```
config_check/
├── finder.py     # acha os arquivos de configuração
├── loader.py     # lê JSON/YAML e trata arquivo vazio ou quebrado
├── validator.py  # confere campos e tipos
├── rules.py      # lê o arquivo de regras
├── report.py     # escreve os relatórios JSON e CSV
└── cli.py        # argumentos e código de saída
tests/            # testes com pytest
examples/         # configs de exemplo (ok e bad)
```
