# Våffelhuset

## Tänkt uppgiftstext för publicering
Välkomna till våffelhuset! Lyckas du göra det efterfrågade antalet våfflor innan tävlingen är över?

## Beskrivning
En enkel bufferöverskrivning i en datastruktur för att komma runt mekanismer i ett program.
Våffelhuset tar indata via stdin:
  * ålder
  * namn
  * ursprung

Både parametrarna namn och ålder kan användas för att få in användarspecificerad data i variabeln som håller värdet för antal tillverkade våfflor.
När rätt antal våfflor tillverkats skrivs flaggan ut.

## Bygga
Beroende på vilken svårighetsgrad man vill ha programmet byggas med olika parametrar. 
Här får SSM-gänget gärna hjälpa till om ni tycker default-uppgiften är för svår:

* ``RANDOM=[yes|no]`` default = yes
  Om RANDOM=yes kommer målvärdet för bufferöverskrivningen slumpas varje gång programmet körs.

* ``HINT_STRUCT=[yes|no]`` default=no
  Om HINT_STRUCT=yes kommer programmet skriva ut definitionen för datastrukturen som innehåller räknaren att skrivas ut.

Det vill säga att den "svåraste" varianten byggs med utan att ange några några parametrar alls:
``make``
...medan den "enklaste" varianten byggs enligt:
``make RANDOM=no HINT_STRUCT=yes``

Jag anser inte att källkoden ska publiceras som del av uppgiften.

## Testa
Ett pwntools-baserat lösningsförslag finns i filen ``solve.py``.

## Docker
En template för docker/docker-compose finns i ``docker``-mappen.  En standardvariant med xinetd som tcp-wrapper för programmet. Binären kopieras in till ``docker/chall`` när man bygger.

## Kontakt
Lars Helgeson, FOI  
Tel: +46703935326  
Jobb: lars.helgeson@foi.se  
Privat: larshson@gmail.com  
Discord: larshson (finns bland annat i kodsport)  
