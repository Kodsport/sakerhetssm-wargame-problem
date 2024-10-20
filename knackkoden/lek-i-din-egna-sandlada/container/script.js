// Grattis du hittade hit! Här är kod från min server som din webbläsare gladeligen tog emot genom att besöka min hemsida
// Under fliken "console" så kan du köra egen javascript kod, testa kopiera koden nedan och läs ut resultatet från funktionen genom att anropa den.

function strxor(enc, key) {
    var ret = '';
    for (var i = 0; i < enc.length; i++)
        ret += String.fromCharCode(enc.charCodeAt(i) ^ key.charCodeAt(i % key.length));
    return ret;
}

function fåFlagga() {
    const flagga = strxor("12=\x1e\x0e\x97\x1a\x1a\x03>\x03\x04\x02\x17\x0c\x00=\x08/\x16\r\x1d\r\x02\x87\x05\x11\x0bM\x0e", "bapelsin")
    console.log(flagga)
}

// fåFlagga()