# Dashboard de Estatística — Conjuntos LEGO

Front-end interativo (Streamlit + Apache ECharts) do trabalho de Estatística.
Este diretório é **autossuficiente**: tem o código, as dependências e o dataset.

```
frontend/
├── app.py                     # o dashboard
├── requirements.txt           # dependências
├── .streamlit/config.toml     # tema (cores LEGO)
└── base_de_dados/
    └── lego_sets.csv          # dataset (Maven Analytics)
```

## Rodar no seu computador

```bash
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

Abre em `http://localhost:8501`.

---

## Publicar na internet (para a professora só abrir um link)

> **Sobre a Vercel:** a Vercel é feita para sites estáticos e funções curtas.
> O Streamlit precisa de um servidor sempre ligado com WebSocket, então **não
> roda na Vercel**. A opção equivalente, gratuita e oficial para Streamlit é o
> **Streamlit Community Cloud** — a professora recebe um link `https://...` e
> não instala nada.

### Passo a passo (Streamlit Community Cloud)

1. Suba este projeto para um repositório no **GitHub** (público ou privado).
2. Acesse <https://share.streamlit.io> e entre com a conta do GitHub.
3. Clique em **"Create app"** / **"Deploy a public app from GitHub"**.
4. Preencha:
   - **Repository:** `seu-usuario/Data_Analytics_LEGO`
   - **Branch:** `main`
   - **Main file path:** `frontend/app.py`
5. Clique em **Deploy**. Em ~2 minutos o app fica no ar.
6. Copie a URL (algo como `https://data-analytics-lego.streamlit.app`) e envie
   para a professora.

O Streamlit Cloud instala sozinho o que está em `requirements.txt` (na raiz do
repositório ou ao lado do `app.py`).

### Alternativas (também com servidor Python, não Vercel)

| Serviço | Observação |
|---|---|
| **Render** (render.com) | plano free; comando de start: `streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0` |
| **Railway** (railway.app) | mesmo comando de start |
| **Hugging Face Spaces** | escolher o SDK "Streamlit" ao criar o Space |
