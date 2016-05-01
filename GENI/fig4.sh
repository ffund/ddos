TestDur=25
AtkDuration=22
AtkStart=1.5

of=$1

sudo ./capture_and_analyze.py eth13 $TestDur --output $of --bin 600 > 1 &

ssh -o "StrictHostKeyChecking no" client "nohup ITGSend -a server -l sender.log -x receiver.log -C 25 -c 500 -T UDP -t ${TestDur}000 > client.log &"

sleep $AtkStart

for a in a1 a2
do
    ssh -o "StrictHostKeyChecking no" $a "nohup ITGSend -a server -l sender.log -x receiver.log -C 150 -c 500 -T UDP -t ${AtkDuration}000 > $a.log &"
done

wait
sudo chmod 744 res.png
