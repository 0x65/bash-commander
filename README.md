bash-commander
==============

Looks through your .bash\_history file to give you a report of your
most used commands, and suggests some possible aliases you could use.

Note that if your HISTCONTROL environment variable is set to `erasedups`
this program would have little use. Also, by default your .bash\_history
is updated only when your bash session ends. Type `history -a` to update
your .bash\_history file with your current history.

Takes an optional parameter `-n N`, which causes the program to display
your top N most used commands.

Sample Output
-------------
```
Your top 10 most used commands:
 #1:    vim (143)
 #2:    ./m.sh (63)
 #3:    vim m.sh (56)
 #4:    vim ccsh.sh (53)
 #5:    f (32)
 #6:    ./ccsh.sh (30)
 #7:    echo (25)
 #8:    source ccsh.sh (24)
 #9:    source (24)
 #10:   vim blah (21)

Here are some aliases, and the amount of characters typed you would save per alias:
 vim -> v (2 characters / 286 total)
 ./m.sh -> m (5 characters / 315 total)
 vim m.sh -> vm (6 characters / 336 total)
 vim ccsh.sh -> vc (9 characters / 477 total)
 f -> f (0 characters / 0 total)
 ./ccsh.sh -> c (8 characters / 240 total)
 echo -> e (3 characters / 75 total)
 source ccsh.sh -> sc (12 characters / 288 total)
 source -> s (5 characters / 120 total)
 vim blah -> vb (6 characters / 126 total)

However, if all the aliases were in place, you would save 1883 characters in all - or about 32.4096385542% of your total bash history.
```
