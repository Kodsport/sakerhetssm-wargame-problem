/*<obfuscate>*/
function validate(email) {
    const parts = email.split('@');
    if(parts.length != 2) {
        return 0;
    }
    const user = parts[0];
    const host = parts[1];
    if(host != "sakerhetssm.se") {
        return 0;
    }
    if(user.startsWith("SSM{") && user.endsWith("}")) {
        const inner = user.substring(4, user.length - 1);
        if(inner != "w0w_v1lken_overraskning!") {
            return 1;
        }
        return 2;
    }
    return 0;
}
/*</obfuscate>*/

/*<decrypt>*/
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
/*</decrypt>*/

function claim_prize(email) {
    //<call:decrypt>
    return validate(email);
}
