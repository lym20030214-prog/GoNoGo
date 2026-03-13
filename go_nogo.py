## go no go
# Hi, I’m trying to adapt a GO/NOGO protocol from Price et al., 2016. Food-specific
# response inhibition, dietary restraint and snack intake in lean and overweight/obese adults.
# The task consists in 50 trials (40 go and 10 no-go). During go trials the
# subject should press a key as fast as possible. During no-go trials, no key should
# be pressed.
# Each trial is composed by an image presented for 750ms and was separated by a
# blank screen for 500 ms and preceded by a fixation cross for 500 ms.
# The sequence of go/nogo stimuli are predetermined.
# Two set of images are used: 10 go images (each one is presented 4 times) and 10
# no-go images (each one is presented one time). Image order should be randomized across
# subjects.
# we are going to change for anorexia nervosa intervention

import os
import pandas as pd
from psychopy.gui import DlgFromDict
from psychopy.visual import Window, TextStim, ImageStim
from psychopy.core import Clock, quit, wait
from psychopy.event import Mouse
from psychopy.hardware.keyboard import Keyboard


# Participant info
exp_info = {'participant_nr': '', 'age': ''}
dlg = DlgFromDict(exp_info)

if not dlg.OK:
    quit()

p_name = exp_info['participant_nr']

# Window
win = Window(size=(1200, 800), fullscr=False)
mouse = Mouse(visible=False)
clock = Clock()
kb = Keyboard()


f_list = "/Users/linyiming/Documents/grad/26 SS/CCPX 5199/module 7/HF_LF_60.csv"
foods = pd.read_csv(f_list)

hf = foods[foods['fat'] == 1]   # no-go
lf = foods[foods['fat'] == 0]   # go

lf_sample = lf.sample(n=10).copy()
hf_sample = hf.sample(n=10).copy()

trial_foods = pd.concat(
    [lf_sample, lf_sample, lf_sample, lf_sample, hf_sample],
    ignore_index=True
)
trial_foods = trial_foods.sample(frac=1).reset_index(drop=True)

stim_folder = "/Users/linyiming/Documents/grad/26 SS/CCPX 5199/module 3/Food-Choice-Task-main/stimuli"

trial_foods["correct"] = ""
trial_foods["response"] = ""
trial_foods["rt"] = ""
trial_foods["accuracy"] = ""

# Instructions
instructions = TextStim(
    win,
    text=(
        "Welcome to the task.\n\n"
        "On each trial, you will see a food picture and a cue.\n\n"
        "If the cue says GO:\n"
        "Press the SPACE BAR as quickly as possible.\n\n"
        "If the cue says NO-GO:\n"
        "Do NOT press anything.\n\n"
        "Try to respond quickly and accurately.\n\n"
        "Press SPACE to begin."
    ),
    color="white",
    height=0.05,
    wrapWidth=1.4
)

instructions.draw()
win.flip()

while True:
    keys = kb.getKeys(['space', 'escape'], waitRelease=False)
    if keys:
        if keys[0].name == 'escape':
            win.close()
            quit()
        elif keys[0].name == 'space':
            break

# Run trials
for i in range(len(trial_foods)):
    trial = trial_foods.iloc[i]

    fixation = TextStim(win, text="+", color="white", height=0.08)
    fixation.draw()
    win.flip()
    wait(0.5)

    path = os.path.join(stim_folder, trial["food"])
    print("Stimulus:", path)

    if trial["fat"] == 1:
        correct = "nogo"
        cue_text = "NO-GO"
    else:
        correct = "go"
        cue_text = "GO"

    im = ImageStim(win, image=path, size=(0.8, 0.8), pos=(0, 0))

    cue = TextStim(
        win,
        text=cue_text,
        color="white",
        height=0.07,
        pos=(0, 0.65)
    )

    kb.clearEvents()
    kb.clock.reset()

    response = "nogo"
    rt = "NA"

    t_clock = Clock()
    while t_clock.getTime() < 0.75:
        cue.draw()
        im.draw()
        win.flip()

        keys = kb.getKeys(['space', 'escape'], waitRelease=False)
        if keys and response == "nogo":
            resp = keys[0].name
            if resp == 'escape':
                win.close()
                quit()
            elif resp == 'space':
                response = "go"
                rt = keys[0].rt

    win.flip()
    wait(0.5)

    if response == correct:
        accuracy = 1
    else:
        accuracy = 0

    trial_foods.loc[i, "correct"] = correct
    trial_foods.loc[i, "response"] = response
    trial_foods.loc[i, "rt"] = rt
    trial_foods.loc[i, "accuracy"] = accuracy

end_text = TextStim(
    win,
    text="Thank you for participating!\n\nPress SPACE to exit.",
    color="white",
    height=0.06
)

end_text.draw()
win.flip()

while True:
    keys = kb.getKeys(['space', 'escape'], waitRelease=False)
    if keys:
        break

trial_foods.to_csv(f"{p_name}_gonogo.csv", index=False)

win.close()
quit()