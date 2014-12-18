rm -rf build/
rm -rf /usr/lib/python2.6/site-packages/sps/
rm -rf /usr/bin/sps-*
mkdir -p /etc/sps
python setup.py install
rm -rf /etc/sps/*
cp -r ./etc/* /etc/sps/
ps aux | grep sps | grep -v grep | awk '{print $2}' | xargs kill -9
sps-api --debug
