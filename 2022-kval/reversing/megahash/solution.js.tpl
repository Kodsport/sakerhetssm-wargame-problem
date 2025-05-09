/*[TARGET]*/

let megahash_inv = (input) => {
    if(input.length > HASH_LEN) {
        throw 'Input is too large';
    }
    let data = new Uint8Array(HASH_LEN);
    input.forEach((x, i) => { data[i] = x; });
    
    for(let i = 0; i < HASH_LEN; i++) {

        {
            let data2 = new Uint8Array(HASH_LEN);
            for(let j = 0; j < HASH_LEN; j++)
                for(let k = 0; k < HASH_LEN; k++)
                    data2[j] ^= data[k] * ((DIFFUSION[j] >> k)&1);
            data = data2;
        }
        
        data = data.map(x => SBOX.indexOf(x));


    }
    return data;
};

let solve = () => {
    const decoder = new TextDecoder();
    const flag = megahash_inv(TARGET);
    console.log(decoder.decode(flag));
}

solve();
