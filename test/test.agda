

open import Agda.Builtin.Nat using (Nat; suc; zero; _+_)

module test where

data _even : Nat → Set where
  ZERO : zero even
  STEP : ∀ x → x even → suc (suc x) even

proof₁ : suc (suc (suc (suc zero))) even
proof₁ = ?
