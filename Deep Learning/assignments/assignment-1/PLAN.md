# Assignment 1: Plan of Action

## 1. The problem in plain words

We have 5,108 small aerial photos of land (each 256×256 pixels). For every photo there is a matching black-and-white "answer sheet" (a **mask**): white where the ground is forest, black where it isn't.

We need to teach a computer to look at a new photo and paint its own black-and-white answer sheet.

The real point of the assignment is a **comparison** between two ways of teaching the same model:

| | Model A: "From scratch" | Model B: "Transfer learning" |
|---|---|---|
| Starting point | Knows nothing. Starts with random guesses. | Starts with a model that already learned to recognise everyday objects from 1 million general photos (ImageNet). |
| Training | 100 rounds, the whole model learns. | 50 rounds where only the "painting" half learns and the "seeing" half stays locked, then 50 rounds where everything learns. |

The model has two halves:
- **Seeing half (encoder):** looks at the photo and picks out patterns. We use a well-known design called ResNet50.
- **Painting half (decoder):** turns those patterns back into a full-size black-and-white answer sheet.

Together this shape is called a **U-Net**.

At the end we answer two questions:
1. **Which model is more accurate?**
2. **Which one took longer to train, and was the extra accuracy worth the extra time?**

One **round (epoch)** means the model has seen every training photo once.

---

## 2. What we found when we looked at the data

We checked the data before planning. These facts shaped the decisions below:

| Finding | Why it matters |
|---|---|
| All photos are 256×256 and every photo has a matching mask. | Nothing is missing, so no clean-up is needed. |
| The masks are saved as JPG, so their pixels are not purely black and white. We saw values like 1, 2, 3, 250 and 253 instead of just 0 and 255. | We must snap every mask pixel to pure black or pure white. Otherwise the answer sheets are slightly wrong. |
| About 62% of all pixels are forest. Roughly 4% of photos have almost no forest and 6% are completely forest. | The two classes are fairly balanced, so no special balancing trick is needed. But "accuracy" alone would flatter the models, which is why IoU is the main score. |
| The 5,108 photos were cut from only **190 large satellite images**, about 27 pieces each. | **Important.** Neighbouring pieces of the same big image look almost identical. If one piece is used for training and its neighbour for testing, the test is too easy and the scores are inflated. |

---

## 3. Decisions, one by one

For each decision: the options, the pros and cons, and the final choice.

### 3.1 Where to run things

| Option | Pros | Cons |
|---|---|---|
| Everything on the laptop | Full control, no upload step | The laptop GPU is small (4 GB, 45 W). The laptop must stay awake for hours. |
| Everything on Kaggle | Faster GPU, runs in the background, saves the notebook with all outputs | Slower to debug small mistakes, and the weekly GPU allowance is limited |
| **Quick checks on laptop, full run on Kaggle** | Catch mistakes cheaply, then run once on Kaggle | Two places to keep in sync |

**Decision:** Do the quick checks on the laptop with only a few rounds. Then run the full 100 + 100 rounds on Kaggle.

*Update after measuring:* the laptop turned out faster than expected, about 13 seconds per round. The full job would take roughly an hour locally, so the laptop is a solid backup if Kaggle causes trouble.

### 3.2 Which library

The assignment says "segmentation_models". That name belongs to two libraries by the same author: one older version for Keras/TensorFlow, and one PyTorch version called `segmentation_models_pytorch`.

| Option | Pros | Cons |
|---|---|---|
| Keras version | Matches the name in the assignment exactly | Broken with current TensorFlow without workarounds. Not maintained. |
| **PyTorch version** | Actively maintained, already installed, works cleanly on Kaggle | Slightly different name |

**Decision:** Use the PyTorch version (`segmentation_models_pytorch`). Add one line in the notebook explaining the choice.

### 3.3 How to split the photos into train, check and test groups

We need three groups:
- **Train:** photos the model learns from.
- **Validation:** photos we use during training to see how it's going.
- **Test:** photos kept locked away until the very end for the final scores.

