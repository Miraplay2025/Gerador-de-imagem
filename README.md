# 🧬 Visual Station Pro v4.0 (Open Source Engine)

Interface de geração de imagens de alta fidelidade com **Persistência de Personagem (ID-Lock)** rodando via Google Colab com SDXL Turbo.

## 🚀 Como Colocar o Sistema Online

Siga exatamente estes 3 passos:

### 1. Iniciar o Motor (GPU)
Clique no botão abaixo para abrir o servidor no Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Miraplay2025/Gerador-de-imagem/blob/main/visual_engine.ipynb)

* Dentro do Colab, vá em **Ambiente de Execução** > **Alterar tipo de ambiente** e verifique se **GPU T4** está selecionada.
* Clique em **Executar Tudo** (ícone de Play em cada célula).
* Role até o final da página e procure por um link parecido com: `https://xxxx.lhr.life`. **Copie este link.**

### 2. Acessar a Interface
Abra o site que você hospedou (via GitHub Pages ou localmente):
👉 [Acesse seu arquivo index.html aqui]

### 3. Conectar
No topo da página do gerador, cole a URL que você copiou do Colab no campo **"URL do Colab"**. O status mudará para **ONLINE** e você já pode gerar imagens.

---

## 🛠️ Funcionalidades
* **Banco Visual:** Adicione imagens de referência e nomeie personagens para manter a consistência facial.
* **SDXL Turbo:** Geração ultrarrápida (2 a 4 segundos por imagem).
* **Sem CORS:** Configurado para aceitar requisições de qualquer domínio.
* **Mobile First:** Interface totalmente responsiva para criar pelo celular.

## 📁 Estrutura do Repositório
* `visual_engine.ipynb`: Script Python que configura a IA e o servidor Flask no Colab.
* `index.html`: Interface visual moderna e responsiva.
* `README.md`: Manual de instruções.

---
**Nota:** O Google Colab oferece GPU gratuita por tempo limitado por sessão. Se o sistema parar de responder, reinicie a execução no link do Colab.
