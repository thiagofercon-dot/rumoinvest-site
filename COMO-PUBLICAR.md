RUMOINVEST — COMO PUBLICAR UMA MATÉRIA (leia inteiro antes de começar)

*** REGRA DEFINITIVA (decisão do Thiago em 19/11/2026) ***
O ARTEFATO RUMOINVEST (slug e85b1871-a5cb-4045-9513-a84fa69ac27f) FOI DESATIVADO. NUNCA mais leia, publique, atualize ou use o artefato (nem mcp__claude-artifacts__*, nem a ferramenta Artifact) para o RumoInvest. NÃO existe mais "espelho". A ÚNICA publicação é no site oficial rumoinvest.com, via repositório GitHub thiagofercon-dot/rumoinvest-site (branch main), conforme a seção 2J. Onde este documento disser "artefato", "espelho", "publish_files", "get_artifact", "list_files" ou "read_file" do artefato, IGNORE: não se aplica mais.
Este playbook mora no próprio repositório (COMO-PUBLICAR.md, na raiz). Clone o repositório primeiro (seção 2J, passo 1) e leia-o de lá.

O site é gerado a partir do repositório GitHub. Cada matéria é um arquivo content/AAAA-MM-DD-HHMM-slug.json. O arquivo index.html é gerado por build.py a partir de template.html + content/*.json. Não mexa em template.html nem nas imagens, a menos que o pedido peça.

1) MATERIAL DE ORIGEM (pasta do Google Drive "RumoInvest", id 1b5NOQIurvkwRGUVhedrZ9D1OulmXdYvV)
- RENDA FIXA: a execução "mercado" do horário 13:10 escreve uma matéria de categoria renda-fixa (Tesouro Direto, Selic aplicada, CDB, LCI/LCA, inflação). Pesquise com WebSearch/WebFetch fontes oficiais (Banco Central/Copom, Tesouro Direto, Portal do Investidor/CVM, IBGE) e imprensa especializada para taxas e fatos do dia; use apenas dados confirmados e cite as fontes; use "source_doc": "pesquisa-web-renda-fixa" e "source_topic" com o assunto. Não repita assunto já publicado (confira source_topic). Nas demais execuções de mercado, use o relatório de fechamento/abertura.
- Tarefa "mercado": use o arquivo mais recente cujo título começa com "Relatório de Fechamento" ou outro relatório de análise de mercado da pasta (gerado pelo Agente Pesquisador, 3x ao dia: 8h, 13h, 18h). Consulte também "Base de Conhecimento - Agente Pesquisador RumoInvest" (missão, fontes oficiais, estratégia).
- Tarefa "tendências": use o arquivo mais recente cujo título começa com "Relatório de Tendências" (assuntos mais pesquisados no Google). Consulte também "Diretrizes e Prompt - Agente de Tendências RumoInvest". Cubra as 3 MAIORES BUSCAS do relatório (os 3 termos em alta, na ordem do relatório): escreva UM artigo educativo para cada termo que ainda não virou matéria (confira source_doc/source_topic), ou seja, até 3 artigos por execução. Cada JSON leva "trend": {"rank": 1|2|3, "term": "termo em alta", "ref": "DD/MM do relatório"}; a home mostra esses 3 em "Mais buscados no Google hoje". Se o relatório trouxer menos de 3 termos, cubra os que houver. Se os 3 já foram cobertos, NÃO publique nada e explique no resumo.
- Antes de escrever, confira os JSON já publicados (campo "source_doc" = id do arquivo do Drive e "source_topic"). Não repita pauta nem relatório já usado: se não houver material novo, escolha outra pauta ainda não coberta do relatório; se não sobrar nenhuma, NÃO publique nada e explique no resumo da execução.

2) COMO ESCREVER (jornalista do mercado financeiro, tom analítico, objetivo e acessível)
- Público: investidor iniciante. Linguagem simples, traduza o "economês". Transforme porcentagens em exemplos em reais ("Se você investir R$ 100...") e marque exemplos hipotéticos como ilustrativos.
- Tese do portal: ações abaixo de R$ 10, ações de dividendos (BBAS3, TAEE4) e FIIs populares (MXRF11, GARE11).
- NUNCA recomende compra/venda nem prometa retorno. Conteúdo educativo e informativo. O aviso legal é inserido automaticamente pelo site.
- NÃO invente números, datas, cotações ou citações. Use apenas o que está no relatório ou confirme em fonte oficial (BCB, IBGE, Tesouro, B3, CVM RAD, Fed, SEC) via WebSearch/WebFetch; cite as fontes no campo "sources". Dados que você não conseguir confirmar: não use.
- 350 a 600 palavras. Título forte e claro; "subtitle" é a linha fina (1-2 frases). Inclua ao menos um bloco "giga" (Giga explica) com exemplo prático.
- Termômetro de humor: "sentiment" = Otimista, Pessimista, Alerta ou Neutro (conforme o relatório).
- IMAGEM DE CAPA (OBRIGATÓRIA, via Canva): a CAPA de toda matéria é gerada no Canva (seção 2B). O Canva é usado SOMENTE para a capa. As demais imagens dentro das matérias vêm do Gemini (seção 2H).

2B) CAPA NO CANVA (obrigatório; o Canva é usado SOMENTE para a capa)
- Gere a imagem de capa com mcp__canva__generate-image (carregue o schema com ToolSearch se necessário), aspectRatio LANDSCAPE_16_9. Prompt em português descrevendo uma ilustração editorial moderna ligada ao assunto da matéria (ex.: gráfico em alta + prédios para fechamento; balança com moedas e imóveis para FIIs). Paleta da marca: azul-marinho, verde-azulado e verde (âmbar/dourado como acento). SEM texto nem letras na imagem. Para dinheiro, prefira notas de real brasileiro (não dólares), exceto matéria sobre mercado mundial. A formiga mascote Giga pode aparecer apenas em matérias educativas/mercado (de forma simpática, sem alterar o personagem).
- Aguarde o job com mcp__canva__get-generate-image-job (repita até SUCCESS). O resultado mostra "[Image source: /tmp/claude-tool-results/.../arquivo.png]": esse é o arquivo no disco (miniatura ~200 px; o ambiente não consegue baixar a versão em alta do Canva porque o host export-download.canva.com é bloqueado — não tente curl).
- Converta para a capa: python3 -c "from PIL import Image,ImageFilter; im=Image.open(ORIGEM).convert('RGB').resize((1200,675),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,60,2)); im.save('assets/covers/SLUG.jpg',quality=88)". No JSON: "image": "assets/covers/SLUG.jpg", "image_alt": "descrição curta da imagem", "canva_media_id": "id MAH... retornado". Inclua o arquivo da imagem no mesmo commit da seção 2J.
- Se o Canva falhar após 2 tentativas, publique a matéria sem "image" (o site usa uma capa gráfica automática) e avise no resumo.
- CAPA EM ALTA RESOLUÇÃO, FOTO REALISTA (regra de 18/11, vale no site oficial): o generate-image só entrega miniatura de ~200 px, então faça assim: (1) generate-image com prompt de FOTO realista 16:9 sem texto/letras/calendário/placas, nada de ilustração desenhada; (2) mcp__canva__create-design em formato Presentation (16:9) usando o media id como referência, imagem em tela cheia; (3) mcp__canva__export-design em jpg, qualidade 90, largura 1200 e altura 675, e guarde a URL (export-download.canva.com); se o design tiver 2 páginas e a página 1 sair em branco, use a URL da página 2 (0002); (4) no repositório, escreva em content/imagens-pendentes.json {"assets/covers/SLUG.jpg": "URL"} (mantenha as chaves já existentes) e faça push na main: o workflow "Baixar imagens das matérias" baixa as imagens e esvazia o arquivo. Confira depois que a capa não está em branco e não tem texto.

2H) IMAGENS DO GEMINI DENTRO DA MATÉRIA (além da capa)
- O agente de pesquisa (Gemini) deixa imagens na pasta RumoInvest do Drive (id 1b5NOQIurvkwRGUVhedrZ9D1OulmXdYvV), junto do relatório do mesmo dia/horário, como arquivos png/jpg/webp ou embutidas no documento do relatório (nesse caso baixe com mcp__Google_Drive__download_file_content, exportando como docx/pdf, e extraia: unzip do docx -> word/media; ou pdfimages).
- Use essas imagens como imagens ilustrativas DENTRO do corpo da matéria correspondente (bloco {"type":"image","src":"assets/figuras/SLUG-1.jpg","alt":"...","caption":"..."}), associando cada imagem ao tema/seção/termo do relatório. NÃO use a imagem do Gemini como capa (a capa é do Canva). Se o Gemini entregar mais de uma imagem para o tema, use até 2 no corpo.
- Converta para largura máx. 1200 px (ImageOps.contain, JPG qualidade 88) e inclua no mesmo commit da seção 2J. ANTES de usar, abra a imagem (Read) e confira: sem texto/letras errados, em português do Brasil, sem marca de terceiros, sem personagens protegidos e, para dinheiro, notas de real brasileiro (exceto mercado mundial). Se tiver problema, não use.
- Se não houver imagem do Gemini para o tema, publique só com a capa do Canva e avise no resumo final (mesma linha de aviso da seção 2F). Não gere imagens extras no Canva para substituir.
- Para ilustrações dentro do texto (tarefa de tendências): mesma rotina, salvando em assets/figuras/SLUG-N.jpg e inserindo o bloco {"type":"image","src":"assets/figuras/SLUG-N.jpg","alt":"...","caption":"..."}.
- Mapa mental: use o bloco {"type":"mindmap","title":"Mapa mental: ...","center":"Tema","branches":[{"label":"Ramo","items":["...","..."]}]} (3 a 5 ramos, 2 a 4 itens curtos cada).

2C) TAREFA DE TENDÊNCIAS: ARTIGO EDUCATIVO (o relatório é só a base)
- Use o termo em alta e a "dúvida central do usuário" como ponto de partida para um ARTIGO EDUCATIVO completo (400 a 700 palavras) que ensine o conceito a quem está começando: o que é, por que importa, como funciona, exemplo em R$, erros comuns e o que observar. Cruze com a tese (ações < R$ 10, BBAS3/TAEE4, MXRF11/GARE11) sem recomendar compra.
- Inclua sempre: (a) um bloco "giga" com exemplo prático; (b) um MAPA MENTAL do tema (bloco mindmap); (c) capa gerada no Canva (seção 2B); (d) quando houver imagem do Gemini para o tema, 1 imagem ilustrativa no corpo (seção 2H, bloco image). Escolha categoria educacao quando for conceito geral; use fiis/acoes/dividendos/renda-fixa quando o foco for esse ativo.
- O Canva é usado SOMENTE para a capa de cada matéria (decisão de 17/11). Imagens dentro do texto vêm do Gemini. Links do Canva são privados: não os coloque em "sources".

3) FORMATO DO JSON
{
 "slug": "titulo-em-minusculas-sem-acentos-com-hifens",
 "title": "...", "subtitle": "...",
 "category": "mercado | dividendos | fiis | renda-fixa | acoes | educacao",
 "date": "AAAA-MM-DD (hoje, fuso America/Sao_Paulo)", "time": "HH:MM (horário do slot: 08:05, 13:10 ou 18:15 para mercado; 08:20, 13:25 ou 18:30 para tendências)",
 "sentiment": "Otimista|Pessimista|Alerta|Neutro",
 "meta": "descrição de até 160 caracteres", "tags": ["..."], "sources": ["..."], "trend": {"rank":1,"term":"termo em alta","ref":"DD/MM"} (só tarefa tendências),
 "source_doc": "id do arquivo do Drive usado", "source_topic": "pauta/termo (tarefa tendências) ou 'fechamento'/'abertura'/'intradia'",
 "body": [ blocos... ]
}
Campos de imagem: "image" (capa, Canva), "image_alt", "canva_media_id"; imagens do corpo via bloco image.
Blocos: {"type":"image","src":"assets/figuras/x.jpg","alt":"...","caption":"..."}  {"type":"mindmap","title":"...","center":"...","branches":[{"label":"...","items":["..."]}]}  {"type":"p","text":"..."}  {"type":"h2","text":"..."}  {"type":"ul","items":["..."]}  {"type":"callout","text":"..."}  {"type":"table","head":["A","B"],"rows":[["x","y"]]}  {"type":"giga","title":"Giga explica: ...","blocks":[ p / table ... ]}
Use **negrito** dentro dos textos. Não use HTML.
Categoria: mercado = abertura/intradia/fechamento e macro; fiis; dividendos; acoes (ações baratas e demais); renda-fixa (Tesouro, CDB, LCI/LCA, Selic aplicada); educacao (guias e "como investir").

4) PUBLICAR (somente GitHub; o artefato NÃO é mais usado)
a) Siga a seção 2J (clonar o repositório, copiar JSON/capas/imagens, atualizar data/cotacoes.json, rodar python3 build.py, conferir com Playwright, commit e push na main).
b) NÃO publique, leia nem atualize o artefato RumoInvest em hipótese alguma.
c) Resumo final de 2 linhas: título publicado, categoria, fontes, e a mensagem do commit enviado à main (ou o erro, conforme 2J).
Se o Drive, o GitHub ou a pesquisa estiverem indisponíveis, não publique conteúdo inventado: explique o problema no resumo.


5) ONDE CADA MATÉRIA APARECE E LINGUAGEM PÚBLICA (regras do site)
- A HOME mostra apenas NOTÍCIAS (categorias mercado, dividendos, fiis, renda-fixa, acoes), com chamada "Continue lendo". Os artigos educativos NÃO aparecem na lista de notícias da home.
- Os ARTIGOS EDUCATIVOS da tarefa "tendências" são SEMPRE publicados com "category": "educacao" (seção Educação), com o campo "trend": {"rank": 1|2|3, "term": "termo em alta", "ref": "DD/MM"}. A seção Educação os destaca em "Assuntos em alta".
- NUNCA escreva em título, linha fina, texto, tags ou fontes que o tema é "mais pesquisado/mais buscado no Google" nem cite "Google Trends" ou "Relatório de Tendências". Use apenas "assunto em alta" / "tema do momento".
- Matérias de mercado e renda fixa (notícias) usam a categoria do assunto (mercado, renda-fixa, dividendos, fiis, acoes) e aparecem na home e na seção correspondente.


2D. SEO E GATILHOS MENTAIS (obrigatório em todo artigo educativo)
- Título com a palavra-chave principal no início + promessa clara (ex.: "O que é a taxa Selic? Entenda em 5 minutos...").
- "meta" com 140-160 caracteres, contendo a palavra-chave. 4-6 "tags" com variações de busca (ex.: "O que é Selic", "Como investir").
- Estrutura: parágrafo de abertura com a palavra-chave em negrito, 3+ blocos h2 (viram o índice "Neste artigo"), exemplo numérico rotulado como ilustrativo, "giga" (Giga explica), mindmap, bloco "faq" (3-4 perguntas, vira dados estruturados FAQPage) e bloco "cta" final.
- Links internos: use [texto](#materia-slug) no corpo; cada artigo deve linkar para pelo menos 2 outros (artigos relacionados/evergreen).
- Gatilhos mentais permitidos (honestos): clareza ("em 5 minutos", "passo a passo"), curiosidade, autoridade (citar fonte oficial: Banco Central, CVM, Tesouro, B3), prova por números verificáveis, escassez/urgência só quando real (ex.: data de reunião do Copom), reciprocidade (guia gratuito), ação (CTA).
- PROIBIDO: prometer rentabilidade garantida, "fique rico", depoimentos ou números de prova social inventados, urgência falsa. Sempre incluir que rentabilidade passada não garante resultados futuros quando falar de retorno.
- Formato faq: {"type":"faq","title":"...","items":[{"q":"...","a":"..."}]}; cta: {"type":"cta","title":"...","text":"... [link](#materia-slug)"}.
- Os 4 guias evergreen já publicados: o-que-e-a-taxa-selic..., como-comecar-a-investir-com-pouco-dinheiro..., renda-fixa-ou-renda-variavel..., reserva-de-emergencia... Linke para eles.


2E. NOVO PADRÃO DOS DOCUMENTOS DO DRIVE (14/11, ler sempre antes de escrever)
- Base de Conhecimento do Agente Pesquisador: relatório diário com 6 seções (Mercado, Dividendos, FIIs, Renda Fixa, Ações, Educação). CADA seção deve virar pelo menos uma matéria na categoria correspondente (mercado, dividendos, fiis, renda-fixa, acoes, educacao). Nunca deixar uma seção do site vazia.
- Ativos da tese: ações abaixo de R$ 10; BBAS3 e TAEE4 (dividendos); MXRF11, GARE11 e HGLG11 (FIIs). Nunca chamar de "carteira recomendada" nem recomendar compra/venda.
- Todo dado numérico deve ter exemplo em reais ("Se você investir R$ 100...", rotulado como ilustrativo), termômetro de humor (Otimista, Pessimista, Alerta, Neutro) e o aviso legal (já automático no site).
- FONTES: em "sources" use objetos {"t":"nome da fonte","url":"link","at":"dd/mm/aaaa hh:mm"} (a data/hora da informação). Strings simples ainda funcionam, mas prefira objetos com link. Sempre citar ticker/nome oficial no texto. Só use links reais que apareceram no relatório; nunca invente URL.
- Diretrizes do Agente de Tendências: relatório com os 5 termos do dia (a home mostra até 5 "Assuntos em alta") e seções detalhadas por termo, cada uma com Pacote SEO. Use no JSON: "focus_kw" (palavra-chave foco), "meta" (até 160 caracteres) e "tags" (as do Pacote SEO). Cruzar sempre o termo com a tese (ações < R$ 10, BBAS3, TAEE4, MXRF11, GARE11). Escrever matéria (categoria educacao, campo trend) para os 3 primeiros; os demais ficam só na lista do relatório.


2F. SEM RELATÓRIO NO DRIVE: PESQUISA PRÓPRIA + AVISO (16/11)
- Antes de escrever, confira na pasta RumoInvest se existe relatório do slot atual (data e hora no nome/modifiedTime: do dia, gerado depois da última rodada). Se não houver relatório novo, NÃO pare e NÃO reaproveite o relatório antigo como se fosse novo.
- Nesse caso, faça a pesquisa por conta própria na web (WebSearch/WebFetch, fontes oficiais e grandes veículos, dados do dia confirmados em pelo menos 2 fontes), siga os mesmos padrões das seções 2D e 2E (6 seções, fontes com link e data/hora, sem recomendação, sem números inventados) e publique normalmente.
- AVISE o usuário: a PRIMEIRA linha do resumo final da execução deve ser "⚠️ AVISO: relatório do Gemini não encontrado na pasta do Drive para este horário. Pesquisa própria feita pelo Claude." seguida de 1 linha com o que foi pesquisado e as fontes. Se o relatório existir, a primeira linha deve ser "✅ Relatório do Drive usado: <nome do arquivo>".
- No JSON, preencha "source_doc" com "Pesquisa própria do Claude (sem relatório do Drive em DD/MM hh:mm)" quando for o caso. Em tendências sem relatório, escreva a matéria só se achar assuntos em alta verificáveis na web; senão, diga no aviso que não publicou.


2I. FAIXA DE COTAÇÕES NO TOPO DO SITE (obrigatório em TODA execução) — regra revisada em 28/11
- O site mostra, abaixo do cabeçalho superior, uma faixa rolante "B3 · Cotações" lida do arquivo data/cotacoes.json do repositório (build.py a embute no index.html). A cada execução, atualize esse arquivo e inclua-o no mesmo commit/push da seção 2J.
- Formato: {"updated":"DD/MM/AAAA hh:mm","fechamento":"DD/MM/AAAA","items":[{"t":"BBAS3","p":"R$ 15,10","v":-0.35}, ...]}. "t" = ticker/nome; "p" = preço ou pontos já formatado em pt-BR; "v" = variação percentual do dia como número (opcional; omita se não souber).
- DATA DO FECHAMENTO: o dia do último pregão fechado a que os números se referem vai UMA VEZ no campo "fechamento" (DD/MM/AAAA), e o site a mostra abaixo do rótulo "B3 · Cotações" (ex.: "Fechamento 27/11"). NÃO escreva mais a data em cada ativo: não use o campo "ref" nos itens (remova-o se existir). Se os números forem de pregão em andamento, use o último fechamento completo e deixe isso claro no texto da matéria, não na faixa.
- TODOS OS ATIVOS: extraia SEMPRE todos os ativos da B3 que aparecerem nos relatórios do Drive do dia (Relatório de Fechamento/Abertura, Base de Conhecimento e Relatório de Tendências) e na pesquisa do dia: Ibovespa, dólar, TODAS as ações e TODOS os fundos imobiliários citados, sem limite de quantidade. Itens fixos que nunca saem: IBOVESPA, DÓLAR, MXRF11, GARE11, HGLG11, BBAS3, TAEE4. Ordem: IBOVESPA, DÓLAR, ações (fixas primeiro), FIIs.
- Use SOMENTE números que estejam no relatório do Drive desse horário ou em fonte confiável confirmada na web na mesma execução (B3, RI das empresas, grandes veículos); nunca invente nem estime. Se um ativo não tiver número novo nesta execução, mantenha o anterior apenas se for do último fechamento; remova itens com mais de 2 dias úteis. Ao mudar o dia do fechamento, atualize "fechamento" e confira que TODOS os itens são desse dia.
- Atualize "updated" com a data/hora da execução. A faixa já mostra o aviso de que são cotações de referência, sem recomendação.

2J. PUBLICAÇÃO NO SITE OFICIAL (GitHub Pages, rumoinvest.com) — obrigatório em TODA execução que gerar matéria ou atualizar cotações
O site oficial é o repositório GitHub thiagofercon-dot/rumoinvest-site (branch main), publicado automaticamente: todo push na main dispara o workflow "Publicar na Hostinger" (GitHub Actions), que gera o site estático e o envia à Hostinger; o site atualiza uns 3 minutos depois do push. O artefato foi desativado em 19/11/2026 e não é mais usado; a PUBLICAÇÃO OFICIAL (e única) é esta.
ATENÇÃO (18/11): nas execuções de 08:05, 08:20 e 13:10 de 18/11 as matérias foram publicadas só no artefato e o site oficial ficou sem elas. Esta etapa é OBRIGATÓRIA: sem o push na main o rumoinvest.com NÃO atualiza. Se add_repo, clone ou push falharem, tente de novo (até 3 vezes) e, se continuar falhando, escreva na PRIMEIRA linha do resumo: "⚠️ GITHUB NÃO PUBLICADO: <erro exato>". Nunca encerre dizendo que publicou se o push não aconteceu. Confira com git log -1 e git status que o commit subiu para origin/main. Faça-a logo depois de escrever as matérias e gerar as capas, na mesma execução:
1) Chame mcp__claude-code-remote__add_repo com owner "thiagofercon-dot", repo "rumoinvest-site", access "push". Em seguida: git clone --depth 1 https://github.com/thiagofercon-dot/rumoinvest-site /home/claude/rumoinvest-site (UM clone, timeout de 10 min) e mcp__claude-code-remote__register_repo_root se o add_repo mandar.
2) Para cada matéria nova: copie o JSON para content/ com o nome AAAA-MM-DD-hhmm-slug.json (mesmo formato de sempre), a capa para assets/covers/NOME.jpg (1200x675, o mesmo caminho do campo "image") e cada imagem do corpo para assets/figuras/NOME.jpg (o mesmo caminho do bloco image). Nunca apague nem altere matérias de outros horários.
3) Campo "capa" (só no site oficial): matéria de mercado das 08:05 e a de renda fixa das 13:10 levam "capa": "dia"; a de mercado das 19:00 leva "capa": "noite"; as de tendências (educação) não levam. 
4) Atualize data/cotacoes.json conforme a seção 2I e rode: python3 build.py (ele valida os campos obrigatórios e se as capas existem e gera o index.html; se der erro, corrija e rode de novo).
5) Confira com Playwright (file:// no index.html): a página abre sem erro de JavaScript e a faixa de cotações aparece.
6) git add -A; git commit -m "Matérias de DD/MM hhh"; git -c push.negotiate=true push origin HEAD:main. Se o push for rejeitado (outro horário publicou antes): git fetch --depth=1 origin main; git reset --hard origin/main; refaça os passos 2 a 4 (copiar arquivos, rodar build.py) e tente de novo, no máximo 3 vezes.
7) Nunca edite template.html nem build.py no repositório, a menos que a tarefa peça. Nunca coloque chaves, tokens ou dados pessoais no repositório (ele é público).
8) No resumo final diga se o GitHub foi publicado (mensagem do commit) ou, se falhou, o erro; em caso de falha, NÃO use o artefato como alternativa: avise o erro exato no resumo e envie push notification.


2K. FERRAMENTAS E SIMULADORES: ATUALIZAR A SELIC (28/11) — execuções de mercado (08:05 e 19:00) e de renda fixa (13:10)
O site tem 3 ferramentas (/ferramentas/): calculadora de juros compostos, Tesouro Selic vs. Poupança e simulador de aportes. A de Tesouro Selic vs. Poupança traz a Selic padrão escrita em template.html (função toolSelic): o campo id="ts-s" com value="13.75" e o parágrafo "Premissas e fontes", que cita a meta de 13,75% ao ano, o Copom de 04/11/2026 e o Comunicado nº 46.230 do Banco Central.
- QUANDO ATUALIZAR: somente quando o Copom mudar a meta da Selic (reunião nova) ou quando você confirmar no site do Banco Central (bcb.gov.br, comunicado do Copom) que a meta vigente é outra. Se a meta continua 13,75% ao ano, NÃO mexa em nada.
- COMO: no clone, edite SOMENTE esses dois pontos de template.html: (a) value="13.75" do campo ts-s para a nova meta (ponto decimal, ex.: 13.50); (b) no parágrafo "Premissas e fontes", troque a meta (com vírgula, ex.: 13,50%), a data da reunião do Copom, o número do Comunicado e a data de vigência pelos dados do comunicado oficial. Não invente número de comunicado nem datas: se não conseguir confirmar no bcb.gov.br, não altere e avise no resumo.
- Faça o commit "Ferramentas: Selic atualizada para X% (Copom DD/MM/AAAA)" e o push na main junto com as matérias (fluxo da seção 2J). Esta é a única exceção à regra "nunca edite template.html".
- NÃO altere as demais premissas (regra da poupança, tabela regressiva do Imposto de Renda) sem fonte oficial mostrando que mudaram.
- No resumo final, diga em uma linha se a Selic das ferramentas foi atualizada ou se permaneceu em 13,75%.
