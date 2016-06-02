for i in `mysql -uroot porta-configurator -sse "select ip from Servers"`
do
    h=`mysql -uroot porta-configurator -sse "select Name from Servers where IP='$i'"`
    echo -e "\n====== $h $i ======\n"
    rsh_porta.sh $i '
        red=`echo -en "\e[31m"`
        green=`echo -en "\e[32m"`
        normal=`echo -en "\e[0m"`
        echo -e "- - - ifconfig - - -\n"
        ifconfig  | sed -n "/^[a-z]\+/,+1p"
        echo "---------------------------"
        gw=`netstat -nr | grep ^0.0.0.0 | cut -d" " -f10`
        if [ $(sudo grep $gw /etc/sysconfig/network | sudo grep -qi gateway=; echo "$?") -eq 0 ]
        then
            echo "${green}GATEWAY=$gw is present in: /etc/sysconfig/network ${normal}"
        else
            echo "${red}GATEWAY=$gw is not present in the /etc/sysconfig/network - need to fix ${normal}"
        fi
        for i in $(netstat -i | egrep -vi "^inet|^lo|^vip|^Kernel|^Iface" | cut -d" " -f1)
        do
           echo -e "Interface : $i"
           egrep -i "^HWADDR|^onboot" /etc/sysconfig/network-scripts/ifcfg-$i          
           if [ $(sudo grep $gw /etc/sysconfig/network-scripts/ifcfg-$i | sudo grep -qi ^gateway; echo "$?") -eq 0 ]; then
               echo "${green}GATEWAY=$gw is present in: /etc/sysconfig/network-scripts/ifcfg-$i - you may skip /etc/sysconfig/network ${normal}"         
           fi          
           echo "---------------------------"
           sleep 1
        done'
done
