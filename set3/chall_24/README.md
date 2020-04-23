I deliberately implemented this in a different manner than what comes to mind intuitively

Initially I thought of implementing it such that each output of the RNG is broken into 4 bytes and that is used as the keystream. Here, there is no loss of information as the entire output is used in the key.

Instead if we used mod(output, 256) as each byte of the keystream, there is a loss of 24 bits .
I wanted to test if the attack could still work and thus I implemented it this way.

