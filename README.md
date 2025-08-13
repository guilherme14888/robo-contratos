# Robo Contratos

Interface web simples para iniciar o robô de automação e receber o resultado em PDF.

## Requisitos

- Python 3.9+
- [Flask](https://flask.palletsprojects.com/)
- Dependências do script `robocontratos.py` (Selenium, etc.)

Instale as dependências com:

```bash
pip install flask
```

## Executando

```bash
python app.py
```

Acesse `http://localhost:5000` no navegador e escolha **CNVW** ou **FIAT**.
Digite o valor desejado e clique em **Enviar** para que o robô execute o
`robocontratos.py` e disponibilize o PDF gerado para download.
