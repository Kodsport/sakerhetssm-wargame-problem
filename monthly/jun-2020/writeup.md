# Säkerhetsbiblioteket

Första steget till lösningen är att trycka på knappen längst upp till höger på huvud sidan och läsa source. Vi ser att bara böcker som matchar `"borrowed": False` visas på huvud sidan, Så uppgiften är nog att komma åt en bok som är utlånad.

Rad 26 i source ser ungefär ut så här:

```py
book=collection.find_one({"id": json.loads(request.args.get("id"))})
```

Detta är koden som listar ut vilken bok som visas när man går in på en bok. vi kontrollerar `request.args.get("id")`, eftersom det är `id=` argumentet i urlen. Säkerhetsfelet här är att json.loads används i onödan, vilket låter oss skicka andra datatyper än bara nummer till "id" i collection.find_one funktionen. Därför, kan vi göra en [NoSQL injection](https://medium.com/rangeforce/nosql-injection-6514a8db29e3). Till exempel, kan vi fråga servern om en bok med en id högre än 2 genom att skicka med detta på slutet av urlen: `?id={"$gt":2}`. Servern svarar då med den enda andra boken i databasen, vilket råkar vara flagboken, i vilkens beskrivning flaggan finns.
