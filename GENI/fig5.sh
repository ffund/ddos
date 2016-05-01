TestDur=25
AtkDuration=22
AtkStart=1.5

of=$1

sudo ./capture_and_analyze.py eth13 $TestDur --output $of --bin 600 > 1 &

ssh -o "StrictHostKeyChecking no" client "nohup ITGSend -a server -l sender.log -x receiver.log -C 25 -c 500 -T UDP -t ${TestDur}000 > client.log &"

sleep $AtkStart

for a in a1 a2 a3 a4 a5 a6
do
    ssh -o "StrictHostKeyChecking no" $a "nohup ITGSend -a server -l sender.log -x receiver.log -C 125 -c 500 -T UDP -t ${AtkDuration}000 > $a.log &"
done

for a in a7 a8 a9 a10 a11 a12
do
    ssh -o "StrictHostKeyChecking no" $a "nohup ITGSend -a server -l sender.log -x receiver.log -C 250 -c 500 -T UDP -t ${AtkDuration}000 > $a.log &"
done

wait
wait
sudo chmod 744 ${of}.png
