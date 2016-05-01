TestDur=25
AtkDuration=22
AtkStart=1.5
BinLen=600

iface=$1
of=$2

sudo ./capture_and_analyze.py $iface $TestDur --output $of --bin $BinLen --show > ${of}point.txt &

ssh -o "StrictHostKeyChecking no" client "nohup ITGSend -a server -l sender.log -x receiver.log -C 25 -c 500 -T UDP -t ${TestDur}000 > client.log &"

sleep $AtkStart

for a in a1 a2
do
    ssh -o "StrictHostKeyChecking no" $a "nohup ITGSend -a server -l sender.log -x receiver.log -C 150 -c 500 -T UDP -t ${AtkDuration}000 > $a.log &"
done

wait
sudo chmod 744 ${of}*png

sleep 10

for i in 100 125 150 175 200 
do
    AVG=""
    for j in 1 2 3 4 5
    do
        sudo ./capture_and_analyze.py $iface $TestDur --output $of --bin $BinLen > fig4.tmp &

        ssh -o "StrictHostKeyChecking no" client "nohup ITGSend -a server -l sender.log -x receiver.log -C 25 -c 500 -T UDP -t ${TestDur}000 > client.log &"

        sleep $AtkStart

        for a in a1 a2
        do
            ssh -o "StrictHostKeyChecking no" $a "nohup ITGSend -a server -l sender.log -x receiver.log -C $i -c 500 -T UDP -t ${AtkDuration}000 > $a.log &"
        done

        wait
        AVG="$AVG $(<fig4.tmp)"
        sleep 10
    done
    echo "$i: $AVG"
done