| Option | Pros | Cons |
|---|---|---|
| Shuffle all 5,108 pieces randomly | Simple, and it's what most online notebooks do | Neighbouring pieces end up on both sides, so the test becomes too easy and the scores look better than they really are |
| **Split by the 190 big source images** | Honest test: the model is scored on land it has truly never seen | Scores will look a little lower. Group sizes will be close to the target but not exact. |

**Decision:** Split by source image into about **70% train, 15% validation and 15% test**. All pieces of one big image go into the same group. Use a fixed random seed so both models get exactly the same split. We will mention this choice in the report, because it's a sign of careful work.

### 3.4 Image size

| Option | Pros | Cons |
|---|---|---|
| **128×128 (shrink)** | Suggested by the assignment. About 4 times faster to train. | Loses some fine detail at forest edges |
| 256×256 (original) | Sharper edges, possibly slightly better scores | About 4 times the training cost for both 100-round runs |

**Decision:** 128×128, as the assignment suggests. We shrink the masks to 128 as well and snap them back to pure black and white afterwards.

### 3.5 Preparing the pixel values (normalisation)

The assignment requires scaling pixel values from 0–255 down to 0–1. The pre-trained model also learned on photos that were adjusted in one more small way: each colour channel shifted by a fixed amount (the "ImageNet average").

| Option | Pros | Cons |
|---|---|---|
| 0–1 scaling only | Simplest and matches the text exactly | The pre-trained model sees inputs slightly different from what it's used to, which is unfair to Model B |
| **0–1 scaling, then the ImageNet adjustment, for both models** | Meets the requirement. The pre-trained model sees familiar-looking input. Both models get identical input, so the comparison stays fair. | One extra line of code |

**Decision:** Scale to 0–1, then apply the ImageNet adjustment. Do the same for **both** models.

### 3.6 Creating extra variety in the training photos (augmentation)

Randomly flipping or rotating training photos gives the model more variety to learn from.

| Option | Pros | Cons |
|---|---|---|
| None | Simplest | Over 100 rounds the models may start memorising the training photos, especially Model A |
| **Light: flips and 90° turns only** | Aerial photos have no "up", so a flipped forest is still a forest. Reduces memorising. Costs almost nothing. | Tiny extra code |
| Heavy: colour changes, zoom, blur and so on | Even more variety | More things to tune and explain. Could distort what forest looks like. |

**Decision:** Light only: random horizontal flip, vertical flip and 90° turns. We apply them to the training photos only, never to validation or test, and identically for both models.

### 3.7 How we measure "wrong" during training (loss)

| Option | Pros | Cons |
|---|---|---|
| Pixel-by-pixel error only (BCE) | Stable and standard | Doesn't directly reward getting the *shape* of the forest right |
| Overlap error only (Dice) | Directly rewards good overlap with the true forest area | Can be jumpy early in training |
| **Both added together (BCE + Dice)** | Stable *and* shape-aware. Recommended by the assignment. | None worth mentioning |

**Decision:** BCE + Dice, weighted equally.

### 3.8 How the model adjusts itself (optimizer and step size)

The **learning rate** is how big a correction the model makes after each mistake. Big steps learn fast but are rough. Small steps are careful but slow.

| Setting | Model A (scratch) | Model B, phase 1 (locked seeing half) | Model B, phase 2 (all unlocked) |
|---|---|---|---|
| Optimizer | AdamW (Adam + a gentle size penalty, see 3.14) | AdamW | AdamW (restarted fresh) |
| Starting step size | 0.001 | 0.001 | **0.0001** (10× smaller) |
| Step size over time | Slowly shrinks to near zero by round 100 | Shrinks over its 50 rounds | Shrinks over its 50 rounds |

**Why a smaller step size in phase 2:** when we unlock the pre-trained seeing half, big steps would wreck the useful knowledge it already has. Small steps gently adjust it to forest photos instead. This is standard practice for fine-tuning.

**Why the step size shrinks over time:** make big corrections early, then fine-tune carefully near the end. We use a smooth "cosine" curve for this.

### 3.9 Should we use Optuna (automatic hyperparameter search)?

Optuna automatically tries many settings, such as step size and batch size, and keeps the best.

