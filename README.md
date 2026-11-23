# TagGame: Chaser x Runner com Q-Learning

Dois agentes competem em um grid com obstáculos. O **chaser** tenta capturar o **runner**, e o **runner** tenta escapar até o fim do episódio. Cada agente aprende sua própria política por **Q-Learning tabular**, treinando ao mesmo tempo contra o outro (self-play simultâneo, também chamado de Independent Q-Learning).

O projeto é escrito em Python, com visualização em pygame.

## Estrutura do projeto

```
taggame/
  env.py        Ambiente: mapa, regras, estados e recompensas (sem pygame)
  agent.py      Agente Q-Learning (tabela Q, epsilon-greedy, atualização)
  train.py      Treinamento dos dois agentes
  play.py       Visualização em pygame das políticas treinadas
  README.md     Este arquivo
```

Arquivos gerados pelo treino:

```
  chaser_q.pkl  Tabela Q do chaser
  runner_q.pkl  Tabela Q do runner
  train_log.csv Taxa de captura e duração média por janela de episódios
```

## Requisitos

- Python 3.10 ou superior
- `pygame-ce` (ou `pygame`, ver observação abaixo)
- `numpy`

## Instalação

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate        # Linux e macOS
# venv\Scripts\activate         # Windows

pip install pygame-ce numpy
```

Observações:

- No Python 3.14 (por exemplo, no Arch Linux), o pacote `pygame` original pode ser compilado sem o módulo `font` e gerar o erro `font module not available`. O `pygame-ce` resolve isso, pois já publica pacotes prontos. Se os dois estiverem instalados, remova o original:
  ```bash
  pip uninstall pygame
  pip install --force-reinstall pygame-ce
  ```
- Na primeira execução do `play.py`, o `pygame-emojis` baixa um banco de emojis em SVG, então é necessária conexão com a internet apenas nessa vez.

## Como executar

### 1. Treinar os agentes

```bash
python train.py
```

O treino roda sem janela gráfica e imprime o progresso no terminal a cada janela de episódios:

```
ep   1000 | eps 0.99 | capture_rate 0.41 | avg_len 28.3 | estados: C=... R=...
```

Ao final, salva `chaser_q.pkl`, `runner_q.pkl` e `train_log.csv`.

Opções disponíveis:

| Opção | Padrão | Descrição |
|---|---|---|
| `--episodes` | 50000 | Número de episódios de treino |
| `--eps-start` | 1.0 | Epsilon inicial (exploração total) |
| `--eps-end` | 0.05 | Epsilon final |
| `--eps-decay-frac` | 0.7 | Fração dos episódios usada para decair o epsilon |
| `--window` | 1000 | Tamanho da janela de log |
| `--seed` | 0 | Semente aleatória |

Exemplos:

```bash
python train.py --episodes 5000
python train.py --episodes 100000 --window 5000 --seed 42
```

### 2. Assistir aos agentes

```bash
python play.py
```

Abre a janela do pygame e executa as políticas treinadas de forma gulosa (sem exploração). Se os arquivos `.pkl` não existirem, os agentes agem aleatoriamente e o programa avisa no terminal.

Teclas:

| Tecla | Ação |
|---|---|
| Espaço | Pausar e continuar |
| R | Reiniciar o episódio |
| Seta para cima | Aumentar a velocidade |
| Seta para baixo | Diminuir a velocidade |
| Esc | Sair |

O placar na parte inferior mostra quantos episódios cada lado venceu, o passo atual e a velocidade.

## Como funciona

### Ambiente (`env.py`)

- Grid 10x10 com obstáculos fixos (o mapa fica na constante `MAP`).
- Cinco ações: cima, baixo, esquerda, direita e ficar parado.
- Os dois agentes agem ao mesmo tempo. Se o destino estiver bloqueado (obstáculo ou borda), o agente permanece onde está.
- O chaser captura o runner quando a distância de Manhattan entre eles é menor ou igual a `capture_dist` (padrão 1).
- O episódio termina com a captura ou após `max_steps` passos (padrão 60). Se o tempo acabar, o runner vence.
- As posições iniciais são sorteadas, com distância mínima de 4 entre os agentes.

### Estado de cada agente

Uma tupla com a posição relativa do oponente e as paredes adjacentes:

```
(dx, dy, parede_cima, parede_baixo, parede_esquerda, parede_direita)
```

- `dx` e `dy` são limitados a `[-view_clip, +view_clip]` (padrão 6).
- Cada parede vale 1 se a casa vizinha é obstáculo ou borda, e 0 se está livre.
- No máximo 13 x 13 x 16 = 2704 estados possíveis.

Como o estado é relativo, o agente não conhece sua posição absoluta nem enxerga obstáculos que não estejam colados nele.

### Recompensas (soma zero)

| Situação | Chaser | Runner |
|---|---|---|
| Captura | +10 | -10 |
| Cada passo sem captura | -0,1 | +0,1 |

### Aprendizado (`agent.py`)

Atualização de Q-Learning, com `alpha = 0.1` e `gamma = 0.95`:

```
Q(s, a) <- Q(s, a) + alpha * (r + gamma * max Q(s', a') - Q(s, a))
```

A escolha de ação é epsilon-greedy: com probabilidade epsilon o agente explora uma ação aleatória, e caso contrário escolhe a de maior valor Q (empates são resolvidos aleatoriamente). O epsilon decai linearmente durante o treino.

## O que esperar do treino

A taxa de captura **não** cresce de forma monótona. Em geral ela sobe no início, porque perseguir é mais fácil de aprender, e depois cai ou oscila quando o runner aprende a usar obstáculos e cantos. Cada agente é parte do ambiente do outro, então o alvo muda enquanto ambos aprendem (não estacionariedade). Esse comportamento é esperado e vale ser analisado a partir do `train_log.csv`.

## Personalização

- **Mapa:** edite a constante `MAP` em `env.py` (`#` é obstáculo e `.` é célula livre). O mapa precisa ser retangular.
- **Regras:** `max_steps`, `capture_dist` e `view_clip` são parâmetros do construtor de `TagGameEnv`.
- **Recompensas:** altere o bloco `if caught` no método `step` de `env.py`.
- **Hiperparâmetros:** `alpha`, `gamma` e `epsilon` são parâmetros de `QAgent` em `agent.py`.
- **Emojis:** troque os caracteres no dicionário de emojis do `play.py` (nomes e quantidade de agentes continuam iguais).
- **Tamanho da célula:** constante `CELL` no `play.py`.

