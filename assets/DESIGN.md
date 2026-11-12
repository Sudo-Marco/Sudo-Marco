# Identidade visual · Spike + Pintinho

## Ideia

O pintinho é o mascote; o spike é a energia. A assinatura gráfica é uma curva LIF em integração, disparo e reset, com o pintinho reagindo ao pico. A marca usa o `sudo` só como detalhe tipográfico pequeno. Não usamos janela de terminal, escudo ou estética de template de portfólio.

## Paleta

| Token | Cor | Uso |
|---|---|---|
| Base | `#152126` | Verde-petróleo quase carvão; fundo escuro e texto no tema claro. |
| Apoio | `#FFD93B` | Amarelo original do pintinho; curva, badges e texto no tema escuro. |
| Spike | `#397581` | Azul-petróleo moderado; somente no segmento do disparo LIF. |
| Superfície clara | `#F1F2E8` | Tom neutro do tema claro, tratado como variação de superfície da base. |

Contraste relativo calculado para as cores da marca: base/apoio `11,93:1`; base/spike `3,16:1`; apoio/spike `3,78:1`. No tema claro, base/superfície `14,57:1` e superfície/spike `4,61:1`. Amarelo sobre superfície clara tem apenas `1,22:1`; por isso, não o use como texto ou linha solta nesse tema. O retrato original do pintinho mantém as cores e o contorno que lhe dão forma.

Há três cores de identidade: base, apoio e spike. Os tons de superfície claro/escuro são variantes neutras da base. A arte do mascote é reutilizada pixel a pixel; seus tons próprios não são recoloridos nem usados como novas cores de interface.

## Tipografia e forma

- Nome: `Segoe UI`, com fallback para `Arial` e sans-serif do sistema.
- Detalhes técnicos: `Consolas`, com fallback para `Courier New` e monospace.
- Os textos permanecem como texto SVG e usam fontes locais; não há fontes externas nem dependência de serviços.
- Cantos arredondados aparecem só nos banners e cards. Os traços da curva mantêm as quinas do próprio sinal.

## Uso do pintinho

- A origem de verdade é `assets/source/piu-front-sheet.png`, cópia do atlas aprovado do Synapse Pet.
- O gerador recorta os frames originais de 32 × 44 px: idle `(0, 0, 32, 44)` e feliz `(64, 0, 96, 44)`.
- Mantenha a proporção e amplie com vizinho mais próximo. Não redesenhe, recolora, gire, aplique glow nem invente expressões.
- O pintinho aparece nos banners, marca, cards e em um divisor pontual. Os demais divisores ficam só com o trem de pulsos.

## Movimento e acessibilidade

- Só o banner principal se anima: um traço percorre o trem de pulsos, o spike acende e o pintinho dá um pequeno salto/troca para o frame feliz.
- O ciclo dura 5 s e usa CSS dentro do SVG. A regra `prefers-reduced-motion: reduce` remove as animações e mostra o estado final estático.
- Cada SVG tem `<title>` e `<desc>`. Cada uso em Markdown tem alt text. Acento de spike é gráfico não textual; texto usa pares de alto contraste.
- Todo par de tema em README é escolhido com `<picture>` e `prefers-color-scheme`; imagens e capturas são locais ao repositório.
- Os cards embutem uma cópia compacta da captura real como dado no próprio SVG, evitando referências de imagem externas ou quebradas; a captura original permanece intacta.

## Gerar novamente

O gerador usa Pillow para recortar o sprite e montar os social previews PNG. Os arquivos de origem já ficam em `assets/source/`.

```powershell
python -m pip install Pillow
python tools/generate_brand_assets.py --synapse ..\synapse-companion --urna ..\urna-cidada
```

Execute com os três repositórios em diretórios irmãos, ajustando os caminhos se necessário. O comando atualiza os SVGs do perfil, as marcas/cards/badges dos dois projetos e os arquivos `docs/social-preview-dark.png` e `docs/social-preview-light.png` de cada projeto. Compare o diff depois de gerar; o script não atualiza as descrições dos repositórios nem modifica screenshots ou sprites-fonte.

Os social previews são imagens fixas 1280 × 640 porque o GitHub aceita somente uma imagem por repositório. `docs/social-preview.png` é a versão escura pronta para upload; as variantes `social-preview-dark.png` e `social-preview-light.png` ficam disponíveis para escolha manual.