| For Optuna | Against Optuna |
|---|---|
| Might find slightly better settings | Each try needs many training rounds. Twenty tries would cost about twenty times the compute and eat through the weekly Kaggle allowance. |
| Looks thorough | The assignment is a **comparison**, not a race for the highest score. Settings that are fair and identical for both models matter more than perfect ones. |
| | If we tune one model more than the other, the comparison becomes unfair. Tuning both properly doubles the cost again. |
| | The assignment only asks us to *document* our choices, not to search for them |

**Decision: No Optuna.** We use well-known, sensible defaults and apply the same ones to both models. Optional extra: a quick check on the laptop of 2–3 step sizes for about 5 rounds each, only to confirm 0.001 isn't obviously bad.

### 3.10 Early stopping, and which saved version to score

**Early stopping** means ending training once it stops improving. The assignment requires exactly 100 rounds, so we **don't stop early**.

After many rounds a model can start memorising and actually get slightly worse on new photos.

| Option | Pros | Cons |
|---|---|---|
| Score the model as it is after round 100 | Literally "the final model" | Might score a version that has started memorising |
| **Save the best version seen during training (judged on the validation group) and score that on the test group** | Standard practice. Scores each model at its best, which is fairer. | Needs one extra line to save the model |

**Decision:** Train the full 100 rounds. Keep the version with the best validation score. Report its test scores as the main result. Also show the round-100 scores in a small side column, for completeness.

### 3.11 Keeping the time comparison fair

Training time is a required result, so it must be measured cleanly:
- Load all photos into memory **once, before the timers start**, so disk reading doesn't favour either model.
- Time only the training loop, including the per-round validation check, and use the same method for both models.
- Run both models **in the same Kaggle session on the same GPU**, one after the other.
- Record the time of every round, not just the total. Model B's locked phase should be clearly faster per round, and that's worth pointing out in the analysis.

### 3.12 Locking the seeing half properly (Model B, phase 1)

"Locking" has two parts, and online code often forgets the second:
1. Stop its weights from changing.
2. Stop its internal running averages from updating. These are small counters inside the model (batch-norm statistics) that silently keep changing even when the weights are locked, unless we explicitly freeze them.

**Decision:** Do both. In phase 2, unlock both.

### 3.13 Other settings

| Setting | Choice | Reason |
|---|---|---|
| Photos per training step (batch size) | 32 everywhere | Measured on the laptop: uses only about 1.3 GB with the setting below, so it fits on both machines |
| Faster maths (mixed precision) | On, for both models | Measured about 1.4× faster and 3× less memory on the laptop. Scores are unaffected. |
| Kaggle GPU | **T4** (use one of the two) | Kaggle's current PyTorch **doesn't work on the P100**: the P100 is too old, so any calculation crashes. The T4 is supported and benefits from mixed precision. |
| Random seed | Fixed (42) everywhere | Same split and repeatable results |
| Forest/not-forest cut-off | 0.5 | If the model is more than 50% sure a pixel is forest, call it forest |
| Saving progress | Save the model and a per-round log file after training | If something crashes, we don't lose everything |

### 3.14 Do we need regularisation? (ways to stop memorising)

**Regularisation** is any trick that stops a model memorising its training photos, so that it does well on new photos instead.

**Why we need to think about it:** the model has 32.5 million adjustable numbers and trains for 100 rounds on about 3,500 photos. Model A especially, since it starts from nothing, could start memorising in the later rounds.

**What is already working in our favour:**
- Every photo contains 16,384 pixel answers, not just one label, so there is far more to learn from than "3,500 photos" suggests.
- The flips and turns from 3.6 already add variety.
- The model's built-in "running average" layers (batch normalisation) add a mild steadying effect.
- Keeping the best version (3.10) acts as a safety net: if the model starts memorising late, we simply don't use those later versions.

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| Light flips/turns | Free and suits aerial photos | none | **Yes** (already chosen in 3.6) |
| Gentle size penalty (weight decay 0.0001, via AdamW) | Standard and costs nothing. Nudges the model toward simpler solutions. | One more number to state | **Yes** |
| Keep the best version by validation score | Protects against late memorising | none | **Yes** (already chosen in 3.10) |
| Dropout (randomly switching off parts during training) | Strong anti-memorising tool | The ready-made U-Net has no slot for it, so we'd have to change the standard model. It also clashes with batch normalisation. Changing the "standard U-Net" is against the assignment's spirit. | No |
| Heavy colour and zoom changes | More variety | More settings. Could distort what forest looks like. | No |
| Stop training early | Classic tool | The assignment requires exactly 100 rounds | No |

