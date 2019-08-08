# Bham-ARTIQ-examples
A repository of simple examples of ARTIQ code

## Examples
#### LED_OnOffPulse.py
Code demonstrating basic use of an LED on the Kasli Board
- Switch LED on
- Switch LED off
- Pulse LED
#### LED_Parallel.py
Code demonstrating "with parallel" and "with sequential" statements by pulsing LEDs on Kasli Board
- Two parallel threads
- One of the parallel threads has sequential code within it
#### TTLout_OnOffPulse.py
Code demonstrating basic use of a TTL output channel 
- Switch TTL output on
- Switch TTL output off
- Pulse TTL output
#### TTLin_SingleRead.py
Code demonstrating basic reading of a TTL input channel
- Reads TTL input (1 or 0)
- Prints TTL input
#### TTLin_Trigger.py
Code demonstrating basic use of TTL input channel as Trigger
- Scans TTL input for rising edges for fixed interval
- Gives TTL output if rising edge is detected in time interval
  - Timing is deterministic between input and output
