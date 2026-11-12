# Entrever — fotografia e filmes

Landing page de uma marca fictícia de fotografia e filmes. O case apresenta casamentos, formaturas, newborn e narrativas em vídeo. O projeto está pronto para ser versionado no GitHub e publicado como site estático na Vercel, mas ainda não está conectado a nenhum serviço.

![Prévia da seção Sobre](docs/previews/preview-sobre-arredondado-desktop.jpg)

## Tecnologias

HTML semântico, CSS e um pequeno JavaScript para a navegação. Não há framework, bundler ou build para servir o site. As imagens publicadas são WebP; as fontes Fraunces e Plus Jakarta Sans são carregadas localmente em WOFF2.

## Estrutura

```text
Entrever/
├── site/                  # Única pasta publicada pela Vercel
│   ├── index.html         # Landing page
│   ├── 404.html           # Página para URLs inexistentes
│   └── assets/
│       ├── css/           # Estilos da landing page e do 404
│       ├── js/            # Indicador e rolagem do menu
│       ├── fonts/         # Fontes e licenças OFL
│       └── images/        # Arquivos WebP usados nas páginas
├── identidade/            # Marca, estudos e logo fonte da origemdev
├── imagens/               # PNGs originais usados para gerar os WebPs
├── scripts/               # Exportação de imagens e verificação do site
├── docs/                  # Instruções de deploy e capturas do processo
├── vercel.json            # Publica site/ sem build
└── requirements-dev.txt   # Dependência apenas para exportar imagens
```

## Rodar localmente

Na pasta `site/`:

```bash
python -m http.server 4173
```

Abra `http://localhost:4173/`. A segunda página é `http://localhost:4173/404.html`.

## Verificar e regenerar imagens

Na raiz do projeto:

```bash
python scripts/check_site.py
python -m pip install -r requirements-dev.txt
python scripts/optimize_assets.py
```

O verificador confere arquivos locais, âncoras, dimensões e formato das imagens, URLs de fontes e a pasta de saída da Vercel. A exportação lê os PNGs de `imagens/` e os arquivos de `identidade/`, depois grava WebPs em `site/assets/images/`. A Vercel recebe os WebPs prontos e não executa Python.

## Publicação

O arquivo `vercel.json` fixa o preset **Other** e a pasta de saída `site/`. Veja o passo a passo em [docs/DEPLOY.md](docs/DEPLOY.md). O repositório ainda não tem remoto configurado; a conexão com GitHub e Vercel fica para a próxima etapa.

## Conteúdo demonstrativo

A Entrever e o fotógrafo são fictícios. O email `ola@entrever.foto`, a localização em São Paulo e os links de WhatsApp sem destinatário fazem parte do case. Substitua esses dados antes de usar o projeto para atender clientes reais. As imagens originais e as etapas da identidade ficam documentadas em `imagens/` e `identidade/`. A marca origemdev usada no crédito foi copiada para `identidade/origemdev-logo-fonte.webp`, permitindo recriar o arquivo publicado sem depender de outra pasta do computador.

As licenças OFL das fontes estão em `site/assets/fonts/`.
