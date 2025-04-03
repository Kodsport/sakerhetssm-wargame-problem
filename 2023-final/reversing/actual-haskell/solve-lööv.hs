{-# LANGUAGE RecursiveDo, LambdaCase #-}
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

data Tree a = Leaf a | Node (Tree a) (Tree a) deriving (Eq, Show)
data Bit = One | Zero deriving (Eq)
type BitString = [Bit]

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

scramble :: RandomGen r => Tree a -> Rand r (Tree a)
scramble x = do
  r <- getRandom
  if leaf x then return x else do
    y <- scramble (left x)
    z <- scramble (right x)

    return (bool flip id r Node z y)


scrambleTree :: (Eq a, RandomGen b) => b -> Tree a -> (Tree a, b)
scrambleTree r t = runRand (scramble t) r

-- hii
unscrambleT :: RandomGen r => RandT r (Tardis (Tree a) (Tree a)) ()
unscrambleT = mdo
  x <- lift getPast
  r <- getRandom
  if leaf x then lift $ sendPast x else mdo
    if r then mdo
        lift $ sendPast (Node z y)
        z <- lift getFuture
        lift $ sendFuture (right x)
        unscrambleT
        y <- lift getFuture
        lift $ sendFuture (left x)
        unscrambleT
    else mdo
        lift $ sendPast (Node y z)
        y <- lift getFuture
        lift $ sendFuture (left x)
        unscrambleT
        z <- lift getFuture
        lift $ sendFuture (right x)
        unscrambleT


-- scrambleTree :: (Eq a, RandomGen b) => b -> Tree a -> (Tree a, b)
-- scrambleTree r t = (a, b)
--   where ((_, b), (a, _)) = runTardis (runRandT scrambleT r) (undefined, t)

unscrambleTree :: (Eq a, RandomGen b) => b -> Tree a -> (Tree a, b)
unscrambleTree r t = (a, b)
  where ((_, b), (a, _)) = runTardis (runRandT unscrambleT r) (undefined, t)

unscramble :: (Eq a, RandomGen b) => b -> Tree a -> ([a], BitString) -> [a]
unscramble r t (l, xs) = fst (decode t . flips bs . (++ xs) . encode t' $ l)
  where (t', r') = scrambleTree r t
        bs = randoms r'

tree :: Tree Char
tree = fst $ unscrambleTree (mkStdGen 420) scrambledTree -- FIXME: We lost the tree :(

scrambledTree :: Tree Char
scrambledTree = Node (Node (Node (Node (Node (Node (Leaf '0') (Node (Node (Leaf 'H') (Leaf 'f')) (Leaf 'a'))) (Leaf 'p')) (Leaf 's')) (Node (Node (Leaf '}') (Leaf 'R')) (Leaf 'E'))) (Node (Node (Node (Node (Leaf 'K') (Node (Leaf '3') (Leaf 'O'))) (Node (Node (Leaf '9') (Leaf 'v')) (Node (Leaf 'I') (Node (Leaf 'e') (Leaf 'V'))))) (Node (Leaf 'G') (Leaf '7'))) (Node (Node (Node (Node (Node (Leaf 'Q') (Leaf '{')) (Leaf 'l')) (Node (Node (Leaf 'd') (Leaf '5')) (Node (Node (Leaf 'C') (Leaf 'k')) (Leaf 't')))) (Node (Leaf 'S') (Node (Node (Node (Node (Node (Leaf 'j') (Node (Leaf 'h') (Leaf 'X'))) (Node (Leaf 'J') (Leaf 'c'))) (Node (Leaf 'B') (Leaf 'F'))) (Node (Leaf 'U') (Node (Leaf 'M') (Leaf 'm')))) (Leaf '1')))) (Node (Node (Leaf 'T') (Leaf 'Y')) (Node (Leaf 'A') (Leaf 'w')))))) (Node (Node (Node (Node (Node (Node (Node (Leaf 'i') (Leaf 'b')) (Node (Leaf 'x') (Node (Leaf 'o') (Leaf 'D')))) (Leaf '_')) (Node (Leaf 'Z') (Node (Node (Node (Leaf '8') (Node (Node (Leaf '6') (Leaf '2')) (Leaf 'W'))) (Leaf 'g')) (Leaf 'P')))) (Node (Node (Leaf 'u') (Leaf 'L')) (Leaf 'z'))) (Node (Node (Node (Leaf 'r') (Leaf 'n')) (Leaf 'N')) (Leaf '4'))) (Node (Leaf 'y') (Leaf 'q')))

splitOn :: Char -> String -> (String, String)
splitOn c [] = ("", "")
splitOn c xs = (takeWhile (/= c) xs, drop 1 $ dropWhile (/= c) xs)

main :: IO ()
main = do
  let r = mkStdGen 420

  if fst (scrambleTree r tree) /= scrambledTree then
    die "Not the correct tree!"
  else do
    putStrLn "Welcome to REAL haskell hours."
    putStrLn "Please input the encrypted flag"
    putStr "> "

    flag <- (reverse . dropWhile isSpace . reverse) <$> readFile "encrypted.txt"
    let d = parseBitString `second` splitOn ':' flag

    putStrLn $ "tree = " ++ show tree
    putStrLn $ "The flag is: " ++ unscramble r tree d