Depois de mudar o mapa ou as recompensas, treine novamente, pois as tabelas salvas só valem para o ambiente em que foram treinadas.

## Problemas comuns

| Sintoma | Causa provável e solução |
|---|---|
| `font module not available` | `pygame` compilado sem `sdl2_ttf`. Instale `pygame-ce` (ver Instalação). |
| `FileNotFoundError: No file available for emoji` | O emoji escolhido não existe na base do `pygame-emojis`. Use outro emoji. |
| Os agentes se movem aleatoriamente no `play.py` | Os arquivos `.pkl` não foram encontrados. Rode `train.py` na mesma pasta antes. |
| Taxa de captura oscila muito | Comportamento esperado em aprendizado multiagente. Treine por mais episódios e compare seeds diferentes. |

## Ideias de extensão

- Script de avaliação que confronta cada política com um oponente aleatório e com o oponente treinado.
- Gráfico da evolução da taxa de captura a partir do `train_log.csv`.
- Mapas aleatórios a cada episódio, com estado de maior alcance de visão.
- Mais de um chaser e mais de um runner no mesmo grid.
- Comparação com outros algoritmos (SARSA, Double Q-Learning, DQN).

Inteligencia Artificial foi utilizada para auxiliar esse projeto durante seu desenvolvimento
