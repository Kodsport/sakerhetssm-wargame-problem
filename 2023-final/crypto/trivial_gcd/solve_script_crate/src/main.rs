use rug::{
    integer::{IsPrime, Order},
    ops::Pow,
    Integer,
};
use std::{
    io::{self, BufRead},
    str,
    time::Instant,
};

#[derive(Clone)]
/// A symbolic representation of the gcd expression
///
/// Initially, `amc=bmc=0`, `ac=bc=1`, `a = e_1` and `b = e_2`.
/// This corresponds to
/// ```
/// gcd(c_2^0 m^e_1 - c_1^1, c_1^0 m^e_2 - c_2^1)
/// = gcd(m^e_1 - c_1, m^e_2 - c_2)
/// ```
struct Exponents {
    amc: Integer,
    a: Integer,
    ac: Integer,
    bmc: Integer,
    b: Integer,
    bc: Integer,
}
impl Exponents {
    /// Doing a symbolic gcd step:
    /// ```
    /// gcd(c_2^amc m^a - c_1^ac,         c_1^bmc m^b     -         c_2^bc)
    /// gcd(c_2^amc m^a - c_1^ac, c_2^amc c_1^bmc m^b     - c_2^amc c_2^bc)
    /// gcd(c_2^amc m^a - c_1^ac, c_2^amc c_1^bmc m^b     - c_2^amc c_2^bc - c_1^bmc m^(b-a)(c_2^amc m^a - c_1^ac))
    /// gcd(c_2^amc m^a - c_1^ac, c_1^ac  c_1^bmc m^(b-a) - c_2^amc c_2^bc)
    /// gcd(c_2^amc m^a - c_1^ac, c_1^(bmc+ac)    m^(b-a) - c_2^(amc+bc))
    /// ```
    /// So `(amc, a, ac, bmc, b, bc) -> (amc, a, ac, bmc+ac, b-a, amc+bc)` when `b >= a`.
    /// Symmetrically, we have that
    /// ```
    /// gcd(c_2^amc      m^a     - c_1^ac      , c_1^(bmc+ac) m^(b-a) - c_2^(amc+bc))
    /// gcd(c_1^bmc      m^b     - c_2^bc      , c_2^(amc+bc) m^(a-b) - c_1^(bmc+ac))
    /// gcd(c_2^(amc+bc) m^(a-b) - c_1^(bmc+ac), c_1^bmc      m^b     - c_2^bc)
    /// ```
    fn symbolic_forward(&self) -> Self {
        let mut s = self.to_owned();
        if s.a <= s.b {
            s.bmc += &s.ac;
            s.b -= &s.a;
            s.bc += &s.amc;
        } else {
            s.amc += &s.bc;
            s.a -= &s.b;
            s.ac += &s.bmc;
        }
        s
    }
    /// This value is proportional to the memory required to evaluate the gcd numerically.
    fn min_size(&self) -> Integer {
        Integer::max(
            Self::size(&self.amc, &self.a, &self.ac),
            Self::size(&self.bmc, &self.b, &self.bc),
        )
    }
    /// Approximately proportional to the logarithm of `c_i^xmc m^x - c_j^xc`.
    fn size(xmc: &Integer, x: &Integer, xc: &Integer) -> Integer {
        Ord::max(Integer::from(xmc + x), xc.clone())
    }
}

