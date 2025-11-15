<h1 align="center" style="font-weight: bold;">Genesights 📊</h1>

<div align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white" alt="Pandas" />
    <img src="https://img.shields.io/badge/Matplotlib-11557c?logo=plotly&logoColor=white" alt="Matplotlib" />
    <img src="https://img.shields.io/badge/Postgres-%23316192.svg?logo=postgresql&logoColor=white" alt="Postgres" />
    <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff" alt="Docker" />
</div>

## 🔧 Pré-requisitos

- [Python](https://www.python.org/downloads/)
- Importação de todas bibliotecas, o mesmo pode ser instalalado via terminal atráves do comando.

```yaml
pip install streamlit
pip install pandas
pip install matplotlib
pip install sqlalchemy
pip install dotenv
```

## ⚙️ Particularidades do sistema

 - Para a correta geração do gráfico no sistema e a prevenção de erros, o arquivo <code>(.xlsx, .csv)</code> deve seguir o layout padrão pré-definido, em conformidade com a simplicidade da ferramenta. Para gerar todos os valores na ferramenta Genesights, é necessário seguir todo layout conforme consta na imagem abaixo:
  
![alt text](src/img/layoutCompleto.png)

- O usuário precisa ter no minímo algumas colunas obrigatórias para geração de gráficos dentro da ferramenta, conforme consta na imagem abaixo (Elementos obrigatórios para realizar a filtragem dos meses).
  
 ![alt text](src/img/layoutObrigatorio.png)

- A coluna <code>Max, Min, Média, Desvio Padrão, Variação de Porcentagem</code> serão utilizado para geração de gráfico com base na sua necessidada, ou seja, caso queira um gráfico de valores máximo o arquivo (.xlsx, .csv) necessita ter o coluna <code>MAX</code> com alguns valores.
  
  - <strong> OBS: Não é necessário seguir a mesma ordem do layout. </strong>
