# NES-Kaffe #

<details> 
  <summary>SPOILER</summary>

Port av NanoVM (en minimal JVM) till NES + ett enkelt labyrint-spel skrivet i Java. Rätt lösning av labyrinten ger flaggan.

Måste byta kontroller mellan P1 och P2 enligt ett slumpat mönster annars förlorar man, bör ta alldeles för lång tid att lösa manuellt.

Lösningsförslag:
 * Reva javakoden, lista ut hur labyrinten är uppbyggd och hur lösningen mappar till flaggan
 * Patcha javakoden så att du inte kan förlora, labyrinten kan då lösas manuellt
 * Använd speedrun-tooling för att automatisera lösningsprocessen, exvis Bizhawks Lua-motor
</details>
