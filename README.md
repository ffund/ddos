# Distributed Denial of Service Attacks
Using GENI to reproduce the results of:
[1] Lau, Felix, et al. "Distributed denial of service attacks." Systems, Man, and Cybernetics, 2000 IEEE International Conference on. Vol. 3. IEEE, 2000.

### Introduction ###
Here we reproduce Figures 4 and 5 of Distributed Denial of Service Attacks paper.
The objective of this experiment is to show how effective Distributed Denial of Service (DDOS) attacks are under two different queueing schemes: Drop Tail and Random Early Detection.
It shows whether or not legitimate users can obtain desired service while a DDOS attack is in process.
Results are verified using a GENI testbed.

It takes about 30 minutes to reproduce my results.

### Background ###
A Denial of Service (DoS) attack is defined as an attempt to make a machine or a resource unavailable to its legitimate users.
When we have more than one source attacing the target, it is called a Distributed DoS (DDoS).
Typically, attackers try to take control of a lot of unique IP addresses (Zombie Machines) and use them to exhaust a resource either on the target machine, or the network that connects legitimate users to the target machine/s.

In this context, it is intersting to see how queueing networks will perform if they are targeted by a DDOS attacks.
Felix Lau et. al tried to find an answer to this question in 2000, and published their results in the paper we cite today.

In their experiment, they have simulated the simplest of DDOS attacks, when a router is targeted by the attacker aiming at overwhelming its queues and authors have analyzed how different queueing management techniques perform under the DDOS attack.
As shown in the figure, a client tries to reach a service through a single hop network with a router connecting it to the server.
Assuming that an attacker takes control of a set of zombie machines connected to the same router, we simulate how he/she can make the service unavailable to the client by targeting the router and overwhelming its queue.
As an outcome, packets will be droped while the attack is in progress and the client will experience a considerable drop in its bandwidth.

