{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE UnboxedTuples #-}

module Solve where
import qualified Data.Text as T
import GHC.Utils.Monad.State hiding (state)
import Control.Applicative

type Text = T.Text
type VarRef = Text

data Value = Variable VarRef | Constant Int
data Op = Mul | Add | Equ
data ConstraintPart = CP {cpOut :: VarRef, cpV1 :: Value, cpOp :: Op, cpV2 :: Value}
data Constraint = C {name :: Text, invar :: VarRef, outvar :: VarRef, parts :: [ConstraintPart]} deriving (Show)

instance Show Value where
  show (Variable s) = T.unpack s
  show (Constant n) = show n

instance Show Op where
  show Mul = "*"
  show Add = "+"
  show Equ = "=="

instance Show ConstraintPart where
  show (CP r v1 op v2) = unwords [T.unpack r, "=", show v1, show op, show v2]

-- Parse a value, either a variable (x, y, etc) or a value (peano form)
parseValue :: Text -> Value
parseValue t
  | T.elem 'Z' t  = Constant $ T.count "S" t
  | otherwise     = Variable t

-- Have to do this since my GHC version doesn't have a builtin for it (NixOS moment)
-- Basically lifts a raw state transformation into the state monad
-- Need to convert from a normal tuple to an unlifted tuple, hence the lambda
state :: (s -> (a, s)) -> State s a
state s = State {runState' = \x -> let (a, b) = s x in (# a, b #)}

both :: (a -> b) -> (a, a) -> (b, b)
both f (a, b) = (f a, f b)

-- Split haystack on all occurrences of needle, removing those occurrences
splitOn :: Text -> Text -> [Text]
splitOn _ "" = []
splitOn needle haystack = let (a, b) = T.breakOn needle haystack in T.strip a : splitOn needle (T.strip $ T.drop (T.length needle) b)

-- This is cursed. But it works, so whatever
splitArg :: Text -> (Text, Text)
splitArg t = both T.strip $
             (T.spanM (\c -> state $ \i -> (c /= ' ' || i /= 0, case c of {'(' -> i + 1; ')' -> i - 1; _ -> i})) t) `evalState` 0

-- Split by spaces, while respecting parenthesis. I.e. ` splitArgs "a (b c) d" = ["a", "(b c)", "d"] `
splitArgs :: Text -> [Text]
splitArgs "" = []
splitArgs t = let (x, xs) = splitArg t in x : splitArgs xs

-- Parse a constraint part in the form of 'PAdd x (S Z) y' for example
parseConstraintPart :: Text -> ConstraintPart
parseConstraintPart t = CP res v1 op v2
  where (op_s:v1_s:v2_s:res:_) = splitArgs t
        op = case op_s of
          "PAdd" -> Add
          "PMul" -> Mul
          "PEq" -> Equ
        (v1, v2) = both parseValue $ (v1_s, v2_s)

-- Parse an entire constraint
-- instance (a,b,c) => Apply cname in out
parseConstraint :: Text -> Constraint
parseConstraint t = C cname inVar outVar parts
  where (parts_t, dat_raw) = both T.strip . T.breakOn "=>" $ t
        parts = map (parseConstraintPart . T.strip) . splitOn "," . T.dropAround (`elem` ("()" :: String)) . T.dropAround (not . (`elem` ("()" :: String))) $ parts_t
        dat = dropWhile (/= "Apply") . splitOn " " . T.strip $ dat_raw
        cname = dat !! 1
        inVar = dat !! 2
        outVar = dat !! 3

-- Finds the equation determining the value of a given variable. Crashes horribly if not found
equationFor :: VarRef -> [ConstraintPart] -> ConstraintPart
equationFor v l
  | (cpOut $ head l) == v = head l
  | otherwise = equationFor v $ tail l

-- Evaluates an equation part, which is an actual operation
evalPart :: Int -> Constraint -> ConstraintPart -> Int
evalPart inv c part = case cpOp part of
  Mul -> a * b
  Add -> a + b
  Equ -> fromEnum $ a == b
  where (a, b) = both (evalValue inv c) $ (cpV1 part, cpV2 part)

-- Evaluates a value, which is either the input variable, a constant, or an unknown
evalValue :: Int -> Constraint -> Value -> Int
evalValue inv c val = case val of
  (Constant n) -> n
  (Variable v) -> if v == invar c then inv else evalPart inv c . equationFor v $ parts c

-- Evaluates a constraint
eval :: Int -> Constraint -> Int
eval inv c = evalPart inv c $ equationFor (outvar c) (parts c)

-- Checks if a constraint is satisfied
satisfiesConstraint :: Constraint -> Int -> Bool
satisfiesConstraint c val = toEnum $ eval val c

alphabet :: String
alphabet = "_abcdefghijklmnopqrstuvwxyz0123456789"

-- Solves a constraint by the highly advanced brute-force algorithm
solveConstraint :: Constraint -> Char
solveConstraint c = (alphabet !!) . head . filter (satisfiesConstraint c) $ [0..]

-- Solves a list of constraints into a string
solveConstraints :: [Constraint] -> String
solveConstraints = liftA solveConstraint

-- Finds all the constraints in the challenge file
findConstraints :: [Text] -> [Text]
findConstraints = filter (\t -> "instance" `T.isPrefixOf` t && "Apply C" `T.isInfixOf` t)

-- Now we go
main :: IO()
main = do
  file <- readFile "../challenge.hs"
  cs <- liftA parseConstraint . findConstraints . map T.pack . lines <$> readFile "../challenge.hs"
  putStrLn . ("SSM{" ++) . (++ "}") . solveConstraints $ cs
