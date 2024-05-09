{-# LANGUAGE UndecidableInstances #-}
{-# LANGUAGE FunctionalDependencies #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE TypeOperators #-}
{-# LANGUAGE TypeFamilies #-}
{-# LANGUAGE AllowAmbiguousTypes #-}
{-# OPTIONS_GHC -freduction-depth=0 #-}

-- PEANO --
data Z
data S n

class PAdd a b r | a b -> r
instance PAdd Z Z Z
instance PAdd Z (S x) (S x)
instance (PAdd x y z) => PAdd (S x) y (S z)

class PMul a b r | a b -> r
instance PMul x Z Z
instance PMul Z x Z
instance (PMul x y xy, PAdd x xy xxy) => PMul x (S y) xxy

-- BOOLEAN --
data T
data F

class And a b c | a b -> c
instance And T T T
instance And T F F
instance And F T F
instance And F F F

class PEq a b c | a b -> c
instance PEq Z Z T
instance PEq (S x) Z F
instance PEq Z (S y) F
instance (PEq x y z) => PEq (S x) (S y) z

-- LISTS --
data E
data x ::: xs
infixr 5 :::

class All a b | a -> b
instance All E T
instance All (F ::: l) F
instance (All l t) => All (T ::: l) t

class Length a b | a -> b
instance Length E Z
instance (Length xs r) => Length (x:::xs) (S r)

-- FUNCTIONS --
class Apply f a b | f a -> b
class MapMany f a b | f a -> b

instance MapMany E E E
instance MapMany E (x ::: xs) E
instance MapMany (x ::: xs) E E
instance (Apply f a b, MapMany fs as bs) => MapMany (f:::fs) (a:::as) (b:::bs)

-- CTF
--GENERATED-CONSTRAINTS--

class CheckFlag f r | f -> r
instance (MapMany Cs f a, Length Cs cl, Length f fl, PEq cl fl e, All a t, And e t r) => CheckFlag f r

-- REIFICATION AND MAGIC
class ToString t where toString :: t -> String
instance ToString T where toString _ = "Correct!!"
instance ToString F where toString _ = "Incorrect!!"

success :: CheckFlag Flag a => a
success = undefined

main :: IO()
main = putStrLn (toString success)

--- Klistra in flaggan från 'gen_flag.py' på nästa rad ---