![sample.png](https://raw.githubusercontent.com/aaghdai/ddos/master/Figures/sample.png)

The ultimate goal of the router is to forward packets from ligitimate users.
Therefore, the key metric in this experiment is the rate at which client communicates with the server while the attack is in progress.
A rate of zero indicates no connectivity and a rate drop indicates service degradation.

In this project we are interested to reproduce two specific figures from Lau et. al paper.
Figures 4 and 5, which show the performance of the router under DropTail and Random Early Detection (RED) buffer management policies.
Authors of the original paper show that under DropTail attackers can fully deny the client of access to the server, however, under RED, client can still communicate with the server, although at a slower pace and with degraded quality of service.
### Results ###
Figure 4 of [1]:
![fig4.png](https://raw.githubusercontent.com/aaghdai/ddos/master/Figures/fig4.png)

Figure 5 of [1]:
![fig5.png](https://raw.githubusercontent.com/aaghdai/ddos/master/Figures/fig5.png)

Verification of results:
For Fig. 4 I was unable to verify that the client receive no bandwidth. Instead, the experiment shows that the client experiences a noticable rate drop:
![tbf.png](https://raw.githubusercontent.com/aaghdai/ddos/master/Results/tbf.png)

For Fig. 5 I was can verify the resulta. The experiment shows that the client maintains connectivity under RED even though attackers flood 9Mbps of packets to the router:
![red-client.png](https://raw.githubusercontent.com/aaghdai/ddos/master/Results/red_client.png)

Further, I also analysed how sensitive these results are to do change of total attack bandwidth.
Under DropTail queue, attackers can further degrade the client's desired rate by flooding more data:
![result-tbf.png](https://raw.githubusercontent.com/aaghdai/ddos/master/Results/result-tbf.png)

Under RED however, increasing total attack bandwidth does not affect the user by a noticable margin:
![result-red.png](https://raw.githubusercontent.com/aaghdai/ddos/master/Results/result-red.png)

### Run My Experiment ###
<ol>
  <li>Create an architecture with a client, a server, and 12 attackers all connected to a router in a star network. An RSPEC for this topology is included in GENI/ .</li>
  <li>Install pre-requirements:
    <ol>
      <li>Install D-ITG on client, server, and attackers:
        <pre><code> $ sudo apt-get update
        $ sudo apt-get install d-itg </code></pre></li>
      <li> In order to capture and analyze the traces router needs scapy and matplotlib. Install these packages on router:
        <pre><code> $ sudo apt-get update
 $ sudo apt-get install python-scapy python-matplotlib </code></pre></li>
      <li> Copy following scripts from GENI/ to the router:
        <ol>
          <li> capture_and_analyze.py </li>
          <li> draw.py </li>
          <li> fig4.sh </li>
          <li> fig5.sh </li>
        </ol>
      </li>
    </ol>
  </li>
  <li> Get DropTail results:
    <ol>
      <li> Setup token bucket filter on the interface that connects router to the server:
        <pre><code> $ sudo tc qdisc del dev eth13 root
 $ sudo tc qdisc replace dev eth13 root tbf rate 1mbit limit 550 burst 550 peakrate 1.0001mbit mtu 560 </code></pre></li>
      </li>
      <li> At server, run ITGRecv:
        <pre><code> $ ITGRecv </code></pre></li>
      <li> At the router, run the script to reproduce Figure4, specifying interface to server and output file name:
        <pre><code> $ ./fig4.sh eth13 tbf | tee tbf.res </code></pre></li>
      </li>
    </ol>
  <li> Get RED results:
    <ol>
      <li> Setup RED on the interface that connects router to the server:
        <pre><code> $ sudo tc qdisc del dev eth13 root
 $ sudo tc qdisc replace dev eth13 root red limit 100000 min 4000 max 12500 avpkt 540 burst 12 probability 0.02 bandwidth 1mbi </code></pre></li>
      </li>
      <li> At server, run ITGRecv:
        <pre><code> $ ITGRecv </code></pre></li>
      <li> At the router, run the script to reproduce Figure5, specifying interface to server and output file name:
        <pre><code> $ ./fig5.sh eth13 red | tee red.res </code></pre></li>
    </ol>
  </li>
  <li> Sensitivity Analysis: run draw.py in the same folder as red.res & tbf.res.
    <pre><code> $ python draw.py </code></pre></li>
</ol>

### Notes ###
This experiment was done on: Linux 3.13.0-33-generic X86-64, Kentucky InstaGENI

To capture the packets and draw the plots following python packages are requiered:
<ol>
<li> Python 2.7.6 </li>
<li> scapy 2.2.0 </li>
<li> numpy 1.8.2 </li>
<li> matplotlib 1.3.1 </li>
</ol>

Using GENI for verifying the result of [1] is completely doable.
It's pretty easy to get the required resources even through InstaGENI, and modern linux kernels support all the queue management techniqeus used in this paper.

### Troubleshoot ###
<ol>
<li> Getting python error complaining about lack of $DISPLAY environment means that you need X forwarding to enable matplotlib plot functions.
On a Linux operating system you just need to pass -X to enable X forwarding:

<pre><code> $ ssh -X [user]@[machine] </code></pre>

To enable X forwarding on Windows/Mac follow these instructions:
[Windows](https://wiki.utdallas.edu/wiki/display/FAQ/X11+Forwarding+using+Xming+and+PuTTY)
[Mac Os](http://dyhr.com/2009/09/05/how-to-enable-x11-forwarding-with-ssh-on-mac-os-x-leopard/)

</li>
<li> Router keeps asking for password in order to connect a1-a12 machines: It means that you need to setup ssh key at router and let it connect to a1-a12 using the given keys. There are two workarounds for this problem:
<ol>
<li> Copy the private key you use for connecting to GENI machines as ~/.ssh/id_rsa. </li>
<li> Generate a new key for the router using ssh-keygen and copy it to a1-a12 using ssh-copy-id script.
<pre><code> $ ssh-keygen
 $ for i in {1..12};do ssh-copy-id a$i; done</code></pre>
</li>
</ol>
</li>
</ol>
