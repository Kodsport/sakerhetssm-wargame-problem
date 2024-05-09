const encoder = new TextEncoder();
let input = 'SSM{th3_MEGAHASH_m3ga_c00l}';
let input_bytes = encoder.encode(input)
const digest = megahash(input_bytes);

console.log('['+Array.from(digest).toString()+']');
