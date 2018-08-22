# hawkBlackBox
Implementation of Hawk's Black Box to do experiments and get some statistics.

Clone the repository or download the `hawkBlackBox.py` script.
Run it with `./hawkBlackBox.py`. By default, it will display the available
strategies.

```console
$ ./hawkBlackBox.py
AVAILABLE STRATEGIES
============================================
BtoS: From Rank B to Rank S, Same Rank / Random Type combinations

    This strategy always combines devices with the same Rank: 4xB, 4xA
    or 4xS. It does not take the device's type into account (they are
    picked randomly). It starts at Rank B and goes up to Rank S. It does
    not try to maximize the number of stars for the final S-Rank devices.

    Usage:
        ./hawkBlackBox.py  BtoS  stabilizer_level  number_of_green_devices_to_start_with

    Example:
        ./hawkBlackBox.py  BtoS  0  100000
```

You can call a strategy like shown in the usage (using its code name):

```console
$ ./hawkBlackBox.py BtoS 0 100000
Running "From Rank B to Rank S, Same Rank / Random Type combinations" strategy
With Stabilizer level 0 and 100000 B-rank devices

Results phase 1
---------------
A-rank 0-star devices obtained: 961
A-rank 1-star devices obtained: 11128
S-rank 1-star devices obtained: 589

B-rank devices left:
No devices

Results phase 2
---------------
S-rank 0-star devices obtained: 349
S-rank 1-star devices obtained: 1037 (total: 1626)

A-rank devices left:
A-rank 0-star Armor device

Statistics
----------
B-rank devices used: 100000
Total combinations done: 32674
Average number of B-rank devices to get an S-rank device: 50.63
```

#### Contributions welcome!
We need the probabilities for the stabilizer levels 25, 50, 75 and 100.

Look at the code to implement new strategies, or just play from within a Python console.

#### Have fun!
