# Publicação na Vercel

O projeto é um site estático. A Vercel deve publicar **somente o conteúdo de `site/`**. Os PNGs originais, scripts e capturas de tela ficam no repositório para manutenção, mas não entram no site publicado.

## Antes de conectar o GitHub

Na raiz do projeto, execute:

```bash
python scripts/check_site.py
```

Para visualizar localmente:

```bash
cd site
python -m http.server 4173
```

Abra `http://localhost:4173/` e também `http://localhost:4173/404.html` para revisar as duas páginas.

## Importação na Vercel

1. Importe o repositório do GitHub quando ele for conectado.
2. Mantenha a **Root Directory** na raiz do repositório, sem selecionar `site/`.
3. Use o preset **Other**. Não há etapa de build nem instalação de dependências no deploy.
4. O arquivo `vercel.json` já define `site` como **Output Directory**.
5. Confirme que a página inicial abre em `/`, que os assets carregam e que uma URL inexistente mostra a página `404.html`.

Não é preciso configurar variáveis de ambiente para esta versão. O `requirements-dev.txt` serve apenas para gerar imagens WebP localmente.

## Dados demonstrativos

O case usa contatos fictícios. Antes de usá-lo como site comercial real, substitua os links `wa.me/?text=...` por um número válido, o email `ola@entrever.foto` por uma caixa existente e a localização pela informação correta. Após definir um domínio, vale adicionar URL canônica e metadados de compartilhamento com URLs absolutas.

Referências: [sites estáticos sem build](https://vercel.com/docs/builds), [configuração `outputDirectory`](https://vercel.com/docs/project-configuration/vercel-json#outputdirectory) e [página 404 personalizada](https://vercel.com/kb/guide/custom-404-page).
