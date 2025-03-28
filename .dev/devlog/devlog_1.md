# Devlog_1 - Commit: 'Commit inicial do Front-end'

## 📝 Dissertação
- Módulo separado para o front-end para tornar mais fácil de adicionar/mexer na UI
- App.py cuida apenas das configurações da página essenciais
- Quero tentar deixar tudo o mais escalável possível e facilitar a manutenção da front_end. Dessa forma:
    - Manterei o código o mais simples possível, toda lógica complexa deverá ficar para o backend.
    - Focarei em fazer uma versão que funcione, para testar a ui primeiro e discutir os elementos da ui, antes de escrever o código.

## 🔧 Decisões de Código e Desenvolvimento
- 26/03: Iria ser feito usando OOP, mas usaremos funções para simplicidade.
- 26/03: Não usaremos multilinguagem por enquanto por falta de tempo, mas fica como uma ideia interessante para a v3.
    <details>
        <summary>Detalhamento</summary>
        Os testes feitos com tradução funcionaram bem, porém teríamos que traduzir todos os presets manualmente. Como não teremos tempo suficiente pra isso, deixamos essa ideia como um ponto para um v3. Não será difiícil desenvolver, apenas demorado. OBS: O código também teria que ser adaptado, mas isso é fácil com IA.
    </details>
 - 26/03: Ao invés de definirmos NO CÓDIGO quais presets o usuário pode escolher, vamos usar o constructor.py para calcular a lista de presets disponível com base na pasta de presets/. Dessa forma, sempre que adicionarmos um novo preset, ele já vai automaticamente procurar na pasta, com a função do constructor.py.
 - 26/03: Não acho que o banner está bom, removido temporariamente e será adicionado novamente depois.
 - 26/03: Rascunho base da main_interface() feito, com botões do LinkedIn dos dois criadores, e um st.info para descrever o projeto. Botão 'Gerar Dados' até o momento é apenas simbólico.
 - 27/03: Rascunho da interface de geração simples finalizada.
 - 27/03: Duas colunas para os filtros não ficou bonito, revertendo para uma coluna.
 - 27/03:
 - 27/03: Rascunho da interface de geração customizável **NÃO** finalizada, voltar e continuar trabalhando nela amanhã. Ver 'Próximos Commits e Revisões'.


## 🧪 Testes
 - 26/03: Testes de performance genéricos e menores.
 - 27/03: A ui funciona, mas não é responsiva e não tem os padrões automáticos que faciltiarão a vida do usuário, devemos incrementar isso.

## 💡 Próximos Commits e Revisões
 - REVISAR todos os helps e markdowns, e outros textos para o usuário, podem estar mal escritos.
 - Adicionar helpers nos filtros do modo customizado, que são muito complexos.
 - Adicionar o banner, que não foi adicionado.
 - A qt de colunas no modo de geração simples e no modo de geração customizável ainda não foi definida pra ser configurada de forma dinâmica.
 - O front-end ainda não tem um sistema robusto de padrões nos filtros que considera os tipos de análise selecionados. Por exemplo, quando selecionado algum tipo que não seja classificação ou regressão, ele deveria automaticamente tirar o filtro da target (não vai ter target). Devemos ajustar pra considerar esses padrões.
 - Ainda não colocamos pro usuário poder customizar os valores de integridade pras colunas e pra target, devemos adicionar.
 - Usuario poder escolher quais colunas target incluir.
 - Balanceamento de classes precisa ser mais customizável. Pra começar, o número de classes deve ser baseado no preset.
 - Botão 'Gerar Dados' puramente simbólico por enquanto.
 - Colocamos valores de texte para as interfaces simples e customizadas (presets), devemos escrever uma função simples em constructor.py para poder já ler os presets disponíveis. 
 - Popular o código com comentários e rmover os comentários de debug.

## 🔮 Futuro (v3)
 - Multilinguagem. Adaptaremos todos os presets para suportar inglês e português.
 - Separar a quantidade de linhas, deixando 100 mil como limite, com uma opção "Ativar mais linhas (Experimental)", com um st.warning avisando que pode apresentar travamentos, demorar pra carregar, e que os formatos csv e excel deixam de ser utilizados, apenas PARQUET (pra rodar tudo mais rápido internamente por ser PARQUET-only)
 - O streamlit não usa async por padrão. Seria interessante, embora talvez não traga muito resultado útil, testar aplicar session.state, cache e monitoramente de processos pra fazer a página esperar o usuário filtrar.