**Decision:** Light regularisation, applied identically to both models: flips and turns, plus a gentle size penalty (weight decay 0.0001), plus keeping the best version.

**How we check it worked:** we plot the training score next to the validation score. If the two lines drift far apart late in training while the validation score falls, that's memorising. We report what we see honestly, but we **don't re-tune in the middle of the experiment**, because changing one model's settings would break the fair comparison.

---

## 4. How we'll score the models

All scores are computed on the **test group**. We count every pixel across all test photos together, then compute:

| Score | Plain meaning |
|---|---|
| **IoU (main score)** | Take the predicted forest area and the true forest area. IoU is their overlap divided by their combined area. 1.0 is perfect. |
| Accuracy | Share of all pixels labelled correctly. This looks high even for mediocre models, because most pixels are easy. |
| Precision | Of the pixels we *called* forest, how many really were forest? (Few false alarms?) |
| Recall | Of the pixels that *really are* forest, how many did we find? (Little missed?) |
| F1 | A single balance of precision and recall. The analysis section asks for it. |

---

## 5. Final course of action

### Stage 1: Sanity checks on the laptop (a few minutes each)
1. Load the list of photos and check that every photo has a mask.
2. Show 3–4 photos next to their masks, to confirm they line up and that snapping to black and white works.
3. Do the split by source image and print how many photos and big images land in each group. Confirm no big image appears in two groups.
4. Build both models and push one batch through them, to check that the input and output shapes are right.
5. **"Memorise a handful" test:** train on about 8 photos for a short while. The error should drop close to zero. If it doesn't, something is broken.
6. Run 2 rounds of Model A and 2 rounds of Model B (1 locked + 1 unlocked). Check that the timers, the saving and the score table all work.

### Stage 2: The full run on Kaggle (one notebook, one session, T4)
1. Attach the dataset and set the GPU to "GPU T4 x2". Only one of the two GPUs is used.
2. Run Model A for 100 rounds, saving the best version and the per-round log.
3. Run Model B for 50 locked rounds, then 50 unlocked rounds with the smaller step size, again saving the best version and the log.
4. Use **"Save & Run All"** so it runs in the background and keeps every output.

### Stage 3: Results and write-up (in the same notebook)
1. **Score table:** IoU, Accuracy, Precision, Recall and F1 for both models (best version, plus round-100 for completeness).
2. **Training curves:** error and IoU per round for both models on one chart. Model B's jump at round 50, when it's unlocked, should be visible.
3. **Time table:** total training time, and average time per round (phase 1 and phase 2 shown separately for Model B).
4. **Side-by-side pictures** for 3–4 test photos: original, true mask, Model A's guess, Model B's guess. Include at least one hard example.
5. **Short analysis:**
   - Which model scored higher, and why. (Expected: Model B, because it starts out already knowing edges, textures and shapes.)
   - Time versus accuracy. (Expected: Model B is faster overall thanks to the cheaper locked phase, and more accurate.)
   - One or two sentences on the honest split, and why our scores may be lower than online notebooks that shuffle randomly.
6. Download the finished notebook with all outputs from Kaggle and submit it.

### Notebook outline
1. Title and short problem summary
2. Setup (libraries, seed, device)
3. Data loading and checks
4. Train/validation/test split by source image
5. Preparation and augmentation
6. Model, loss, scores and training loop (shared by both experiments)
7. Experiment 1: from scratch
8. Experiment 2: transfer learning (phase 1 and phase 2)
9. Test results table
10. Training curves and time comparison
11. Visual comparison
12. Analysis and conclusion
13. Documented choices (short summary of section 3 of this plan)
