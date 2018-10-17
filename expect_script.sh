#!/usr/bin/expect

spawn ./install.sh
expect -exact "Input an existing directory path:\r"
send -- "/home/noisy/Devel/EOS/eos\r"
expect -exact "Input an existing directory path:\r"
send -- "/home/noisy/Devel/EOS/workspace\r"
expect eof
