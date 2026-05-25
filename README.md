# Snake — Jogo local multiplayer

Jogo **Snake** em Python com [Pygame](https://www.pygame.org/), pensado para partidas locais com **2 a 4 jogadores** na mesma tela. O visual segue um estilo retrô (grid, cores sólidas e HUD minimalista), inspirado em arcades clássicos.

## Funcionalidades

- Seleção de **2, 3 ou 4 jogadores** no menu inicial
- Tela em **tela cheia** (resolução do monitor atual)
- Cada jogador controla uma cobra com cor própria
- **Comida compartilhada**: quem come primeiro ganha o ponto
- Colisões: paredes, próprio corpo, corpo de outras cobras e cabeça contra cabeça
- **Placar em tempo real** e tela de fim de jogo com vencedor ou empate
- Efeitos sonoros ao comer e no game over

## Requisitos

- Python 3.10+ (testado com 3.11)
- [Pygame](https://www.pygame.org/)

## Instalação

```bash
git clone <url-do-repositorio>
cd SnakeMultiplayer

python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate

pip install pygame
```

## Como executar

Os arquivos de áudio ficam em `src/assets/`. Execute o jogo **a partir da pasta `src`** para que os sons sejam carregados corretamente:

```bash
cd src
python main.py
```

## Controles

### Menu

| Tecla | Ação |
|-------|------|
| `2` / `3` / `4` | Escolher número de jogadores |
| `Enter` | Iniciar partida |
| `Esc` | Sair |

### Durante a partida

| Jogador | Cor (padrão) | Movimento |
|---------|--------------|-----------|
| P1 | Verde | `W` `A` `S` `D` |
| P2 | Azul | Setas |
| P3 | Amarelo | `I` `J` `K` `L` |
| P4 | Magenta | `T` `F` `G` `H` |

| Tecla | Ação |
|-------|------|
| `Esc` | Encerrar o jogo |
| `Espaço` | Voltar ao menu (após game over) |

Não é possível inverter a direção em 180° (por exemplo, indo para a direita não pode pressionar esquerda imediatamente).

## Regras de vitória

- Permanece em jogo enquanto houver **mais de um jogador vivo**
- Quando restar **apenas um vivo**, ele vence
- Se **todos morrerem no mesmo instante**, vence quem tiver **maior pontuação**; empate se o placar for igual

Cada maçã (`Food`) vale **1 ponto** e faz a cobra crescer um segmento.

## Estrutura do projeto

```
SnakeSingleplayer/
├── docs/
│   ├── Arquitetura Snake - C4 Model - Context Diagram.pdf
│   ├── Arquitetura Snake - C4 Model - Container Diagram.pdf
│   └── Arquitetura Snake - C4 Model - Components Diagram.pdf
├── src/
│   ├── main.py              # Ponto de entrada
│   ├── game.py              # Loop principal, menus, HUD e renderização
│   ├── config.py            # Resolução, grid, cores e mapeamento de teclas
│   ├── sprites.py           # Entidades Snake e Food
│   ├── systems.py           # Colisões, direção e áudio de gameplay
│   ├── utils.py             # Posição aleatória no grid
│   └── assets/
│       ├── snakeEat.wav
│       └── gameover.wav
├── .gitignore
└── README.md
```

### Responsabilidade dos módulos

| Módulo | Papel |
|--------|--------|
| `main.py` | Inicia a aplicação e delega para `Game.run()` |
| `game.py` | Orquestra eventos, atualização, desenho e fluxo (menu → partida → game over) |
| `config.py` | Constantes globais (tela, FPS, cores, direções, teclas por jogador) |
| `sprites.py` | Lógica de movimento, crescimento e desenho das cobras e da comida |
| `systems.py` | Regras de colisão (parede, auto-colisão, entre cobras, comida) |
| `utils.py` | Geração de coordenadas aleatórias no grid |

## Arquitetura

O sistema está documentado no modelo **C4** (níveis 1 a 3). Os diagramas ficam em `docs/`:

| Nível C4 | Diagrama | Arquivo |
|----------|----------|---------|
| 1 — Contexto | Sistema, usuários e dependências externas | [Context Diagram](docs/Arquitetura%20Snake%20-%20C4%20Model%20-%20Context%20Diagram.pdf) |
| 2 — Containers | Aplicação desktop, assets e fronteiras principais | [Container Diagram](docs/Arquitetura%20Snake%20-%20C4%20Model%20-%20Container%20Diagram.pdf) |
| 3 — Componentes | Módulos Python (`game`, `sprites`, `systems`, etc.) | [Components Diagram](docs/Arquitetura%20Snake%20-%20C4%20Model%20-%20Components%20Diagram.pdf) |

Arquivos (caminho relativo à raiz do repositório):

- `docs/Arquitetura Snake - C4 Model - Context Diagram.pdf`
- `docs/Arquitetura Snake - C4 Model - Container Diagram.pdf`
- `docs/Arquitetura Snake - C4 Model - Components Diagram.pdf`

## Configuração

Parâmetros principais em `src/config.py`:

| Constante | Descrição | Valor padrão |
|-----------|-----------|--------------|
| `CELL_SIZE` | Tamanho de cada célula em pixels | `20` |
| `FPS` | Velocidade do loop (quadros por segundo) | `10` |
| `WIDTH` / `HEIGHT` | Resolução da janela | Tela cheia do monitor |

A grade é calculada automaticamente: `GRID_WIDTH = WIDTH // CELL_SIZE` e o mesmo para a altura.

## Desenvolvimento

- Código em **Python**, sem dependências além do Pygame
- Pastas `venv/` e `__pycache__/` estão no `.gitignore`
- Para alterar sons, substitua os `.wav` em `src/assets/` mantendo os nomes `snakeEat.wav` e `gameover.wav`, ou ajuste os caminhos em `systems.py` e `game.py`

## Licença

Não especificada neste repositório. Inclua um arquivo `LICENSE` se for distribuir o projeto.
