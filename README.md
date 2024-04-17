# Pixelfuzz

## Pixelfuzz extends AFL to fuzz GUI applications

afl directory - `/home/prikshit/work/asst/AFL - ./afl-fuzz`

afl-fuzz.c contains codebase of afl-fuzz

Compile afl-fuzz.c -> `make afl-fuzz`

Projects in - `/home/prikshit/work/asst`

If you open a new terminal set -

`export AFL_SKIP_CPUFREQ=1`

## Connect to display

`xhost +`

## Command to run -

### Black box fuzzing with AFL -

`afl-fuzz -t 30000+ -i in -o out -g calc/clicks.py -n -m none -- calc/gnome-calculator`

### Instrumented fuzzing with AFL -

`afl-fuzz -t 30000+ -i in -o out -g matefuzz/clicks.py -m none -- matefuzz/gnome-calculator`

### Fuzzing in Qemu mode -

`afl-fuzz -t 30000+ -i in -o out -g calc/clicks.py -Q -m none -- calc/gnome-calculator`

## Using xwininfo for boundary detection -

```
xwininfo: Window id: 0x3800004 "Calculator"

Absolute upper-left X: 24
Absolute upper-left Y: 54
Relative upper-left X: 24
Relative upper-left Y: 54
Width: 412
Height: 541
Depth: 32
Visual: 0x2b9
Visual Class: TrueColor
Border width: 0
Class: InputOutput
Colormap: 0x3800003 (not installed)
Bit Gravity State: NorthWestGravity
Window Gravity State: NorthWestGravity
Backing Store State: NotUseful
Save Under State: no
Map State: IsViewable
Override Redirect State: no
Corners: +24+54 -1004+54 -1004-305 +24-305
-geometry 412x541+24+54

start x location : 52
start y location : 79
```

For Qemu mode - add time.sleep(25)
