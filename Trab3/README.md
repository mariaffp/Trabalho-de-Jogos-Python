# Jogo — Evolução do Trab3

Este projeto implementa Trabalho 3 de acordo com o enunciado do classroom.Ele transforma a estrutura inicial em um pequeno jogo de sobrevivência com elementos de bullets. O jogador controla um pato em uma arena, enquanto inimigos aparecem pelas bordas da tela e se aproximam continuamente. O objetivo é sobreviver, desviar dos inimigos e eliminá-los usando os disparos.

A implementação utiliza o padrão de estados para controlar diferentes comportamentos do jogador e dos inimigos. O jogador possui um estado normal, um estado de invencibilidade após receber dano e um estado de ataque ativado pelo power-up. Os inimigos possuem um estado de aproximação, no qual perseguem o jogador, e um estado de atordoamento, que acontece quando são atingidos por um disparo.

Também foram utilizados eventos para realizar a comunicação entre os diferentes objetos do jogo. A criação e destruição de projéteis, a eliminação de inimigos, o recebimento de dano e a ativação do power-up são tratados por meio do sistema de eventos.

Os sprites disponíveis na pasta `images` foram utilizados. O `base.png` representa o jogador normalmente, enquanto `blink.png` indica o estado de invencibilidade quando ele é atacado por um inimigo. Durante o power-up, o jogador utiliza o `quack.png`. Os inimigos utilizam outros sprites da mesma pasta, sendo o `crouch.png` durante a aproximação e `wing.png` quando ele está stunado.

## Manual do jogador

O personagem pode ser movimentado utilizando as teclas clássicas WASD. O botão esquerdo do mouse dispara um projétil na direção do mouse. Os inimigos possuem mais de um ponto de vida, então o primeiro disparo pode deixá-los atordoados, e o segundo disparo os elimina.

Quando um inimigo encosta no jogador, ele perde uma vida e entra automaticamente no estado de invencibilidade. Durante esse período, o pato fica de olho fechado e não pode receber dano novamente. Depois de alguns segundos, ele retorna ao estado normal.

A tecla TAB ativa o poderzinho especial. Nesse momento, o pato muda para o sprite de ataque e cria um círculo de projéteis que fica orbitando ao seu redor durante alguns segundos. Os projéteis orbitais também podem atingir e eliminar os inimigos.

O objetivo é permanecer vivo pelo maior tempo possível, utilizando os disparos, o movimento e o poderzinho, e eliminar os inimigos que spawnam pela arena.
