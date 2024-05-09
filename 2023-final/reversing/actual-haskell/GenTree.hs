{-# LANGUAGE ScopedTypeVariables #-}
module GenTree where

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

data Tree a = Leaf a | Node (Tree a) (Tree a) deriving (Show)

lazyTail :: [a] -> [a]
lazyTail [] = []
lazyTail xs = tail xs

pop :: Int -> [a] -> (a, [a])
pop n xs = (xs !! n, uncurry (++) $ lazyTail `second` splitAt n xs)

push :: Int -> a -> [a] -> [a]
push n x xs = uncurry (++) $ (x:) `second` splitAt n xs

randomTreeInternal :: RandomGen b => [Tree a] -> Rand b (Tree a)
randomTreeInternal [x] = return x
randomTreeInternal xs = do
  na :: Int <- getRandomR (0, length xs - 1)
  let (a, xs') = pop na xs
  nb :: Int <- getRandomR (0, length xs' - 1)
  let (b, xs'') = pop nb xs'
  nr :: Int <- getRandomR (0, length xs'' - 1)
  let xs''' = push nr (Node a b) xs''
  randomTreeInternal xs'''

randomTree :: RandomGen b => b -> [a] -> Tree a
randomTree r xs = evalRand (randomTreeInternal $ map Leaf xs) r

tree = randomTree (mkStdGen 69) $ ['a'..'z'] ++ ['A'..'Z'] ++ ['0'..'9'] ++ "{}_"
