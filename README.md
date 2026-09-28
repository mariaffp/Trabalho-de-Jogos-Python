Pequeno Pinball simplificado desenvolvido com Pygame na disciplina.

# Como jogar

Use A/D ou as setas esquerda e direita para controlar as abas.

A bola se movimenta pela mesa e pode sofrer diferentes efeitos ao colidir com os objetos. Os obstáculos precisam ser atingidos três vezes, e depois de cada acerto eles ficam atordoados por um tempo e, quando são destruídos, reaparecem depois de alguns segundos.

Também existem bônus espalhados pela mesa, que podem aumentar a pontuação ou alterar a velocidade da bola.

Quando a bola cai pelo vão entre as abas, o jogador perde uma vida. Ao chegar a zero vidas, o jogo termina.

# Colisões

O jogo foi desenvolvido a partir do sistema de colisão por polígonos fornecido no trabalho. A detecção utiliza SAT e a decomposição de polígonos em formas convexas.

Além de detectar as colisões, foi adicionada a resposta à colisão para retirar a bola de dentro dos obstáculos e refletir sua velocidade. As abas também podem transmitir movimento para a bola quando são acionadas pelo jogador.


# Estados e eventos

As abas possuem diferentes estados durante o movimento, incluindo repouso, subida, ativa e descida, além de um estado power-up.

A comunicação entre algumas partes do jogo é feita por eventos, permitindo que colisões e quedas gerem ações como pontuação, perda de vidas e alteração dos estados dos inimigos/obstáculos.
