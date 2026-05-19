# LHG Mining Dashboard

Este projeto contém o painel analítico da LHG Mining, desenvolvido em Streamlit.

## Estrutura do Projeto

O repositório foi organizado em dois ambientes principais para facilitar o fluxo de trabalho:

- **`desenvolvimento/`**: Ambiente dedicado a testes e novas implementações. Utiliza chaves de API locais (arquivos JSON) para conectar aos serviços do Google.
- **`producao/`**: Ambiente estável, pronto para deploy no Streamlit Cloud. Utiliza os *secrets* nativos do Streamlit (`st.secrets`) para a autenticação.

## Como Executar a Versão de Desenvolvimento

Para rodar a aplicação localmente e testar alterações, siga os passos abaixo:

1. Abra o terminal e ative o seu ambiente virtual (caso possua um).
   ```bash
   source .venv/bin/activate
   ```

2. Navegue até a pasta de desenvolvimento:
   ```bash
   cd desenvolvimento
   ```

3. Execute a aplicação do Streamlit:
   ```bash
   streamlit run app.py
   ```

> **Nota:** Certifique-se de que os arquivos de credenciais necessários existam dentro de `desenvolvimento/json-acesso/` para que o painel consiga ler os dados das planilhas corretamente.

---
Após validar suas mudanças locais na pasta `desenvolvimento`, você poderá replicar os códigos testados na pasta `producao` e submetê-las ao repositório para deploy.