/// Solution approach:
/// ```
/// c_1 = m^e_1 % (pq)
/// c_2 = m^e_2 % (pr)
/// p = remove_small_factors(gcd(m^e_1 - c_1, m^e_2 - c_2))
/// ```
/// But m^e_1 and m^e_2 are way too large to compute (approx 1GB each).
/// Let's do a few symbolic gcd steps before computing high powers.
///
/// The transformation rules are derived under `symbolic_next`.
fn main() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();
    let m = parse("m", lines.next());
    let e1 = parse("e_1", lines.next());
    let e2 = parse("e_2", lines.next());
    let c1 = parse("c_1", lines.next());
    let c2 = parse("c_2", lines.next());
    let cipher = parse("cipher", lines.next());
    assert!(lines.next().is_none());

    let start = Instant::now();
    let mut exponents = Exponents {
        amc: Integer::ZERO,
        a: e1.clone(),
        ac: Integer::from(1usize),
        bmc: Integer::ZERO,
        b: e2.clone(),
        bc: Integer::from(1usize),
    };
    let naive_size = exponents.min_size();
    println!(
        "Estimated largest value to compute if done naively: {} GB",
        naive_size.clone() * m.signed_bits() / 8_000_000_000u64
    );
    println!("Step 0: Verifying symbolic gcd sqrt speedup hypothesis");
    {
        let mut e = exponents.clone();
        for steps in 0..100 {
            println!("size = {} at step = {steps}", e.min_size());
            e = e.symbolic_forward();
        }
    }
    println!(
        "Step 1: Preprocessing with symbolic gcd steps. (elapsed = {}s)",
        Instant::now().duration_since(start).as_secs_f64()
    );
    let mut steps = 0;
    let mut last_size = naive_size.clone();
    loop {
        let next_exponents = exponents.symbolic_forward();
        let next_size = next_exponents.min_size();
        if next_size > last_size {
            break;
        }
        steps += 1;
        exponents = next_exponents;
        last_size = next_size;
    }
    println!(
        "{}x speedup through {} symbolic steps",
        naive_size / &last_size,
        steps
    );
    println!(
        "Estimated largest reduced value to compute: {} MB",
        2 * last_size * m.signed_bits() / 8_000_000
    );
    let mut p = gcd_from_reduced_exponents(exponents, c1, c2, m, start);
    println!(
        "Step 5: Getting flag (elapsed = {}s)",
        Instant::now().duration_since(start).as_secs_f64()
    );
    for d in 2..100usize {
        p.remove_factor_mut(&Integer::from(d));
    }
    println!("p = {}", p);
    assert_ne!(p.is_probably_prime(30), IsPrime::No);
    let phi: Integer = Integer::from(&p - 1i64) * p.clone().pow(9);
    let d = Integer::from((1 << 16) + 1u64).invert(&phi).unwrap();
    let message = cipher
        .pow_mod(&d, &p.pow(10))
        .unwrap()
        .to_digits(Order::Lsf);
    let flag = str::from_utf8(&message).unwrap();
    println!("{}", flag);
}
fn gcd_from_reduced_exponents(
    Exponents {
        amc,
        a,
        ac,
        bmc,
        b,
        bc,
    }: Exponents,
    c1: Integer,
    c2: Integer,
    m: Integer,
    start: Instant,
) -> Integer {
    let a_small = Exponents::size(&amc, &a, &ac) < Exponents::size(&bmc, &b, &bc);
    println!(
        "Step 2: Computing gcd_small (elapsed = {}s)",
        Instant::now().duration_since(start).as_secs_f64()
    );
    let gcd_small = if a_small {
        Integer::from((&c2).pow(amc.to_u32().unwrap()))
            * Integer::from((&m).pow(a.to_u32().unwrap()))
            - Integer::from((&c1).pow(ac.to_u32().unwrap()))
    } else {
        Integer::from((&c1).pow(bmc.to_u32().unwrap()))
            * Integer::from((&m).pow(b.to_u32().unwrap()))
            - Integer::from((&c2).pow(bc.to_u32().unwrap()))
    };
    println!(
        "Step 3: Computing gcd_big (elapsed = {}s)",
        Instant::now().duration_since(start).as_secs_f64()
    );
    let gcd_big = if a_small {
        c1.pow_mod(&bmc, &gcd_small).unwrap() * m.pow_mod(&b, &gcd_small).unwrap()
            - c2.pow_mod(&bc, &gcd_small).unwrap()
    } else {
        c2.pow_mod(&amc, &gcd_small).unwrap() * m.pow_mod(&a, &gcd_small).unwrap()
            - c1.pow_mod(&ac, &gcd_small).unwrap()
    };
    println!(
        "Step 4: Computing their gcd (elapsed = {}s)",
        Instant::now().duration_since(start).as_secs_f64()
    );
    Integer::gcd(gcd_big, &gcd_small)
}

fn parse(name: &str, line: Option<io::Result<String>>) -> Integer {
    let line = line.unwrap().unwrap();
    let mut items = line.split(|ch: char| ch.is_whitespace());
    assert_eq!(name, items.next().unwrap());
    assert_eq!("=", items.next().unwrap());
    Integer::parse(items.next().unwrap()).unwrap().into()
}
