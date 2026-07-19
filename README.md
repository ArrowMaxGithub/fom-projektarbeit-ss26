# Projektstruktur
Das Projekt wird mit [UV](https://docs.astral.sh/uv/getting-started/installation/) verwaltet und ist in drei Pakete gegliedert:

1. durak: Python-Implementierung eines Durak-Spiels für zwei Spieler
2. cli: Terminalbasiertes Spiel Mensch gegen Agent
3. dqn: DQN-Trainer auf Basis von [Ray RLLib](https://docs.ray.io/en/latest/rllib/index.html), bereitgestellt als Docker-Container.


# CLI-Verwendung
Ein Spiel kann gestartet werden, indem einer der folgenden Bot-Namen an den Unterbefehl `play` übergeben wird:

1. Zufällig: `random`
2. Niedrigste Karte zuerst: `lowest-card`
3. Niedrige Karten früh, hohe Karten später: `interpolation`
4. Nach Trumpfkarten fischen: `trump-fish`
5. DQN Version 0: `dqn-v0`
6. DQN Version 1: `dqn-v1`
7. DQN Version 7: `dqn-v7`
8. DQN Version 14: `dqn-v14`
9. DQN Version Final: `dqn-final`

Beispiel gegen DQN Version 14: `uv run game play dqn-v14`

Dieselbe Bot-Auswahl kann an den Unterbefehl `simulate` übergeben werden, um N Spiele zwischen zwei Bots auszutragen: `uv run game simulate lowest-card dqn-final 1000`

Alle verfügbaren Optionen werden mit `--help` angezeigt.