{-# LANGUAGE RecursiveDo, LambdaCase, ScopedTypeVariables #-}
import Control.Monad.Tardis
import Control.Monad
import Data.Functor.Identity
import Control.Monad.Trans.Class
import Debug.Trace
import System.IO.Unsafe
import System.IO
import Control.Monad.Trans.Random
import Control.Monad.Random.Class
import System.Random
import Data.Tuple.Extra
import Data.Maybe
import Data.Bool
import Data.List
import System.Exit
import Data.Char

data Tree a = Leaf a | Node (Tree a) (Tree a) deriving (Show, Eq)
data Bit = One | Zero deriving (Eq)
type BitString = [Bit]

instance Show Bit where
  show b = case b of
    One -> "1"
    Zero -> "0"

showBitString :: BitString -> String
showBitString = concatMap show

parseBitString :: String -> BitString
parseBitString = map (\case '0' -> Zero; '1' -> One;)

left :: Tree a -> Tree a
left (Leaf x) = Leaf x
left (Node x _) = x

right :: Tree a -> Tree a
right (Leaf x) = Leaf x
right (Node _ x) = x

leaf :: Tree a -> Bool
leaf (Leaf _) = True
leaf _ = False

val :: Tree a -> Maybe a
val (Leaf x) = Just x
val _ = Nothing

decodeCh :: Tree a -> BitString -> (Maybe a, BitString)
decodeCh (Leaf x) a = (Just x, a)
decodeCh t [] = (Nothing, [])
decodeCh t (c:cs) = decodeCh ((if c == One then left else right) t) cs

decode :: Tree a -> BitString -> ([a], BitString)
decode t b = let (r, b') = decodeCh t b in if isNothing r then ([], b) else (fromJust r :) `first` decode t b'

encodeCh :: Eq a => Tree a -> a -> BitString
encodeCh (Leaf x) _ = []
encodeCh t c = v
  where (a, b) = (uncurry (&&&) $ uncurry `both` ((.left) &&& (.right)) encodeCh) (t, c)
        (d, e) = decodeCh t `both` (One:a, Zero:b)
        v = if Just c == fst d then One:a else Zero:b

encode :: Eq a => Tree a -> [a] -> BitString
encode t = concatMap (encodeCh t)

invert :: Bit -> Bool -> Bit
invert x False = x
invert One True = Zero
invert Zero True = One

flips :: [Bool] -> BitString -> BitString
flips = zipWith $ flip invert

scrambleT :: RandomGen r => RandT r (Tardis (Tree a) (Tree a)) ()
scrambleT = mdo
  x <- lift getPast
  r :: Bool <- getRandom
  if leaf x then lift $ sendPast x else mdo
    lift $ sendPast (bool flip id r Node z y)
    y <- lift getFuture
    lift $ sendFuture (left x)
    scrambleT
    z <- lift getFuture
    lift $ sendFuture (right x)
    scrambleT

scrambleTree :: (Eq a, RandomGen b) => b -> Tree a -> (Tree a, b)
scrambleTree r t = (a, b)
  where ((_, b), (a, _)) = runTardis (runRandT scrambleT r) (undefined, t)

-- INTERNAL --
scramble :: (Eq a, RandomGen b) => b -> Tree a -> [a] -> ([a], BitString)
scramble r t = decode t' . flips bs . encode t
  where (t', r') = scrambleTree r t
        bs = randoms r'
-- END INTERNAL --

unscramble :: (Eq a, RandomGen b) => b -> Tree a -> ([a], BitString) -> [a]
unscramble r t (l, xs) = fst (decode t . flips bs . (++ xs) . encode t' $ l)
  where (t', r') = scrambleTree r t
        bs = randoms r'

tree = Node (Node (Node (Leaf 'y') (Leaf 'q')) (Node (Node (Node (Node (Leaf 'n') (Leaf 'r')) (Leaf 'N')) (Leaf '4')) (Node (Node (Node (Leaf 'Z') (Node (Leaf 'P') (Node (Node (Node (Leaf 'W') (Node (Leaf '2') (Leaf '6'))) (Leaf '8')) (Leaf 'g')))) (Node (Node (Node (Node (Leaf 'o') (Leaf 'D')) (Leaf 'x')) (Node (Leaf 'b') (Leaf 'i'))) (Leaf '_'))) (Node (Node (Leaf 'u') (Leaf 'L')) (Leaf 'z'))))) (Node (Node (Node (Leaf 's') (Node (Leaf 'p') (Node (Node (Leaf 'a') (Node (Leaf 'f') (Leaf 'H'))) (Leaf '0')))) (Node (Leaf 'E') (Node (Leaf 'R') (Leaf '}')))) (Node (Node (Node (Node (Node (Leaf 'v') (Leaf '9')) (Node (Node (Leaf 'V') (Leaf 'e')) (Leaf 'I'))) (Node (Leaf 'K') (Node (Leaf 'O') (Leaf '3')))) (Node (Leaf 'G') (Leaf '7'))) (Node (Node (Node (Node (Node (Node (Node (Leaf 'm') (Leaf 'M')) (Leaf 'U')) (Node (Node (Node (Leaf 'j') (Node (Leaf 'X') (Leaf 'h'))) (Node (Leaf 'J') (Leaf 'c'))) (Node (Leaf 'B') (Leaf 'F')))) (Leaf '1')) (Leaf 'S')) (Node (Node (Leaf 'l') (Node (Leaf 'Q') (Leaf '{'))) (Node (Node (Leaf 'd') (Leaf '5')) (Node (Leaf 't') (Node (Leaf 'C') (Leaf 'k')))))) (Node (Node (Leaf 'Y') (Leaf 'T')) (Node (Leaf 'w') (Leaf 'A'))))))
--tree = undefined
scrambledTree = Node (Node (Node (Node (Node (Node (Leaf '0') (Node (Node (Leaf 'H') (Leaf 'f')) (Leaf 'a'))) (Leaf 'p')) (Leaf 's')) (Node (Node (Leaf '}') (Leaf 'R')) (Leaf 'E'))) (Node (Node (Node (Node (Leaf 'K') (Node (Leaf '3') (Leaf 'O'))) (Node (Node (Leaf '9') (Leaf 'v')) (Node (Leaf 'I') (Node (Leaf 'e') (Leaf 'V'))))) (Node (Leaf 'G') (Leaf '7'))) (Node (Node (Node (Node (Node (Leaf 'Q') (Leaf '{')) (Leaf 'l')) (Node (Node (Leaf 'd') (Leaf '5')) (Node (Node (Leaf 'C') (Leaf 'k')) (Leaf 't')))) (Node (Leaf 'S') (Node (Node (Node (Node (Node (Leaf 'j') (Node (Leaf 'h') (Leaf 'X'))) (Node (Leaf 'J') (Leaf 'c'))) (Node (Leaf 'B') (Leaf 'F'))) (Node (Leaf 'U') (Node (Leaf 'M') (Leaf 'm')))) (Leaf '1')))) (Node (Node (Leaf 'T') (Leaf 'Y')) (Node (Leaf 'A') (Leaf 'w')))))) (Node (Node (Node (Node (Node (Node (Node (Leaf 'i') (Leaf 'b')) (Node (Leaf 'x') (Node (Leaf 'o') (Leaf 'D')))) (Leaf '_')) (Node (Leaf 'Z') (Node (Node (Node (Leaf '8') (Node (Node (Leaf '6') (Leaf '2')) (Leaf 'W'))) (Leaf 'g')) (Leaf 'P')))) (Node (Node (Leaf 'u') (Leaf 'L')) (Leaf 'z'))) (Node (Node (Node (Leaf 'r') (Leaf 'n')) (Leaf 'N')) (Leaf '4'))) (Node (Leaf 'y') (Leaf 'q')))

toString :: (String, BitString) -> String
toString (s, bs) = s ++ ":" ++ showBitString bs

splitOn :: Char -> String -> (String, String)
splitOn c [] = ("", "")
splitOn c xs = (takeWhile (/= c) xs, drop 1 $ dropWhile (/= c) xs)

main :: IO ()
main = do
  let r = mkStdGen 420
  if fst (scrambleTree r tree) /= scrambledTree then
    die "Not the correct tree!"
  else do
    let l = "SSM{detta_ar_haskell_pa_riktigt_lmao}"
    putStrLn . toString $ scramble r tree l
    putStrLn "Welcome to REAL haskell hours."
    putStrLn "Please input the scrambled flag"
    putStr "> "

    flag <- getLine
    let d = parseBitString `second` splitOn ':' flag

    putStrLn $ "The flag is: " ++ unscramble r tree d
