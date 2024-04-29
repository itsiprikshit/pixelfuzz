# Pixelfuzz

Pixelfuzz extends AFL to fuzz GUI applications

## Introduction

GUI Fuzzing is not a common practice, and even AFL claims that it can only be done by making source changes.
This project aims to make the required changes in the source code of AFL so that we can fuzz the application with GUI by interacting with the GUI.<br>

There are three main steps in this project -<br>

-   Target discovery (a GUI application)
-   Target initialization and interaction framework invocation (Initializing the target application and the interaction framework from AFL)
-   Interacting with the GUI based on the generated seed

> We used Ubuntu 22.04 to work on this project and forked the repository.
> The link to our AFL fork is [here](https://github.com/itsiprikshit/AFL).

## Target discovery

We chose a target program for fuzzing using AFL, focusing on one that would facilitate instrumentation. Given our criteria, we considered several GUI applications based on C/C++.

Eventually, we selected the following:<br>

-   <b>Gnome calculator</b>, written in Vala. Vala compiles to C using gcc. This choice allowed us to use a language that compiles into C, thereby maintaining our focus on C/C++ for compatibility with AFL. The gnome calculator is the default calculator in Ubuntu 2022 (<b>/usr/bin/gnome-calculator</b>).

*   <b>Mate calculator</b>, written in C and compiled using `afl-gcc` to ensure the fuzzing instrumentation was incorporated. You can find the source code for mate calc [here](https://github.com/mate-desktop/mate-calc).

## Fuzzing and Interaction Framework invocation

There are two ways to initialize fuzzing of binaries in AFL -<br>

-   Keep executing the binary over and over again on each run with `execv`
-   Load the target binary beforehand and stop right before the execution (at main())<br>

Once the binary is loaded, we invoke our interaction framework, a script written in Python.
The path to the Python script is passed as an argument to afl-fuzz using the `-g` flag, which also sets the `gui_mode`.

```
if (gui_mode) {
    python_pid = fork();
    if (!python_pid) {
        char *pargs[] = {"/usr/bin/python3", gui_dir, NULL};
        execv("/usr/bin/python3", pargs);
        exit(0);
    }
}
```

AFL forks a Python process that runs the interaction framework script after running the target binary.
You can see all the changes to AFL’s source code in `afl-fuzz.c` [here](https://github.com/google/AFL/compare/master...itsiprikshit:AFL:master).

## Building AFL -

When you make any changes to afl-fuzz.c, it's important to recompile it. You can compile the fuzzer by running the `make afl-fuzz` command from the root source directory.

## Seed

The current seed used by the target application is encoded in `ISO-8859-1` format and written in the `.cur-input` file in the out directory.

The Python script being invoked takes care of reading this seed and converting them to a sequence of 10 random clicks within the GUI.

## Pseudo-random number generator

To convert a seed string to a random number, we first used a `Fowler–Noll–Vo hash function(FNV-1a hash)`, a fast, non-cryptographic hash algorithm with good dispersion.

The output from FNV-1a is sent to `sfc32`, a pseudorandom number generator (PRNG) that generates a sequence of pseudorandom numbers in the range [0,1).

It ensures that the same seed results in an identical sequence of random numbers (deterministic behavior).

```
seed = open(‘.cur_input’)
random = generate_random(seed)
num1 = random()
num2 = random()
num3 = random()
```

Using this, we generate 10 random numbers.

## Random number translation to clicks

We used the `PyAutoGUI` library to interact with the active screen.
To obtain the target program details like height, width, top_left(x, y) coordinates, etc, we used ‘xwininfo’ and ‘xdotool’ libraries.
The command that gets the active GUI dimensions:
`xwininfo -id $(xdotool getactivewindow)`

Every click needs an x and y coordinate, hence <br>
`x_coord = start_x + width * random_number`<br>
`y_coord = start_y + height * random_number`

Once all the 10 random numbers are converted to clicks, we close the application by providing keyboard input, i.e., `CTRL + Q`.

```
pyautogui.keyDown('ctrlleft')
pyautogui.press('q')
pyautogui.keyUp('ctrlleft')
```

Once the calculator is closed, it returns to the afl to denote that the target application has been successfully closed.

You can find the interaction script [here](https://github.com/itsiprikshit/pixelfuzz/blob/main/clicks.py).

> Note: When fuzzing in Qemu mode, add an appropriate sleep in the clicks.py to ensure the target program is open and running before it starts interacting with the GUI. The sleep needs to be added before the random number generator initialization in the script.

## Initiating the fuzz

Before starting the fuzzing campaign, we had to run the following commands to set the fuzzing -

-   We exported the `AFL_SKIP_CPUFREQ=1` to skip the check for the CPU scaling policy.
-   Disabled sending core dump notifications by running the following command - <br>
    `sudo bash -c 'echo core > /proc/sys/kernel/core_pattern'`<br>
-   Finally, we fuzzed the target program as the root user due to some restrictions of pyautogui, which requires root access.
-   To authorize pyautogui to connect to the display, we ran the following command - `xhost +`

You can now run the target program (the GUI application) by running the following command in your terminal - <br>

`afl-fuzz -t 30000+ -i in -o out -g clicks.py -m none -- mate-calculator`

A few important things to note in the command are - <br>

-   Setting a large timeout value using the `-t` flag (we set it to 30 seconds) to ensure the target program doesn’t close early

-   Setting the `-g` flag to enable `gui_mode` and passing the interaction script as an argument
-   Setting the `-m` none to avoid any memory issues

## Replay crashes

If you find crashes, you can replay them using the `clicks.py` interaction script. Run the following command to replay the crashes - <br>

`python3 clicks.py path/to/target-program path/to/crash-file`

Example -
`python3 clicks.py mate-calc out/crashes/id\:000000\,sig\:06\,src\:000000\,op\:flip1\,pos\:0`

## Results

Out of the two target programs, the mate calculator was instrumented with `afl-gcc`. However, the gnome calculator was not.

We ran the GUI fuzzer in three different modes -<br>

-   Dumb mode (black box fuzzing) - enabled using the -n flag <br>
    `afl-fuzz -t 30000+ -i in -o out -g clicks.py -n -m none -- gnome-calculator`

*   Qemu mode - enabled using the -Q flag <br>
    `afl-fuzz -t 30000+ -i in -o out -g calc/clicks.py -Q -m none -- calc/gnome-calculator`
*   Instrumented mode <br>
    `afl-fuzz -t 30000+ -i in -o out -g matefuzz/clicks.py -m none -- mate-calc`

Surprisingly, we found a bug in `mate-calc`, which we ran in instrument mode. To learn more about the bug, we replayed the crash on the mate calculator.

When we did that, the calculator closed unexpectedly and printed the following error -<br>

```
free(): invalid pointer
Aborted (core dumped)
```
