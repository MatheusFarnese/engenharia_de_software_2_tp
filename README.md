# Trabalho prático da disciplina de engenharia de software 2
## Aluno: Matheus Farnese Lacerda Senna
## Explicação do sistema
Esse é um sistema para a realização de cálculos para o jogo Clash of Clans. Clash of Clans é um jogo
da Supercell, uma empresa finlandesa de desenvolvimento de jogos que foi lançado em 2012 e é muito jogado
até hoje. Cada jogador possui uma vila (com construções defensivas, chamadas de "defesas") e um exército, sendo que o
objetivo principal é atacar as vilas dos outros jogadores com o seu exército, visando destruí-las completamente. Para tal,
são utilizadas tropas, feitiços e heróis. Heróis possuem habilidades especiais que os permitem aplicar dano diretamente em
diferentes locais da vila, sendo que várias estratégias de ataque envolvem a destruição de defesas específicas utilizando
essas habilidades especiais combinadas com feitiços de dano.

Esse sistema foi feito exatamente para facilitar os cálculos para essas estratégias, relacionando para cada defesa
da vila do oponente (setado pelo usuário), o número de feitiços de terremoto (um tipo de feitiço de dano do jogo) necessário para, pareado com
as habilidades dos heróis, destruí-la completamente. O sistema suporta 3 tipos de estratégias diferentes do jogo, com várias configurações de
habilidades possíveis, cobrindo grande parte das estratégias viáveis que envolvem a utilização dessas habilidades de dano direto. Ademais,
também foi desenvolvido uma interface web para tornar mais intuitivo a interação com o usuário.

## Explicação do sistema para quem joga Clash of Clans
Esse é um sistema para facilitar os cálculos em ataques de fireball, spiky ball e em entradas com a Royal Champion e recall. Primeiramente, o
usuário seleciona o nível das defesas da vila que está atacando, utilizando um botão para gerar os níveis relativos ao townhall escolhido, sendo
possível ajustar cada nível manualmente permitindo um ajuste mais grão fino. Em seguida, seleciona-se os níveis de heróis e equipamentos. Então,
escolhe-se a estratégia (fireball, spiky ball ou champion recall), sendo que, para as duas primeiras, as entradas da tabela são a quantidade de
earthquakes necessários para destruir cada defesa, dado que foi utilizado o respectivo equipamento (fireball ou spiky ball) sozinho ou combinados
entre si ou combinados com a giant arrow. Para o caso da Royal Champion, cada célula da tabela é o número de ataques de rocket spear necessários
para derrubar cada defesa, podendo ser combinado com o seeking shield e com um earthquake.

## Explicação das tecnologias utilizadas
O backend do sistema foi totalmente desenvolvido em python. O código foi modularizado em classes, cada qual com uma tarefa específica.

Para o frontend (i.e. interface web) foi utilizado o framework streamlit, que é um framework python open-source.

Para os testes, foi utilizado o pytest, configurado também no github actions.

## Execução do sistema
Utilize o seu método preferido (e.g. git clone ou download zip) para fazer o download dos arquivos desse repositório para o seu computador.
Em seguida, abra um terminal, vá para o diretório raiz da aplicação (o diretório que contém os arquivos .py e o folder "datasets") e execute o seguinte comando:

$ streamlit run streamlit_app.py

Ao executar esse comando, será aberto uma página no seu browser defaut com a aplicação desenvolvida.
Caso o framework streamlit não esteja instalado, é possível instalar com:

$ pip install streamlit
