# Task 02 — Derivation of Gustafson's Scaled Speedup

## Step 1. Normalize the parallel run

We run the program on P cores and measure its time. We split this time into two parts:

- `s` = time of the serial part (only one core works),
- `p` = time of the parallel part (all P cores work).

We normalize the total parallel time to 1:

```
T(P) = s + p = 1                                   (1)
```

*Why:* we only care about ratios of times, so we can choose the unit of time.

## Step 2. Find the equivalent serial workload

Now imagine running **the same job** on one core.

- The serial part still takes `s` (it was done by one core anyway).
- In the parallel part, P cores each worked for time `p`. One core must do all of that work, so it needs `P · p`.

```
T(1) = s + P · p                                   (2)
```

*Why:* the work is conserved. P cores × time p = P·p core-seconds of work.

## Step 3. Speedup definition

```
S(P) = T(1) / T(P) = (s + P·p) / (s + p)           (3)
```

Using (1), the denominator is 1:

```
S(P) = s + p · P                                   (4)
```

This is Gustafson's law in the first form.

## Step 4. Write it with the serial fraction α

Because of the normalization, the serial fraction observed on the parallel machine is

```
α = s / (s + p) = s        and       p = 1 − α     (5)
```

Put (5) into (4):

```
S(P) = α + (1 − α)·P                               (6)
     = α + P − α·P                                 (7)
     = P − α·P + α                                 (8)
     = P − α(P − 1)                                (9)   ∎
```

## Step 5. Checks

- `P = 1` → `S = 1 − 0 = 1` ✔ (one core gives no speedup)
- `α = 0` → `S = P` ✔ (perfect linear speedup)
- `α = 1` → `S = 1` ✔ (fully serial program)
- Slope `dS/dP = 1 − α` is constant, so the speedup is a straight line with slope `1 − α`.

## Step 6. Efficiency (used later)

```
E(P) = S(P)/P = 1 − α·(P − 1)/P
```
