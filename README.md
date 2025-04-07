# 📊 Segmentação PF Sicredi Vanguarda

Projeto para análise e previsão de segmentos de clientes Pessoa Física (PF), considerando renda, investimentos e localização, com o objetivo de apoiar decisões estratégicas da cooperativa **Sicredi Vanguarda PR/SP/RJ**.

---

## 🚀 Funcionalidades

- **Geração de dados sintéticos** representativos de clientes PF  
- **Classificação de clientes** em segmentos: **PF I**, **PF II**, **PF III**, **PF IV**  
- **Definição automática** do canal de atendimento ideal: **Digital** ou **Agência**  
- **Análises estatísticas** por região e segmento  
- **Modelo preditivo** para prever a migração de canal  
- **Dashboard interativo** com Streamlit  
- **Visualizações profissionais** com Seaborn e Matplotlib  
- **Código modular e reutilizável** para fácil manutenção  

---

## 🛠 Tecnologias Utilizadas

- **Python 3.10+**  
- **Pandas** & **NumPy**  
- **Seaborn** & **Matplotlib**  
- **Scikit-learn**  
- **Streamlit**  
- **Jupyter Notebook**  

---

## 🧠 Lógica de Segmentação

| Segmento | Renda Mensal         | Investimentos         | Canal de Atendimento |
|----------|----------------------|-----------------------|-----------------------|
| **PF I** | Até R$ 2.000         | Qualquer              | Digital               |
| **PF II**| R$ 2.001 a R$ 4.000  | Qualquer              | Digital               |
| **PF III**| R$ 4.001 a R$ 10.000 | Ou ≥ R$ 100.000       | Agência               |
| **PF IV**| Acima de R$ 10.000   | Ou ≥ R$ 250.000       | Agência               |

---

## 📊 Visualização do Dashboard

Para executar o dashboard, utilize o comando abaixo:

```bash
streamlit run src/app_modelo_segmentacao.py
```

---

## 📦 Instalação do Projeto

Siga os passos abaixo para configurar o ambiente:

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Sicredi_Segmentacao_PF.git
cd Sicredi_Segmentacao_PF

# Crie e ative o ambiente virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

---

## 🧪 Testes e Simulações

Explore e valide o projeto utilizando os notebooks disponíveis na pasta `notebooks/`:

- **Exploração de dados**  
- **Testes de modelos preditivos**  
- **Simulação de mudanças** nas faixas de corte  
- **Análise de padrões** por região  

---

## 👨‍💻 Autor

**João Pedro Cavalheiro dos Reis**  
Estudante de Ciência da Computação  
Profissional na Sicredi Vanguarda PR/SP/RJ  

[🔗 LinkedIn](https://www.linkedin.com/in/seu-perfil) • [💻 GitHub](https://github.com/seu-usuario)

---