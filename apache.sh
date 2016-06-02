
for i in `mysql -uroot porta-configurator -sse "select ip from Servers where name like '%slave%' or name like  '%web%' or name like  '%um%'"`
do
    h=`mysql -uroot porta-configurator -sse "select Name from Servers where IP='$i'"`
    echo -e "\n----- $h $i -----\n"
    rsh_porta.sh $i '
    echo -e "-----The main conf :"
    grep "^Include" /etc/httpd/conf/httpd.conf
    echo -e "----------------\n"
    if [ -f ~/apache_configs.txt ] ; then sudo rm ~/apache_configs.txt; fi
    for i in $(ls --color=never /etc/httpd/conf.d/ | xargs echo ); do echo $i >> ~/apache_configs.txt; done
    sleep 1
    echo -e "The custom files are the following:\n "   
    for f in `egrep -vi "apreq.conf|call-recording.httpd.conf|custom-repository.httpd.conf|deny.conf|fcgid.conf|pagespeed.conf|performance.conf|perl.conf|perl-HTML-Mason.conf|php.conf|porta-configurator.httpd.conf|porta-fcgid.conf|porta.httpd.conf|porta-um.httpd.conf|README|ssl.conf" ~/apache_configs.txt | grep "\.conf$"`
    do
        echo -e "/etc/httpd/conf.d/$f\n "       
        for ip in `grep "<Virtual" /etc/httpd/conf.d/$f | sed "s/\s/:/g" | cut -d: -f2 | sort -u`
        do
            ifcfg=`grep "$ip" /etc/sysconfig/network-scripts/ifcfg-*`
            ifup=`ifconfig | grep "$ip" | sed "s/^\s*//"`
            netst=`sudo netstat -nlp | grep $ip | grep httpd | sed "s/^/\t\t\t/"`           
            printf "    %-20s%s\n" "virtual host ip:" "$ip"
            printf "    %-20s%s\n" "configuration file:" "$ifcfg"
            printf "    %-20s%s\n" "interface ip:" "$ifup"
            printf "    %s\n%s\n\n" "listening ports:" "$netst"
        done
    done'
done
